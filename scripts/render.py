"""Render a claim-chain argument-chain YAML into Markdown and Mermaid views,
compute the logic score, and write the three-part report (logic, limitations,
missing evidence). Also derives each claim's verdict from its support links
(weakest-link rule), draws a one-page summary chart, follows each aim from the
introduction to the conclusion (golden thread), and counts the local checks of
each part of the paper.

Usage: python scripts/render.py examples/<paper>/<paper>.yaml examples/<paper>/generated/
Also checks that every relation points to a known statement or entity, and
recomputes every derived check that has a formula.
"""
import ast
import math
import operator
import sys
from pathlib import Path

import yaml

TYPE_STYLE = {
    "BACKGROUND": "bg", "GAP": "bg", "HYPOTHESIS": "claim", "AIM": "claim", "QUESTION": "q",
    "DEFINITION": "claim", "ASSUMPTION": "asm", "METHOD": "meth", "DATA": "meth",
    "OBSERVATION": "obs", "CLAIM": "claim", "LIMITATION": "lim", "OUTLOOK": "out",
}
CLASSDEFS = """  classDef bg fill:#eef2f7,stroke:#64748b,color:#111
  classDef claim fill:#dbeafe,stroke:#1d4ed8,color:#111
  classDef obs fill:#dcfce7,stroke:#15803d,color:#111
  classDef lim fill:#fee2e2,stroke:#b91c1c,color:#111
  classDef asm fill:#fef3c7,stroke:#b45309,color:#111
  classDef meth fill:#f3e8ff,stroke:#7e22ce,color:#111
  classDef out fill:#f1f5f9,stroke:#94a3b8,color:#111,stroke-dasharray:4 3
  classDef q fill:#ffffff,stroke:#334155,color:#111
  classDef ext fill:#ffffff,stroke:#64748b,color:#111,stroke-dasharray:2 2"""
EDGE = {
    "SUPPORTS": "-->", "MOTIVATES": "-->", "ANSWERS": "-->", "DEPENDS_ON": "-.->",
    "WEAKENS": "-.->", "CONTRADICTS": "-.->", "QUALIFIES": "-.->",
    "ALTERNATIVE_EXPLANATION_FOR": "-.->", "ANALOG_OF": "-.->", "CONDITIONALLY_SUPPORTS": "-.->",
    "DELIVERS": "-->", "RESTATES": "-.->",
}
SECTIONS = [
    ("Motivation", {"BACKGROUND", "GAP", "HYPOTHESIS", "AIM"}),
    ("Concept", {"DEFINITION", "QUESTION"}),
    ("Methods and data", {"METHOD", "ASSUMPTION", "DATA"}),
    ("Observations", {"OBSERVATION"}),
    ("Claims", {"CLAIM"}),
    ("Limitations (stated by authors)", {"LIMITATION"}),
    ("Outlook", {"OUTLOOK"}),
]
# Draft weighting of verdicts for the logic score.
# WEAK sits halfway between PARTIAL and INCONCLUSIVE, so v0.4 scores are unchanged.
VALIDITY_SCORE = {"YES": 1.0, "PARTIAL": 0.5, "WEAK": 0.375, "INCONCLUSIVE": 0.25, "NO": 0.0}
VALIDITY_MARK = {"YES": "✓", "PARTIAL": "◐", "WEAK": "◔", "INCONCLUSIVE": "?", "NO": "✗"}
MERMAID_MARK = {"YES": "✓", "PARTIAL": "(partial)", "WEAK": "(weak)", "INCONCLUSIVE": "?", "NO": "✗"}  # ◐ is missing from the default font
SCORED_TYPES = {"CLAIM", "HYPOTHESIS"}
SCORE_METHOD = ("mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, "
                "INCONCLUSIVE=0.25, NO=0 (draft weighting)")
# Draft weights by claim_role for the weighted score; statements without a role weigh 1.
ROLE_WEIGHT = {"MAIN_CONCLUSION": 3.0, "COUNTER_CLAIM": 0.0}
WEIGHTED_METHOD = ("as the logic score, but MAIN_CONCLUSION weighs 3, COUNTER_CLAIM 0 "
                   "and every other claim or hypothesis 1 (draft weighting)")
OBLIGATION_SCORE = {"DISCHARGED": 1.0, "PARTIALLY_DISCHARGED": 0.5, "OPEN": 0.0}


def logic_score(chain):
    scored = [s for s in chain["statements"] if s["statement_type"] in SCORED_TYPES]
    verdicts = [s["assessment"]["validity"] for s in scored if s.get("assessment")]
    unassessed = [s["id"] for s in scored if not s.get("assessment")]
    score = sum(VALIDITY_SCORE[v] for v in verdicts) / len(verdicts) if verdicts else None
    counts = {v: verdicts.count(v) for v in VALIDITY_SCORE}
    return score, counts, unassessed


def weighted_logic_score(chain):
    pairs = [(ROLE_WEIGHT.get(s.get("claim_role"), 1.0), VALIDITY_SCORE[s["assessment"]["validity"]])
             for s in chain["statements"] if s["statement_type"] in SCORED_TYPES and s.get("assessment")]
    total = sum(w for w, _ in pairs)
    return sum(w * v for w, v in pairs) / total if total else None


LINK_CRITERIA = ["directness", "sufficiency", "controls", "alternatives", "scope_match"]
SUPPORT_LINKS = {"SUPPORTS", "CONDITIONALLY_SUPPORTS"}
CAPPING_LINKS = {"WEAKENS", "QUALIFIES", "ALTERNATIVE_EXPLANATION_FOR"}
RANK = ["NO", "INCONCLUSIVE", "WEAK", "PARTIAL", "YES"]
STRENGTH_VERDICT = {"STRONG": "YES", "INTERMEDIATE": "PARTIAL", "WEAK": "WEAK", "UNSUPPORTED": "INCONCLUSIVE"}
DERIVED_METHOD = ("verdicts derived from the links: an incoming CONTRADICTS gives NO; otherwise the strongest "
                  "support link decides (STRONG YES, INTERMEDIATE PARTIAL, WEAK WEAK, none INCONCLUSIVE); "
                  "WEAKENS, QUALIFIES or an alternative explanation caps at PARTIAL; CONDITIONALLY_SUPPORTS "
                  "counts as WEAK at most; an essential link caps the claim at its own strength and at the derived "
                  "verdict of the claim it comes from. Links without a strength count as INTERMEDIATE. Claims "
                  "without links keep the annotator's verdict")


def link_strength(r):
    """Support strength derived from the five link criteria, or the annotator's rating if no criteria are given."""
    c = r.get("link_criteria") or {}
    vals = {k: c[k] for k in LINK_CRITERIA if c.get(k) and c[k] != "NOT_APPLICABLE"}
    if not vals:
        strength = r.get("support_strength") or "INTERMEDIATE"
    else:
        failed = [k for k, v in vals.items() if v == "NOT_MET"]
        partly = [k for k, v in vals.items() if v == "PARTLY"]
        if len(failed) >= 2 or {"directness", "scope_match"} & set(failed):
            strength = "UNSUPPORTED"
        elif failed or len(partly) > 2:
            strength = "WEAK"
        elif partly:
            strength = "INTERMEDIATE"
        else:
            strength = "STRONG"
    if r["predicate"] == "CONDITIONALLY_SUPPORTS" and strength in {"STRONG", "INTERMEDIATE"}:
        strength = "WEAK"
    return strength


def _cap(verdict, limit):
    return min(verdict, limit, key=RANK.index)


def derived_verdicts(chain):
    """Derived verdict per CLAIM and HYPOTHESIS (None where the statement has no incoming links to derive from)."""
    stmts = {s["id"]: s for s in chain["statements"]}
    incoming = {}
    for r in chain["relations"]:
        incoming.setdefault(r["object"], []).append(r)
    memo, visiting = {}, set()

    def derive(sid):
        if sid in memo:
            return memo[sid]
        if sid in visiting:  # cycle: no cap from this side
            return None
        visiting.add(sid)
        rels = incoming.get(sid, [])
        supports = [r for r in rels if r["predicate"] in SUPPORT_LINKS]
        if any(r["predicate"] == "CONTRADICTS" for r in rels):
            verdict = "NO"
        elif not supports and not any(r["predicate"] in CAPPING_LINKS for r in rels):
            verdict = None
        else:
            strengths = [link_strength(r) for r in supports]
            verdict = max((STRENGTH_VERDICT[x] for x in strengths), key=RANK.index, default="INCONCLUSIVE")
            if any(r["predicate"] in CAPPING_LINKS for r in rels):
                verdict = _cap(verdict, "PARTIAL")
            for r, x in zip(supports, strengths):
                if not r.get("essential"):
                    continue
                verdict = _cap(verdict, STRENGTH_VERDICT[x])
                src = stmts.get(r["subject"])
                if src and src["statement_type"] in SCORED_TYPES:
                    up = derive(src["id"])
                    if up is None and src.get("assessment"):
                        up = src["assessment"]["validity"]
                    if up:
                        verdict = _cap(verdict, up)
        visiting.discard(sid)
        memo[sid] = verdict
        return verdict

    return {s["id"]: derive(s["id"]) for s in chain["statements"] if s["statement_type"] in SCORED_TYPES}


def derived_score(chain):
    """Logic score over derived verdicts (annotator's verdict where none can be derived), and the disagreements."""
    derived = derived_verdicts(chain)
    vals, differ = [], []
    for s in chain["statements"]:
        a = s.get("assessment")
        if s["statement_type"] not in SCORED_TYPES or not a:
            continue
        d = derived.get(s["id"])
        vals.append(VALIDITY_SCORE[d or a["validity"]])
        if d and d != a["validity"]:
            differ.append((s["id"], a["validity"], d))
    return (sum(vals) / len(vals) if vals else None), differ


def obligation_coverage(chain):
    status = [o["obligation_status"] for s in chain["statements"]
              for o in (s.get("assessment") or {}).get("proof_obligations", [])]
    return (sum(OBLIGATION_SCORE[x] for x in status) / len(status) if status else None), len(status)


# ---- golden thread and local checks (Sepideh's paper logic map) ----

END_PARTS = {"CONCLUSION", "ABSTRACT"}
CERTAINTY_RANK = ["SPECULATIVE", "PROPOSED", "PREDICTED", "DEMONSTRATED"]
CHECK_KIND = {
    "completeness": {"REPRODUCIBILITY", "MISSING_QUANTIFICATION"},
    "arithmetic": {"ARITHMETIC"},
    "consistency": {"INTERNAL_INCONSISTENCY", "UNACKNOWLEDGED_CONFLICT", "UNADDRESSED_COUNTEREVIDENCE"},
}


def golden_thread(chain):
    """Follow each AIM to what delivers it. Returns (rows, unpromised main conclusions, certainty drift)."""
    stmts = {s["id"]: s for s in chain["statements"]}
    rels = chain["relations"]
    aims = [s for s in chain["statements"] if s["statement_type"] == "AIM"]
    restated_by = {}
    for r in rels:
        if r["predicate"] == "RESTATES":
            restated_by.setdefault(r["object"], []).append(r["subject"])
    has_end = any(s.get("paper_part") in END_PARTS for s in chain["statements"])

    def at_end(sid, seen=()):
        if stmts.get(sid, {}).get("paper_part") in END_PARTS:
            return True
        return any(at_end(x, seen + (sid,)) for x in restated_by.get(sid, []) if x not in seen)

    rows = []
    for a in aims:
        gaps = [r["subject"] for r in rels if r["object"] == a["id"] and r["predicate"] == "MOTIVATES"
                and stmts.get(r["subject"], {}).get("statement_type") == "GAP"]
        gaps += [r["object"] for r in rels if r["subject"] == a["id"] and r["predicate"] == "ANSWERS"]
        by = [stmts[r["subject"]] for r in rels if r["object"] == a["id"] and r["predicate"] == "DELIVERS"
              and r["subject"] in stmts]
        shown = [x for x in by if x["statement_type"] in {"OBSERVATION", "CLAIM"}]
        if not by:
            outcome = "DROPPED"
        elif not shown:
            outcome = "METHOD ONLY"
        elif has_end and not any(at_end(x["id"]) for x in by):
            outcome = "NOT RESTATED"
        else:
            outcome = "DELIVERED"
        rows.append({"aim": a, "gaps": gaps, "by": by, "outcome": outcome})

    unpromised = []
    if aims:
        delivers_from = {r["subject"] for r in rels if r["predicate"] == "DELIVERS"}
        to_hyp = {r["subject"] for r in rels if r["predicate"] in SUPPORT_LINKS
                  and stmts.get(r["object"], {}).get("statement_type") == "HYPOTHESIS"}
        restates = {r["subject"]: r["object"] for r in rels if r["predicate"] == "RESTATES"}
        for s in chain["statements"]:
            if s["statement_type"] != "CLAIM" or s.get("claim_role") != "MAIN_CONCLUSION":
                continue
            ids, x = {s["id"]}, s["id"]
            while x in restates and restates[x] not in ids:
                x = restates[x]
                ids.add(x)
            if not ids & (delivers_from | to_hyp):
                unpromised.append(s)

    drift = []
    for r in rels:
        if r["predicate"] != "RESTATES":
            continue
        later, earlier = stmts.get(r["subject"]), stmts.get(r["object"])
        if not later or not earlier or not later.get("author_certainty") or not earlier.get("author_certainty"):
            continue
        d = CERTAINTY_RANK.index(later["author_certainty"]) - CERTAINTY_RANK.index(earlier["author_certainty"])
        if d:
            drift.append((earlier, later, "STRENGTHENED" if d > 0 else "WEAKENED"))
    return rows, unpromised, drift


def overstated(chain):
    """Claims the authors present as demonstrated that the annotator finds weak, inconclusive or contradicted."""
    return [s for s in chain["statements"] if s.get("author_certainty") == "DEMONSTRATED"
            and (s.get("assessment") or {}).get("validity") in {"WEAK", "INCONCLUSIVE", "NO"}]


def part_checks(chain):
    """Issue counts per paper part and check kind; failed derived checks count as arithmetic."""
    counts = {}
    failed = {sid for sid, _, status, _ in run_checks(chain) if status not in {"ok", "not machine-checkable"}}
    for s in chain["statements"]:
        part = s.get("paper_part", "UNSPECIFIED")
        row = counts.setdefault(part, {"completeness": 0, "arithmetic": 0, "consistency": 0, "argument": 0, "high": 0})
        for c in s.get("concerns", []):
            kind = next((k for k, types in CHECK_KIND.items() if c["concern_type"] in types), "argument")
            row[kind] += 1
            if c.get("priority") in {"CRITICAL", "HIGH"}:
                row["high"] += 1
        if s["id"] in failed:
            row["arithmetic"] += 1
    return {p: r for p, r in counts.items() if sum(v for k, v in r.items() if k != "high")}


def fmt_score(x):
    return "n/a" if x is None else f"{x:.2f}"


# ---- derived checks: safe evaluation of arithmetic formulas over value symbols ----

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
        ast.Pow: operator.pow, ast.USub: operator.neg, ast.UAdd: operator.pos,
        ast.Lt: operator.lt, ast.LtE: operator.le, ast.Gt: operator.gt, ast.GtE: operator.ge,
        ast.Eq: operator.eq, ast.NotEq: operator.ne}
_FUNCS = {"abs": abs, "min": min, "max": max, "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
          "exp": math.exp, "sin": math.sin, "cos": math.cos, "tan": math.tan, "asin": math.asin,
          "acos": math.acos, "atan": math.atan, "degrees": math.degrees, "radians": math.radians}
_CONSTS = {"pi": math.pi, "k_B": 8.617333262e-5}  # k_B in eV/K


def _eval(node, env):
    if isinstance(node, ast.Expression):
        return _eval(node.body, env)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id] if node.id in env else _CONSTS[node.id]
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left, env), _eval(node.right, env))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand, env))
    if isinstance(node, ast.Compare):
        left = _eval(node.left, env)
        for op, comp in zip(node.ops, node.comparators):
            right = _eval(comp, env)
            if not _OPS[type(op)](left, right):
                return False
            left = right
        return True
    if isinstance(node, ast.BoolOp):
        vals = [_eval(v, env) for v in node.values]
        return all(vals) if isinstance(node.op, ast.And) else any(vals)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in _FUNCS:
        return _FUNCS[node.func.id](*[_eval(a, env) for a in node.args])
    raise ValueError(f"unsupported expression: {ast.dump(node)}")


def _close(computed, reported):
    """Equal up to the precision the reported number is given in (or 1 %)."""
    decimals = len(repr(float(reported)).split(".")[1].rstrip("0")) if "." in repr(float(reported)) else 0
    return abs(computed - reported) <= max(0.01 * abs(reported), 0.5 * 10 ** -decimals)


def run_checks(chain):
    """Recompute every derived check with a formula. Returns a list of (statement id, check, status, computed)."""
    out = []
    for s in chain["statements"]:
        for e in s.get("evidence", []):
            env = {v["symbol"]: v["value"] for v in e.get("values", []) if v.get("symbol")}
            for c in e.get("derived_checks", []):
                if not c.get("formula"):
                    out.append((s["id"], c, "not machine-checkable", None))
                    continue
                try:
                    got = _eval(ast.parse(c["formula"], mode="eval"), env)
                except Exception as exc:  # unknown symbol, bad syntax
                    out.append((s["id"], c, f"error: {exc}", None))
                    continue
                if isinstance(got, bool):
                    ok = c.get("satisfied") is None or got == c["satisfied"]
                else:
                    ok = c.get("result") is None or _close(got, c["result"])
                out.append((s["id"], c, "ok" if ok else "MISMATCH", got))
    return out


def label(x):
    return x.lower().replace("_", " ")


def short(i):
    return i.split(":", 1)[1]


def node(i):
    return short(i).replace("-", "_").replace(".", "_")


def evidence_str(ev):
    parts = []
    for e in ev or []:
        s = e["evidence_kind"].lower()
        if e.get("locator"):
            s += f" ({e['locator']})"
        if e.get("references"):
            s += " [" + ", ".join(e["references"]) + "]"
        if e.get("description"):
            s += f": {e['description']}"
        parts.append(s)
    return "; ".join(parts) or "none given"


def check(chain):
    known = {s["id"] for s in chain["statements"]}
    known |= {e["id"] for e in chain.get("entities", [])}
    bad = [(r["id"], x) for r in chain["relations"] for x in (r["subject"], r["object"]) if x not in known]
    bad += [(s["id"], x) for s in chain["statements"]
            for o in (s.get("assessment") or {}).get("proof_obligations", [])
            for x in o.get("discharged_by", []) if x not in known]
    for rid, x in bad:
        print(f"dangling reference in {rid}: {x}", file=sys.stderr)
    failed = [r for r in run_checks(chain) if r[2] not in {"ok", "not machine-checkable"}]
    for sid, c, status, got in failed:
        print(f"derived check in {sid} ({c['expression']}): {status}, computed {got}", file=sys.stderr)
    return not bad and not failed


def warrant_str(w):
    bits = [label(x) for x in (w.get("warrant_basis"), w.get("support_strength")) if x]
    if w.get("references"):
        bits.append("refs " + ", ".join(w["references"]))
    return w["rule"].strip() + (f" ({'; '.join(bits)})" if bits else "")


def check_str(c, got=None, status=None):
    s = c["expression"]
    if c.get("result") is not None:
        s += f" = {c['result']:g}" + (f" {c['unit']}" if c.get("unit") else "")
    if c.get("satisfied") is not None:
        s += " ✓ satisfied" if c["satisfied"] else " ✗ not satisfied"
    if status == "ok":
        s += " (recomputed)"
    elif status:
        s += f" ({status}" + (f", computed {got:g}" if isinstance(got, (int, float)) and not isinstance(got, bool) else "") + ")"
    return s


def markdown(chain):
    pub = chain["publication"]
    rel_out, rel_in = {}, {}
    for r in chain["relations"]:
        rel_out.setdefault(r["subject"], []).append(r)
        rel_in.setdefault(r["object"], []).append(r)
    L = [f"# Argument chain: {pub['title']}", "",
         f"{', '.join(pub['authors'])} ({pub['year']}), {pub['id']}. "
         f"Generated from the claim-chain YAML (schema {chain['schema_version']}); do not edit by hand.", ""]
    score, counts, _ = logic_score(chain)
    if score is not None:
        L += [f"**Logic score: {score:.2f}** ({', '.join(f'{v} {k}' for k, v in counts.items())}), "
              f"weighted by claim role: {fmt_score(weighted_logic_score(chain))}. "
              f"Method: {SCORE_METHOD}.", ""]
    checks = {}
    for sid, c, status, got in run_checks(chain):
        checks[id(c)] = (status, got)
    for title, types in SECTIONS:
        sts = [s for s in chain["statements"] if s["statement_type"] in types]
        if not sts:
            continue
        L += [f"## {title}", ""]
        for s in sts:
            hedge = " *(hedged)*" if s.get("hedged") else ""
            tags = " ".join(f"`{label(s[k])}`" for k in ("claim_role", "author_certainty", "priority") if s.get(k))
            L.append(f"**{short(s['id'])}** `{s['statement_type']}` {tags} {s.get('section', '')}{hedge}  ")
            L.append(f"{s['text']}  ")
            if s["statement_type"] not in {"HYPOTHESIS", "QUESTION", "DEFINITION"} or s.get("evidence"):
                L.append(f"Evidence: {evidence_str(s.get('evidence'))}  ")
            for e in s.get("evidence", []):
                for c in e.get("derived_checks", []):
                    L.append(f"Check: {check_str(c, *reversed(checks.get(id(c), (None, None))))}  ")
            if s.get("warrant"):
                L.append(f"Warrant: {warrant_str(s['warrant'])}  ")
            if s.get("claim_modality"):
                L.append(f"Modality: {label(s['claim_modality'])}  ")
            if s.get("assumption_basis"):
                L.append(f"Basis: {label(s['assumption_basis'])}. Open question: {s.get('open_question', '-')}  ")
            if s.get("limitation_kind"):
                L.append(f"Kind: {label(s['limitation_kind'])}  ")
            sc = s.get("scope")
            if sc:
                bits = [", ".join(short(m) for m in sc.get("materials", []))]
                if sc.get("sample_count"):
                    bits.append(f"n = {sc['sample_count']}")
                if sc.get("scope_note"):
                    bits.append(sc["scope_note"])
                L.append("Scope: " + "; ".join(b for b in bits if b) + "  ")
            for r in rel_out.get(s["id"], []):
                who = {"ANNOTATOR": " *(annotator)*", "ANNOTATOR_BACKGROUND": " *(annotator, background knowledge)*"}.get(r["asserted_by"], "")
                attrs = ", ".join(label(r[k]) + (" uncertainty" if k == "uncertainty" else "")
                                  for k in ("support_basis", "support_strength", "uncertainty") if r.get(k))
                attrs = f" [{attrs}]" if attrs else ""
                L.append(f"→ {label(r['predicate'])} **{short(r['object'])}**{attrs}{who}  ")
                if r.get("warrant"):
                    L.append(f"&nbsp;&nbsp;&nbsp;warrant: {warrant_str(r['warrant'])}  ")
            for c in s.get("concerns", []):
                pr = f" ({label(c['priority'])})" if c.get("priority") else ""
                L.append(f"⚠ {label(c['concern_type'])}{pr}: {c['description']}  ")
            a = s.get("assessment")
            if a:
                L.append(f"**Verdict: {VALIDITY_MARK[a['validity']]} {a['validity']}**. {a['rationale']}  ")
                for m in a.get("missing_evidence", []):
                    L.append(f"Missing: {m}  ")
                for o in a.get("proof_obligations", []):
                    by = ", ".join(short(x) for x in o.get("discharged_by", []))
                    pr = f", {label(o['priority'])}" if o.get("priority") else ""
                    L.append(f"Obligation ({label(o['obligation_status'])}{pr}): {o['text']}" + (f" ← {by}" if by else "") + "  ")
                    for d in o.get("requested_data", []):
                        L.append(f"&nbsp;&nbsp;&nbsp;needs: {d['quantity']}" + (f" [{d['unit']}]" if d.get("unit") else "")
                                 + (f" via {d['method']}" if d.get("method") else "") + "  ")
            L.append("")
    return "\n".join(L)


def mermaid(chain, include=None):
    keep = include or {s["id"] for s in chain["statements"]}
    L = ["flowchart TD"]
    used = set()
    for r in chain["relations"]:
        a, b = r["subject"], r["object"]
        if a not in keep or b not in keep and not b.startswith("ent:"):
            continue
        lbl = r["predicate"].lower().replace("_", " ")
        arrow = EDGE[r["predicate"]]
        if r["predicate"] == "SUPPORTS" and r.get("support_strength") == "STRONG":
            L.append(f"  {node(a)} ==> {node(b)}")
        elif r["predicate"] in {"SUPPORTS", "MOTIVATES", "DEPENDS_ON", "DELIVERS"}:
            L.append(f"  {node(a)} {arrow} {node(b)}")
        else:
            L.append(f"  {node(a)} {arrow}|{lbl}| {node(b)}")
        used |= {a, b}
    stmts = {s["id"]: s for s in chain["statements"]}
    for i in sorted(used):
        if i in stmts:
            s = stmts[i]
            words = s["text"].replace('"', "'").split()
            txt = " ".join(words[:9]) + (" …" if len(words) > 9 else "")
            mark = f" {MERMAID_MARK[s['assessment']['validity']]}" if s.get("assessment") else ""
            L.append(f'  {node(i)}["<b>{short(i)}{mark}</b><br/>{txt}"]:::{TYPE_STYLE[s["statement_type"]]}')
        else:
            L.append(f'  {node(i)}(["{short(i)}"]):::ext')
    L.append(CLASSDEFS)
    return "\n".join(L)


SUMMARY_WORD = {"YES": "True", "PARTIAL": "Partly true", "WEAK": "Weak",
                "INCONCLUSIVE": "Not supported", "NO": "Contradicted"}
SUMMARY_CLASS = {"YES": "yes", "PARTIAL": "partly", "WEAK": "weak", "INCONCLUSIVE": "no", "NO": "no"}
SUMMARY_CLASSDEFS = """  classDef idea fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
  classDef claim fill:#ffffff,stroke:#616161,color:#000
  classDef yes fill:#c8e6c9,stroke:#2e7d32,color:#000
  classDef partly fill:#fff9c4,stroke:#f9a825,color:#000
  classDef weak fill:#ffe0b2,stroke:#ef6c00,color:#000
  classDef no fill:#ffcdd2,stroke:#c62828,color:#000
  classDef bottom fill:#f5f5f5,stroke:#212121,stroke-width:2px,color:#000"""


def _plain(text, words=None):
    """Text for a Mermaid markdown string: no quotes or markup, cut to `words`. Mermaid wraps it."""
    w = text.replace('"', "'").replace("`", "'").replace("*", "").replace("_", " ").split()
    if words and len(w) > words:
        w = w[:words] + ["…"]
    return " ".join(w)


def _first_sentence(text):
    return text.strip().split(". ")[0].rstrip(".") + "."


def summary_mermaid(chain, max_claims=6):
    """One-page chart for any reader: thesis, main conclusions, verdict in words, bottom line (after Soroush's D1)."""
    sts = chain["statements"]
    hyp = next((s for s in sts if s["statement_type"] == "HYPOTHESIS"), None)
    mains = [s for s in sts if s["statement_type"] == "CLAIM" and s.get("claim_role") == "MAIN_CONCLUSION"
             and s.get("assessment")][:max_claims]
    top = _plain(hyp["text"] if hyp else chain["publication"]["title"], 25)
    head = "The paper sets out to show" if hyp else "Paper"
    L = ["flowchart TB", f'  P["`**{head}**\n{top}`"]:::idea']
    for i, s in enumerate(mains):
        v = s["assessment"]["validity"]
        L.append(f'  C{i}("`**{short(s["id"])}**\n{_plain(s["text"], 16)}`"):::claim')
        L.append(f'  V{i}["`**{SUMMARY_WORD[v]}**\n{_plain(_first_sentence(s["assessment"]["rationale"]), 20)}`"]'
                 f":::{SUMMARY_CLASS[v]}")
        L += [f"  P --> C{i}", f"  C{i} --> V{i}", f"  V{i} --> BL"]
    pa = chain.get("paper_assessment") or {}
    overall = pa.get("overall_validity") or (hyp or {}).get("assessment", {}).get("validity")
    bottom = (f"Overall: {SUMMARY_WORD[overall]}. " if overall else "") + _first_sentence(pa.get("summary", ""))
    L.append(f'  BL["`**Bottom line**\n{_plain(bottom, 35)}`"]:::bottom')
    if not mains:
        L.append("  P --> BL")
    L.append(SUMMARY_CLASSDEFS)
    return "\n".join(L) + "\n"


def report(chain):
    """The three outputs from the blackboard: logic, limitations, missing evidence."""
    pub, pa = chain["publication"], chain.get("paper_assessment", {})
    score, counts, unassessed = logic_score(chain)
    sts = chain["statements"]
    L = [f"# claim-chain report: {pub['title']}", "",
         f"{', '.join(pub['authors'])} ({pub['year']}), {pub['id']}. Generated; do not edit by hand.", ""]
    L += ["## 1. Logic", ""]
    coverage, n_obl = obligation_coverage(chain)
    if pa.get("overall_validity"):
        L.append(f"**Overall: {VALIDITY_MARK[pa['overall_validity']]} {pa['overall_validity']}** · "
                 f"**Logic score: {score:.2f}** · weighted: {fmt_score(weighted_logic_score(chain))} · "
                 f"proof obligations discharged: {fmt_score(coverage)} (of {n_obl})  ")
    L.append(f"Score method: {SCORE_METHOD}. Weighted: {WEIGHTED_METHOD}.  ")
    L.append(f"Verdicts: {', '.join(f'{v} {k}' for k, v in counts.items())}."
             + (f" Not yet assessed: {', '.join(short(u) for u in unassessed)}." if unassessed else ""))
    if pa.get("summary"):
        L += ["", pa["summary"]]
    dscore, differ = derived_score(chain)
    derived = derived_verdicts(chain)
    L += ["", f"**Score from derived verdicts: {fmt_score(dscore)}**, {len(differ)} claim(s) where the derived "
          f"verdict differs from the annotator's. Method: {DERIVED_METHOD}.  "]
    L += ["", "| Statement | Role | Modality | Authors say | Verdict | Derived | Rationale |", "|---|---|---|---|---|---|---|"]
    for s in sts:
        a = s.get("assessment")
        if s["statement_type"] in SCORED_TYPES and a:
            d = derived.get(s["id"])
            dv = "-" if not d else ("same" if d == a["validity"] else f"**{VALIDITY_MARK[d]} {d}**")
            L.append(f"| **{short(s['id'])}** {s['text']} | {label(s.get('claim_role', '-'))} | "
                     f"{label(s.get('claim_modality', '-'))} | {label(s.get('author_certainty', '-'))} | "
                     f"{VALIDITY_MARK[a['validity']]} {a['validity']} | {dv} | {a['rationale']} |")
    rated = [r for r in chain["relations"] if r.get("link_criteria")]
    if rated:
        abbrev = {"MET": "✓", "PARTLY": "◐", "NOT_MET": "✗", "NOT_APPLICABLE": "–"}
        L += ["", "**Support links tested on the five criteria** (directness, sufficiency, controls, alternatives, "
              "scope match; ✓ met, ◐ partly, ✗ not met, – not applicable):", "",
              "| Link | Criteria | Strength | Note |", "|---|---|---|---|"]
        for r in rated:
            c = r["link_criteria"]
            x = link_strength(r)
            given = r.get("support_strength")
            st = label(x) + (f" (annotator: {label(given)})" if given and given != x else "")
            ess = " (essential)" if r.get("essential") else ""
            L.append(f"| {short(r['subject'])} → {short(r['object'])}{ess} | "
                     f"{''.join(abbrev.get(c.get(k), '·') for k in LINK_CRITERIA)} | {st} | {c.get('criteria_note', '')} |")
    rows, unpromised, drift = golden_thread(chain)
    if rows:
        L += ["", "**Golden thread** (each aim from the introduction to the end of the paper):", "",
              "| Aim | Gap | Method | Result | Claim (verdict) | Outcome |", "|---|---|---|---|---|---|"]
        for t in rows:
            by = lambda types: ", ".join(short(x["id"]) for x in t["by"] if x["statement_type"] in types) or "-"
            claims = ", ".join(f"{short(x['id'])} ({VALIDITY_MARK[x['assessment']['validity']]})" if x.get("assessment")
                               else short(x["id"]) for x in t["by"] if x["statement_type"] == "CLAIM") or "-"
            L.append(f"| **{short(t['aim']['id'])}** {t['aim']['text']} | {', '.join(short(g) for g in t['gaps']) or '-'} | "
                     f"{by({'METHOD', 'DATA'})} | {by({'OBSERVATION'})} | {claims} | {t['outcome']} |")
        L.append("")
        L.append("Outcomes: DELIVERED, NOT RESTATED (delivered but absent from the conclusion and abstract), "
                 "METHOD ONLY (carried out but no result shown), DROPPED (nothing delivers it).")
    if unpromised:
        L += ["", "**Main conclusions no aim or hypothesis promised:** "
              + ", ".join(short(s["id"]) for s in unpromised) + "."]
    if drift:
        L += ["", "**Certainty drift between restatements:**", ""]
        for earlier, later, kind in drift:
            L.append(f"- {kind}: **{short(earlier['id'])}** ({label(earlier['author_certainty'])}, "
                     f"{label(earlier.get('paper_part', '-'))}) → **{short(later['id'])}** "
                     f"({label(later['author_certainty'])}, {label(later.get('paper_part', '-'))})")
    over = overstated(chain)
    if over:
        L += ["", "**Presented as demonstrated, but the verdict is weak, inconclusive or no:** "
              + ", ".join(f"{short(s['id'])} ({s['assessment']['validity']})" for s in over) + "."]
    results = run_checks(chain)
    if results:
        L += ["", "**Recomputed checks:**", ""]
        for sid, c, status, got in results:
            L.append(f"- **{short(sid)}** {check_str(c, got, status)}")
    parts = {}
    for s in sts:
        parts.setdefault(s.get("paper_part", "UNSPECIFIED"), []).append(s)
    L += ["", "**Statements per paper part:**", "", "| Part | Statements |", "|---|---|"]
    for part, ps in parts.items():
        L.append(f"| {label(part)} | {', '.join(short(s['id']) for s in ps)} |")
    causal = [s for s in sts if s.get("claim_modality") == "CAUSAL"]
    if causal:
        L += ["", "Causal claims (check against correlational evidence): "
              + ", ".join(short(s["id"]) for s in causal) + "."]
    L += ["", "## 2. Limitations", ""]
    for k in pa.get("key_limitations", []):
        L.append(f"- {k}")
    L += ["", "**Stated by the authors:**", ""]
    for s in sts:
        if s["statement_type"] == "LIMITATION":
            L.append(f"- **{short(s['id'])}** ({label(s.get('limitation_kind', '-'))}): {s['text']}")
    L += ["", "**Assumptions the argument rests on:**", ""]
    for s in sts:
        if s["statement_type"] == "ASSUMPTION":
            L.append(f"- **{short(s['id'])}** ({label(s.get('assumption_basis', '-'))}): {s['text']} "
                     f"*Open question:* {s.get('open_question', '-')}")
    weak = [(x, w) for x, w in
            [(s["id"], s["warrant"]) for s in sts if s.get("warrant")]
            + [(f"{r['subject']}→{short(r['object'])}", r["warrant"]) for r in chain["relations"] if r.get("warrant")]
            if w.get("warrant_basis") in {"EMPIRICAL_CORRELATION", "UNSTATED", "AUTHOR_ARGUMENT"}
            or w.get("support_strength") == "WEAK"]
    if weak:
        L += ["", "**Inference rules that are empirical, unstated, argued only by the authors, or weak:**", ""]
        for x, w in weak:
            L.append(f"- **{short(x)}**: {warrant_str(w)}")
    L += ["", "**Flagged by the annotator:**", ""]
    for s in sts:
        for c in s.get("concerns", []):
            pr = f" ({label(c['priority'])})" if c.get("priority") else ""
            L.append(f"- **{short(s['id'])}** {label(c['concern_type'])}{pr}: {c['description']}")
    pc = part_checks(chain)
    if pc:
        L += ["", "**Local checks per part** (issues found; failed derived checks count as arithmetic):", "",
              "| Part | Completeness | Arithmetic | Consistency | Argument | High or critical |", "|---|---|---|---|---|---|"]
        for part, r in pc.items():
            L.append(f"| {label(part)} | {r['completeness']} | {r['arithmetic']} | {r['consistency']} | "
                     f"{r['argument']} | {r['high']} |")
    L += ["", "## 3. Missing evidence", ""]
    for m in pa.get("missing_evidence", []):
        L.append(f"- {m}")
    L += ["", "**Open proof obligations:**", ""]
    for s in sts:
        for o in (s.get("assessment") or {}).get("proof_obligations", []):
            if o["obligation_status"] != "DISCHARGED":
                by = ", ".join(short(x) for x in o.get("discharged_by", []))
                pr = f", {label(o['priority'])}" if o.get("priority") else ""
                need = "; ".join(d["quantity"] + (f" [{d['unit']}]" if d.get("unit") else "")
                                 + (f" via {d['method']}" if d.get("method") else "") for d in o.get("requested_data", []))
                L.append(f"- **{short(s['id'])}** ({label(o['obligation_status'])}{pr}): {o['text']}"
                         + (f" (partly: {by})" if by else "") + (f" Needs: {need}." if need else ""))
    questions = [s for s in sts if s["statement_type"] == "QUESTION" and s.get("priority")]
    if questions:
        L += ["", "**Open questions by priority:**", ""]
        order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
        for s in sorted(questions, key=lambda s: order.index(s["priority"])):
            L.append(f"- **{short(s['id'])}** ({label(s['priority'])}): {s['text']}")
    L += ["", "**Per statement:**", ""]
    for s in sts:
        for m in (s.get("assessment") or {}).get("missing_evidence", []):
            L.append(f"- **{short(s['id'])}**: {m}")
    return "\n".join(L) + "\n"


def thread_summary(chain):
    rows, unpromised, drift = golden_thread(chain)
    if not rows:
        return ""
    outcomes = [t["outcome"] for t in rows]
    bits = [f"{outcomes.count(o)} {o.lower()}" for o in ["DELIVERED", "NOT RESTATED", "METHOD ONLY", "DROPPED"]
            if o in outcomes]
    bits += [f"{len(unpromised)} unpromised"] if unpromised else []
    bits += [f"{sum(1 for d in drift if d[2] == 'STRENGTHENED')} strengthened"] if drift else []
    return f"; aims: {', '.join(bits)}"


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    chain = yaml.safe_load(src.read_text())
    ok = check(chain)
    out.mkdir(parents=True, exist_ok=True)
    stem = src.stem
    (out / f"{stem}.md").write_text(markdown(chain))
    (out / f"{stem}_report.md").write_text(report(chain))
    (out / f"{stem}_full.mmd").write_text(mermaid(chain))
    # Core view: thesis-level claims and what bears on them, without methods detail
    core_types = {"GAP", "HYPOTHESIS", "AIM", "QUESTION", "CLAIM", "LIMITATION", "ASSUMPTION"}
    core = {s["id"] for s in chain["statements"] if s["statement_type"] in core_types}
    (out / f"{stem}_core.mmd").write_text(mermaid(chain, core))
    (out / f"{stem}_summary.mmd").write_text(summary_mermaid(chain))
    score, counts, _ = logic_score(chain)
    coverage, n_obl = obligation_coverage(chain)
    dscore, differ = derived_score(chain)
    print(f"wrote {stem}.md, {stem}_report.md, {stem}_full.mmd, {stem}_core.mmd, {stem}_summary.mmd; "
          f"checks ok: {ok}; logic score: {fmt_score(score)} {counts}; "
          f"weighted: {fmt_score(weighted_logic_score(chain))}; derived: {fmt_score(dscore)} "
          f"({len(differ)} differ); obligations discharged: {fmt_score(coverage)} of {n_obl}"
          + thread_summary(chain))


if __name__ == "__main__":
    main()
