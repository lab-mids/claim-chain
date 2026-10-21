"""Render a claim-chain argument-chain YAML into Markdown and Mermaid views,
compute the logic score, and write the three-part report (logic, limitations,
missing evidence).

Usage: python scripts/render.py examples/<paper>/<paper>.yaml examples/<paper>/generated/
Also checks that every relation points to a known statement or entity.
"""
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
    "ALTERNATIVE_EXPLANATION_FOR": "-.->", "ANALOG_OF": "-.->",
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


def logic_score(chain):
    scored = [s for s in chain["statements"] if s["statement_type"] in SCORED_TYPES]
    verdicts = [s["assessment"]["validity"] for s in scored if s.get("assessment")]
    unassessed = [s["id"] for s in scored if not s.get("assessment")]
    score = sum(VALIDITY_SCORE[v] for v in verdicts) / len(verdicts) if verdicts else None
    counts = {v: verdicts.count(v) for v in VALIDITY_SCORE}
    return score, counts, unassessed


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
    return not bad


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
        L += [f"**Logic score: {score:.2f}** ({', '.join(f'{v} {k}' for k, v in counts.items())}). "
              f"Method: {SCORE_METHOD}.", ""]
    for title, types in SECTIONS:
        sts = [s for s in chain["statements"] if s["statement_type"] in types]
        if not sts:
            continue
        L += [f"## {title}", ""]
        for s in sts:
            hedge = " *(hedged)*" if s.get("hedged") else ""
            L.append(f"**{short(s['id'])}** `{s['statement_type']}` {s.get('section', '')}{hedge}  ")
            L.append(f"{s['text']}  ")
            if s["statement_type"] not in {"HYPOTHESIS", "QUESTION", "DEFINITION"}:
                L.append(f"Evidence: {evidence_str(s.get('evidence'))}  ")
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
            for c in s.get("concerns", []):
                L.append(f"⚠ {label(c['concern_type'])}: {c['description']}  ")
            a = s.get("assessment")
            if a:
                L.append(f"**Verdict: {VALIDITY_MARK[a['validity']]} {a['validity']}**. {a['rationale']}  ")
                for m in a.get("missing_evidence", []):
                    L.append(f"Missing: {m}  ")
                for o in a.get("proof_obligations", []):
                    by = ", ".join(short(x) for x in o.get("discharged_by", []))
                    L.append(f"Obligation ({label(o['obligation_status'])}): {o['text']}" + (f" ← {by}" if by else "") + "  ")
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
        if r["predicate"] in {"SUPPORTS", "MOTIVATES", "DEPENDS_ON"}:
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
    if pa.get("overall_validity"):
        L.append(f"**Overall: {VALIDITY_MARK[pa['overall_validity']]} {pa['overall_validity']}** · "
                 f"**Logic score: {score:.2f}**  ")
    L.append(f"Score method: {SCORE_METHOD}.  ")
    L.append(f"Verdicts: {', '.join(f'{v} {k}' for k, v in counts.items())}."
             + (f" Not yet assessed: {', '.join(short(u) for u in unassessed)}." if unassessed else ""))
    if pa.get("summary"):
        L += ["", pa["summary"]]
    L += ["", "| Statement | Modality | Verdict | Rationale |", "|---|---|---|---|"]
    for s in sts:
        a = s.get("assessment")
        if s["statement_type"] in SCORED_TYPES and a:
            L.append(f"| **{short(s['id'])}** {s['text']} | {label(s.get('claim_modality', '-'))} | "
                     f"{VALIDITY_MARK[a['validity']]} {a['validity']} | {a['rationale']} |")
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
                L.append(f"- **{short(s['id'])}** ({label(o['obligation_status'])}): {o['text']}"
                         + (f" (partly: {by})" if by else ""))
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
    print(f"wrote {stem}.md, {stem}_report.md, {stem}_full.mmd, {stem}_core.mmd; references ok: {ok}; "
          f"logic score: {score:.2f} {counts}")


if __name__ == "__main__":
    main()
