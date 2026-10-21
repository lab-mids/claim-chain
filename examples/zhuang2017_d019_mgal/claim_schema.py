"""Pydantic data model for the paper claim/evidence YAML schema (schema_version 0.3).

The YAML stays plain data; this module defines its structure::

    from claim_schema import ClaimDocument
    doc = ClaimDocument.from_yaml(text)       # raises pydantic.ValidationError on bad structure
    doc.claims[0].evidence[0].data
    ClaimDocument.model_json_schema()          # JSON Schema, e.g. for editors or LLM prompts

Structural rules (types, required fields, allowed values) are enforced here.
Cross-references between ids are checked softly by ``claim_graph.ClaimGraph.check``,
so a draft with a dangling id still loads.

Every model allows extra fields, so the format can grow without breaking old
code; ``unknown_fields()`` lists them so typos stay visible.
"""

import json
import re
from typing import Any, Literal, Optional, Union

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Strength = Literal["strong", "moderate", "weak"]

ClaimType = Literal[
    "main_conclusion",
    "intermediate_claim",
    "quantitative_support",
    "mechanistic_interpretation",
    "methodological_conclusion",
    "counter_claim",
]

KNOWN_SECTIONS = ("paper", "references", "claims", "hypotheses", "open_questions", "relations")


class SchemaModel(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    def unknown_fields(self, path=""):
        """Yield ``(path, field)`` for every field not declared in the schema, recursively."""
        here = path or type(self).__name__
        for name in self.model_extra or {}:
            yield here, name
        for name in type(self).model_fields:
            value = getattr(self, name)
            items = value if isinstance(value, list) else [value]
            for i, item in enumerate(items):
                if isinstance(item, SchemaModel):
                    sub = f"{here}.{name}" + (f"[{i}]" if isinstance(value, list) else "")
                    if getattr(item, "id", None):
                        sub = f"{item.id}"
                    yield from item.unknown_fields(sub)


def _listify(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


IdList = list[str]


class _IdListMixin:
    """Accept a single id or a list of ids, and coerce numbers such as ``1.1`` to strings."""

    @field_validator("*", mode="before")
    @classmethod
    def _coerce_id_lists(cls, value, info):
        field = cls.model_fields.get(info.field_name)
        if field is not None and field.annotation == IdList:
            return [str(v) for v in _listify(value)]
        return value


# ---------------------------------------------------------------------------
# bibliographic
# ---------------------------------------------------------------------------


class Paper(SchemaModel):
    id: str
    title: str
    authors: list[str] = Field(default_factory=list)
    journal: Optional[str] = None
    volume: Optional[Union[int, str]] = None
    article: Optional[str] = None
    pages: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None


class Reference(SchemaModel):
    id: str
    paper_reference: Optional[int] = Field(None, description="Number of the entry in the paper's bibliography.")
    authors: list[str] = Field(default_factory=list)
    year: Optional[int] = None
    title: Optional[str] = None
    journal: Optional[str] = None
    publisher: Optional[str] = None
    volume: Optional[Union[int, str]] = None
    pages: Optional[str] = None
    article: Optional[str] = None
    page: Optional[str] = None
    type: Optional[str] = Field(None, description="e.g. 'book'; journal article when omitted.")
    roles: list[str] = Field(default_factory=list, description="Why the argument cites it.")
    note: Optional[str] = None

    @field_validator("pages", "article", "page", mode="before")
    @classmethod
    def _str(cls, v):
        return None if v is None else str(v)

    @property
    def short_label(self):
        if not self.authors:
            return f"ref. [{self.paper_reference if self.paper_reference is not None else '?'}]"
        et_al = " et al." if len(self.authors) > 1 else ""
        return f"{self.authors[0].split()[-1]}{et_al} {self.year or ''}".strip()

    @property
    def citation(self):
        venue = self.journal or self.publisher
        parts = [venue, self.volume, self.pages or self.article or self.page]
        return ", ".join(str(p) for p in parts if p)


# ---------------------------------------------------------------------------
# shared building blocks
# ---------------------------------------------------------------------------


class Source(SchemaModel):
    """Where in the paper something is stated or shown."""

    section: Optional[str] = None
    page: Optional[int] = None
    figure: Optional[Union[int, str]] = None
    table: Optional[Union[int, str]] = None

    def __str__(self):
        return ", ".join(f"{k} {v}" for k, v in self.model_dump(exclude_none=True).items())


class PaperStatement(SchemaModel):
    paraphrase: str
    source: Optional[Source] = None


class EpistemicStatus(SchemaModel):
    author_certainty: Optional[str] = Field(None, description="e.g. predicted, speculation, demonstrated")
    reviewer_assessment: Optional[Strength] = None
    evidence_strength: Optional[Strength] = None
    validation_status: Optional[str] = Field(None, description="e.g. unvalidated, validated")
    reason: Optional[str] = None

    @property
    def assessment(self):
        return self.reviewer_assessment or self.evidence_strength


class ExternalSupport(SchemaModel):
    reference: str
    relation: str = "supports_inference"


class ChainStep(SchemaModel):
    step: Optional[int] = None
    from_: str = Field(alias="from")
    to: str
    external_support: list[ExternalSupport] = Field(default_factory=list)
    strength: Optional[Strength] = None


class Inference(SchemaModel):
    rule: Optional[str] = None
    type: Optional[str] = Field(None, description="e.g. empirical_correlation")
    scope: Optional[str] = None
    strength: Optional[Strength] = None
    overall_strength: Optional[Strength] = None
    external_support: list[ExternalSupport] = Field(default_factory=list)
    chain: list[ChainStep] = Field(default_factory=list)
    caveat: Optional[str] = None

    @property
    def effective_strength(self):
        return self.strength or self.overall_strength

    @model_validator(mode="after")
    def _has_rule_or_chain(self):
        if not self.rule and not self.chain:
            raise ValueError("an inference needs a `rule` or a `chain`")
        return self


class Reaction(SchemaModel):
    expression: str


# ---------------------------------------------------------------------------
# argument nodes
# ---------------------------------------------------------------------------


class Evidence(SchemaModel, _IdListMixin):
    id: str
    origin: Optional[Literal["internal", "external"]] = None
    type: Optional[str] = Field(None, description="e.g. figure, table, calculated_data, experimental_validation")
    method: Optional[Union[str, dict[str, str]]] = None
    source: Optional[Source] = None
    quantity: Optional[str] = None
    quantities: list[str] = Field(default_factory=list)
    unit: Optional[str] = None
    reaction: Optional[Reaction] = None
    reference: Optional[str] = Field(None, description="Single external reference id.")
    references: IdList = Field(default_factory=list, description="Several external reference ids.")
    data: Optional[dict[str, Any]] = None
    derived: Optional[dict[str, Any]] = None
    statement: Optional[str] = None
    observation: Optional[str] = None
    interpretation: Optional[str] = None
    role: Optional[str] = None

    @field_validator("reaction", mode="before")
    @classmethod
    def _reaction(cls, v):
        return {"expression": v} if isinstance(v, str) else v

    @property
    def cited_references(self):
        return ([self.reference] if self.reference else []) + list(self.references)

    @property
    def method_label(self):
        if isinstance(self.method, dict):
            return " + ".join(self.method.values())
        return self.method

    @model_validator(mode="after")
    def _external_needs_reference(self):
        if self.origin == "external" and not self.cited_references:
            raise ValueError(f"evidence {self.id} has origin 'external' but cites no `reference(s)`")
        return self


class Assumption(SchemaModel):
    id: str
    statement: str


class OpenObligation(SchemaModel):
    """Evidence that is missing for a claim or hypothesis (``missing_evidence``)."""

    id: str
    type: Optional[str] = "open_proof_obligation"
    statement: str
    desired_data: list[str] = Field(default_factory=list)
    desired_units: dict[str, str] = Field(default_factory=dict)
    desired_quantity: Optional[dict[str, Any]] = None


class Basis(SchemaModel):
    origin: Optional[Literal["internal", "external"]] = None
    type: Optional[str] = None
    statement: Optional[str] = None


class ArgumentNode(SchemaModel, _IdListMixin):
    """Fields shared by claims and hypotheses, including the inline relation fields."""

    id: str
    statement: str
    paper_statement: Optional[PaperStatement] = None
    epistemic_status: Optional[EpistemicStatus] = None

    evidence: list[Evidence] = Field(default_factory=list)
    inference: Optional[Inference] = None
    assumptions: list[Assumption] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    caveat: Optional[str] = None
    missing_evidence: list[OpenObligation] = Field(default_factory=list)

    # inline relations (all lists of node ids)
    supports: IdList = Field(default_factory=list)
    supported_by: IdList = Field(default_factory=list)
    challenges: IdList = Field(default_factory=list)
    challenged_by: IdList = Field(default_factory=list)
    motivates: IdList = Field(default_factory=list)
    leads_to: IdList = Field(default_factory=list)
    supports_if_validated: IdList = Field(default_factory=list)
    depends_on_hypotheses: IdList = Field(default_factory=list)
    mechanistic_support: IdList = Field(default_factory=list)

    @field_validator("limitations", mode="before")
    @classmethod
    def _limitations(cls, v):
        return _listify(v)

    @property
    def strength(self):
        return self.inference.effective_strength if self.inference else None


class Claim(ArgumentNode):
    type: ClaimType


class Hypothesis(ArgumentNode):
    type: str = "hypothesis"
    basis: Optional[Basis] = None
    quantitative_evidence: Optional[Any] = None

    @field_validator("type")
    @classmethod
    def _is_hypothesis(cls, v):
        if "hypothesis" not in v:
            raise ValueError(f"type {v!r} under `hypotheses` must contain 'hypothesis'; claims belong under `claims`")
        return v


class OpenQuestion(SchemaModel, _IdListMixin):
    id: str
    statement: str
    motivated_by: IdList = Field(default_factory=list)
    importance: Optional[Literal["critical", "high", "medium", "low"]] = None
    reason: Optional[str] = None
    desired_evidence: list[str] = Field(default_factory=list)


class Relation(SchemaModel):
    source: str
    target: str
    relation: str

    @field_validator("source", "target", mode="before")
    @classmethod
    def _str(cls, v):
        return str(v)


# ---------------------------------------------------------------------------
# document
# ---------------------------------------------------------------------------


class ClaimDocument(SchemaModel):
    schema_version: str
    paper: Paper
    references: list[Reference] = Field(default_factory=list)
    claims: list[Claim] = Field(default_factory=list)
    hypotheses: list[Hypothesis] = Field(default_factory=list)
    open_questions: list[OpenQuestion] = Field(default_factory=list)
    relations: list[Relation] = Field(default_factory=list)

    # filled while loading: top-level key under which each claim was written
    sections: dict[str, str] = Field(default_factory=dict, exclude=True)

    @model_validator(mode="before")
    @classmethod
    def _fold_extra_claim_lists(cls, data):
        """Keys such as ``claims_continued`` hold more claims: merge them into ``claims``."""
        if not isinstance(data, dict):
            return data
        data = dict(data)
        sections = {}
        claims = list(data.get("claims") or [])
        for item in claims:
            if isinstance(item, dict) and "id" in item:
                sections[str(item["id"])] = "claims"
        for key in list(data):
            value = data[key]
            if key in KNOWN_SECTIONS or not isinstance(value, list):
                continue
            if value and all(isinstance(x, dict) and "id" in x and "statement" in x for x in value):
                for item in value:
                    sections[str(item["id"])] = key
                claims += value
                del data[key]
        for key in ("hypotheses", "open_questions", "references"):
            for item in data.get(key) or []:
                if isinstance(item, dict) and "id" in item:
                    sections.setdefault(str(item["id"]), key)
        data["claims"] = claims
        data["sections"] = sections
        return data

    @field_validator("schema_version", mode="before")
    @classmethod
    def _version(cls, v):
        return str(v)

    # ---------------- loading ----------------

    @classmethod
    def from_yaml(cls, text):
        return cls.model_validate(yaml.safe_load(text))

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            return cls.from_yaml(f.read())

    @classmethod
    def from_notebook(cls, path, cell=None):
        """Load the first ```yaml fenced block found in a notebook's markdown cells (saved file)."""
        with open(path) as f:
            nb = json.load(f)
        cells = nb["cells"] if cell is None else [nb["cells"][cell]]
        for c in cells:
            m = re.search(r"```ya?ml\s*\n(.*?)```", "".join(c["source"]), re.S | re.I)
            if m:
                return cls.from_yaml(m.group(1))
        raise ValueError(f"No ```yaml block found in {path}")

    def to_yaml(self):
        return yaml.safe_dump(self.model_dump(mode="json", exclude_none=True, exclude_defaults=True, by_alias=True),
                              sort_keys=False, allow_unicode=True, width=88)

    # ---------------- convenience ----------------

    @property
    def argument_nodes(self):
        return [*self.claims, *self.hypotheses]

    def find(self, node_id):
        """Return any element (claim, hypothesis, evidence, reference, ...) by id."""
        for item in self.iter_elements():
            if item.id == node_id:
                return item
        raise KeyError(node_id)

    def iter_elements(self):
        yield from self.references
        for n in self.argument_nodes:
            yield n
            yield from n.evidence
            yield from n.assumptions
            yield from n.missing_evidence
        yield from self.open_questions
