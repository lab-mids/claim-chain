"""Render a claim-chain argument-chain YAML into Markdown and Mermaid views,
compute the logic score, and write the three-part report (logic, limitations,
missing evidence).

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
    "BACKGROUND": "bg", "GAP": "bg", "HYPOTHESIS": "claim", "QUESTION": "q",
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
    "UNDERCUTS": "-.->", "CONTRADICTS": "-.->", "QUALIFIES": "-.->",
    "ALTERNATIVE_EXPLANATION_FOR": "-.->", "ANALOG_OF": "-.->", "CONDITIONALLY_SUPPORTS": "-.->",
}
SECTIONS = [
    ("Motivation", {"BACKGROUND", "GAP", "HYPOTHESIS"}),
    ("Concept", {"DEFINITION", "QUESTION"}),
    ("Methods and data", {"METHOD", "ASSUMPTION", "DATA"}),
    ("Observations", {"OBSERVATION"}),
    ("Claims", {"CLAIM"}),
    ("Limitations (stated by authors)", {"LIMITATION"}),
    ("Outlook", {"OUTLOOK"}),
]
# Draft weighting of verdicts for the logic score.
VALIDITY_SCORE = {"YES": 1.0, "PARTIAL": 0.5, "INCONCLUSIVE": 0.25, "NO": 0.0}
VALIDITY_MARK = {"YES": "✓", "PARTIAL": "◐", "INCONCLUSIVE": "?", "NO": "✗"}
MERMAID_MARK = {"YES": "✓", "PARTIAL": "(partial)", "INCONCLUSIVE": "?", "NO": "✗"}  # ◐ is missing from the default font
SCORED_TYPES = {"CLAIM", "HYPOTHESIS"}
SCORE_METHOD = ("mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, "
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


CRITERIA = ["grounded", "scope_matches", "inference_sound", "alternatives_excluded", "quantified", "consistent"]
CRITERION_SCORE = {"MET": 1.0, "PARTLY": 0.5, "NOT_MET": 0.0}


def criteria_score(crit):
    """Graded score of one claim from its rubric, and the verdict the rubric suggests."""
    vals = {k: crit.get(k) for k in CRITERIA if crit.get(k) and crit.get(k) != "NOT_APPLICABLE"}
    if not vals:
        return None, None
    score = sum(CRITERION_SCORE[v] for v in vals.values()) / len(vals)
    if vals.get("consistent") == "NOT_MET":
        verdict = "NO"
    elif vals.get("grounded") == "NOT_MET":
        verdict = "INCONCLUSIVE"
    elif all(v == "MET" for v in vals.values()):
        verdict = "YES"
    else:
        verdict = "PARTIAL"
    return score, verdict


def graded_score(chain):
    """Role-weighted mean of the rubric scores; None unless every assessed claim has criteria."""
    pairs = []
    for s in chain["statements"]:
        a = s.get("assessment")
        if s["statement_type"] not in SCORED_TYPES or not a:
            continue
        score, _ = criteria_score(a.get("criteria") or {})
        if score is None:
            return None
        pairs.append((ROLE_WEIGHT.get(s.get("claim_role"), 1.0), score))
    total = sum(w for w, _ in pairs)
    return sum(w * v for w, v in pairs) / total if total else None


def obligation_coverage(chain):
    status = [o["obligation_status"] for s in chain["statements"]
              for o in (s.get("assessment") or {}).get("proof_obligations", [])]
    return (sum(OBLIGATION_SCORE[x] for x in status) / len(status) if status else None), len(status)


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
                L.append(f"⚠ {label(c['concern_type'])}: {c['description']}  ")
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
        elif r["predicate"] in {"SUPPORTS", "MOTIVATES", "DEPENDS_ON"}:
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
    g = graded_score(chain)
    if g is not None:
        L.append(f"**Graded score (criteria rubric, draft): {g:.2f}**  ")
    L += ["", "| Statement | Role | Modality | Authors say | Verdict | Rubric | Rationale |", "|---|---|---|---|---|---|---|"]
    abbrev = {"MET": "✓", "PARTLY": "◐", "NOT_MET": "✗", "NOT_APPLICABLE": "–"}
    for s in sts:
        a = s.get("assessment")
        if s["statement_type"] in SCORED_TYPES and a:
            crit = a.get("criteria") or {}
            cs, cv = criteria_score(crit)
            rub = ("".join(abbrev.get(crit.get(k), "·") for k in CRITERIA) + f" {cs:.2f}"
                   + (f" (suggests {cv})" if cv != a["validity"] else "")) if cs is not None else "-"
            L.append(f"| **{short(s['id'])}** {s['text']} | {label(s.get('claim_role', '-'))} | "
                     f"{label(s.get('claim_modality', '-'))} | {label(s.get('author_certainty', '-'))} | "
                     f"{VALIDITY_MARK[a['validity']]} {a['validity']} | {rub} | {a['rationale']} |")
    if any((s.get("assessment") or {}).get("criteria") for s in sts):
        L.append("")
        L.append("Rubric order: grounded, scope matches, inference sound, alternatives excluded, quantified, "
                 "consistent (✓ met, ◐ partly, ✗ not met, – not applicable).")
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
            L.append(f"- **{short(s['id'])}** {label(c['concern_type'])}: {c['description']}")
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
    core_types = {"GAP", "HYPOTHESIS", "QUESTION", "CLAIM", "LIMITATION", "ASSUMPTION"}
    core = {s["id"] for s in chain["statements"] if s["statement_type"] in core_types}
    (out / f"{stem}_core.mmd").write_text(mermaid(chain, core))
    score, counts, _ = logic_score(chain)
    coverage, n_obl = obligation_coverage(chain)
    print(f"wrote {stem}.md, {stem}_report.md, {stem}_full.mmd, {stem}_core.mmd; checks ok: {ok}; "
          f"logic score: {fmt_score(score)} {counts}; weighted: {fmt_score(weighted_logic_score(chain))}; "
          f"obligations discharged: {fmt_score(coverage)} of {n_obl}"
          + (f"; graded: {graded_score(chain):.2f}" if graded_score(chain) is not None else ""))


if __name__ == "__main__":
    main()
