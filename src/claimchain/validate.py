"""Normalize, check and serialize ArgumentChain instances."""
from collections import Counter
from functools import lru_cache
from pathlib import Path

import yaml
from linkml.validator import validate

from claimchain.resources import schema_path

SCORED_TYPES = {"CLAIM", "HYPOTHESIS"}
TOP_LEVEL_ORDER = [
    "id", "schema_version", "annotator", "annotation_date", "publication",
    "entities", "cited_works", "statements", "relations", "paper_assessment",
]


@lru_cache(maxsize=None)
def schema_version(path: Path | None = None) -> str:
    schema = yaml.safe_load(Path(path or schema_path()).read_text(encoding="utf-8"))
    return str(schema["version"])


def normalize(chain: dict) -> dict:
    """Repair the YAML type slips that come up again and again (see the YAML rules in the prompt)."""
    pub = chain.get("publication") or {}
    for key in ("arxiv", "doi"):
        if key in pub and pub[key] is not None and not isinstance(pub[key], str):
            pub[key] = str(pub[key])

    def fix_validity(obj: dict, key: str) -> None:
        if isinstance(obj.get(key), bool):
            obj[key] = "YES" if obj[key] else "NO"

    for rel in chain.get("relations") or []:
        if rel.get("predicate") == "UNDERCUTS":  # renamed to WEAKENS
            rel["predicate"] = "WEAKENS"
    if isinstance(chain.get("paper_assessment"), dict):
        fix_validity(chain["paper_assessment"], "overall_validity")
    for st in chain.get("statements") or []:
        if isinstance(st.get("assessment"), dict):
            fix_validity(st["assessment"], "validity")
        for ev in st.get("evidence") or []:
            for val in ev.get("values") or []:
                if isinstance(val.get("value"), str):
                    try:
                        val["value"] = float(val["value"])
                    except ValueError:
                        pass  # left for the validator to report
    return chain


def check_consistency(chain: dict) -> list[str]:
    """Checks the schema cannot express: unique ids, known references, assessed claims."""
    issues = []
    statements = chain.get("statements") or []
    ids = [s.get("id") for s in statements] + [e.get("id") for e in chain.get("entities") or []]
    ids += [r.get("id") for r in chain.get("relations") or []]
    for dup, n in Counter(ids).items():
        if dup is not None and n > 1:
            issues.append(f"id {dup} is used {n} times; ids must be unique")

    known = {s.get("id") for s in statements} | {e.get("id") for e in chain.get("entities") or []}
    for rel in chain.get("relations") or []:
        for field in ("subject", "object"):
            if rel.get(field) not in known:
                issues.append(f"relation {rel.get('id')}: {field} {rel.get(field)} is not a defined statement or entity")
    for st in statements:
        for ob in (st.get("assessment") or {}).get("proof_obligations") or []:
            for ref in ob.get("discharged_by") or []:
                if ref not in known:
                    issues.append(f"statement {st.get('id')}: discharged_by {ref} is not a defined statement")
        if st.get("statement_type") in SCORED_TYPES and not st.get("assessment"):
            issues.append(f"statement {st.get('id')} ({st.get('statement_type')}) has no assessment")
    if not any(s.get("statement_type") in {"HYPOTHESIS", "AIM"} for s in statements):
        issues.append("no HYPOTHESIS or AIM statement: encode the paper's central thesis as a HYPOTHESIS, "
                      "or its stated aims as AIMs")
    if not chain.get("paper_assessment"):
        issues.append("paper_assessment is missing")
    return issues


def validate_chain(chain: dict, schema: Path | None = None) -> list[str]:
    """Return a list of problems; an empty list means the chain is valid."""
    report = validate(chain, str(schema or schema_path()), "ArgumentChain")
    issues = [r.message for r in report.results]
    return issues + check_consistency(chain)


def _flow(item: dict) -> str:
    return yaml.safe_dump(item, default_flow_style=True, sort_keys=False,
                          allow_unicode=True, width=10**6).strip()


def dump_chain(chain: dict) -> str:
    """Serialize in the house style: block-style statements, one flow-style line per entity and relation."""
    ordered = {k: chain[k] for k in TOP_LEVEL_ORDER if k in chain}
    ordered.update({k: v for k, v in chain.items() if k not in ordered})

    def block(data: dict) -> str:
        return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)

    parts = []
    for key, value in ordered.items():
        if key in ("entities", "relations") and isinstance(value, list):
            lines = "".join(f"  - {_flow(item)}\n" for item in value)
            parts.append(f"\n{key}:\n{lines}")
        elif key in ("statements", "paper_assessment"):
            parts.append("\n" + block({key: value}))
        else:
            parts.append(block({key: value}))
    return "".join(parts)
