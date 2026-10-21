"""Visualize claim/evidence argument graphs defined by ``claim_schema.ClaimDocument``.

Typical use in a notebook::

    import claim_graph as cg
    g = cg.ClaimGraph.from_notebook("mgal-d0-19-structure.ipynb")
    g.doc                    # the validated pydantic ClaimDocument
    g.to_graphviz()          # static SVG with hover tooltips
    g.explore()              # ipywidgets controls (toggle layers, focus a node)
    g.show_mermaid()         # Mermaid flowchart (JupyterLab >= 4.1)
    g.describe("C1.3")       # Markdown summary of one node
    g.check()                # cross-reference consistency report
"""

import json
import re
import textwrap
import urllib.parse
from collections import defaultdict, deque
from dataclasses import dataclass, field

import yaml

from claim_schema import (
    ArgumentNode,
    Assumption,
    Claim,
    ClaimDocument,
    Evidence,
    Hypothesis,
    OpenObligation,
    OpenQuestion,
    Reference,
)

# ---------------------------------------------------------------------------
# text formatting
# ---------------------------------------------------------------------------

_SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
_ELEMENTS = "Mg|Al|Ni|Sn|Cd|Li|Ca|Si|Zn|Cu|Fe|Ti"
_FORMULA = re.compile(rf"(?:{_ELEMENTS})\d*(?:(?:{_ELEMENTS})\d*)+")
_STRUKTUR = re.compile(r"\b([A-Z]\d)_(\d+)")


def fmt(text):
    """D0_19 -> D0₁₉, Mg17Al12 -> Mg₁₇Al₁₂, collapse whitespace."""
    s = " ".join(str(text).split())
    s = _STRUKTUR.sub(lambda m: m.group(1) + m.group(2).translate(_SUB), s)
    return _FORMULA.sub(lambda m: m.group(0).translate(_SUB), s)


def _html(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def _html_sub(text):
    """Escape for graphviz HTML labels and render subscripts with <sub>."""
    s = _html(" ".join(str(text).split()))
    s = _STRUKTUR.sub(lambda m: f"{m.group(1)}<sub>{m.group(2)}</sub>", s)
    return _FORMULA.sub(lambda m: re.sub(r"(\d+)", r"<sub>\1</sub>", m.group(0)), s)


def _wrap_plain(text, width, max_lines):
    """Wrap without converting subscripts (line lengths match the rendered text closely)."""
    lines = textwrap.wrap(" ".join(str(text).split()), width) or [""]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rsplit(" ", 1)[0] + " …"
    return lines


def _wrap(text, width, max_lines):
    return [fmt(line) for line in _wrap_plain(text, width, max_lines)]


def _words(s):
    return str(s).replace("_", " ")


# ---------------------------------------------------------------------------
# drawing vocabulary
# ---------------------------------------------------------------------------

NODE_STYLE = {
    "main_conclusion": dict(shape="box", style="rounded,filled", fillcolor="#14212a", fontcolor="#ffffff", color="#14212a"),
    "intermediate_claim": dict(shape="box", style="rounded,filled", fillcolor="#ffffff", color="#5a6a75"),
    "quantitative_support": dict(shape="box", style="rounded,filled", fillcolor="#ffffff", color="#5a6a75"),
    "mechanistic_interpretation": dict(shape="box", style="rounded,filled", fillcolor="#ffffff", color="#5a6a75"),
    "methodological_conclusion": dict(shape="box", style="rounded,filled", fillcolor="#eef3f6", color="#5a6a75"),
    "counter_claim": dict(shape="box", style="rounded,filled", fillcolor="#fff4f2", color="#b23a2f", penwidth="1.8"),
    "hypothesis": dict(shape="box", style="rounded,dashed,filled", fillcolor="#fff8ec", color="#a8700f", penwidth="1.6"),
    "open_question": dict(shape="note", style="filled", fillcolor="#fff8ec", color="#a8700f"),
    "evidence": dict(shape="box", style="filled", fillcolor="#e6edf0", color="#e6edf0", fontsize="10"),
    "assumption": dict(shape="box", style="filled,dashed", fillcolor="#f3f0f7", color="#7a6a8f", fontsize="10"),
    "reference": dict(shape="tab", style="filled", fillcolor="#e9f1fb", color="#3b6ea8", fontsize="10"),
}

EDGE_STYLE = {
    "supports": dict(color="#2c7a4c"),
    "mechanistic": dict(color="#2c7a4c", style="dotted"),
    "challenges": dict(color="#b23a2f", arrowhead="tee", penwidth="2.2"),
    "conditional": dict(color="#a8700f", style="dashed"),
    "motivates": dict(color="#7d8b94", style="dashed"),
    "required_to_validate": dict(color="#a8700f", style="dotted", arrowhead="odot"),
    "raises": dict(color="#a8700f", style="dotted", arrowhead="vee"),
    "evidence": dict(color="#8a99a3", arrowsize="0.6"),
    "assumption": dict(color="#7a6a8f", style="dotted", arrowsize="0.6"),
    "rule": dict(color="#3b6ea8", style="dashed", arrowhead="diamond", arrowsize="0.7"),
    "validates": dict(color="#3b6ea8", style="dotted", arrowhead="odiamond", arrowsize="0.7"),
    "background": dict(color="#3b6ea8", style="dotted", arrowsize="0.6"),
}
EDGE_LABEL = {
    "supports": "supports", "mechanistic": "mechanistically supports", "challenges": "challenges",
    "conditional": "supports if validated", "motivates": "motivates", "required_to_validate": "required to validate",
    "raises": "raises open question", "evidence": "evidence for", "assumption": "assumed by",
    "rule": "establishes inference rule", "validates": "validates baseline", "background": "background",
}

# relation names in `relations:` and `external_support.relation` -> drawn edge kind
RELATION_ALIASES = {
    "supports": "supports",
    "challenges": "challenges",
    "motivates": "motivates",
    "motivates_validation": "motivates",
    "conditionally_supports": "conditional",
    "supports_if_validated": "conditional",
    "mechanistically_supports": "mechanistic",
    "required_to_validate": "required_to_validate",
    "establishes_inference_rule": "rule",
    "establishes_APB_dislocation_relation": "rule",
    "supports_inference": "rule",
    "validates_baseline": "validates",
    "validates_reference": "validates",
    "provides_background": "background",
}

# inline relation fields of ArgumentNode / OpenQuestion: field -> (direction, kind)
INLINE_FIELDS = {
    "supported_by": ("rev", "supports"),
    "supports": ("fwd", "supports"),
    "challenged_by": ("rev", "challenges"),
    "challenges": ("fwd", "challenges"),
    "motivates": ("fwd", "motivates"),
    "leads_to": ("fwd", "motivates"),
    "supports_if_validated": ("fwd", "conditional"),
    "depends_on_hypotheses": ("rev", "conditional"),
    "mechanistic_support": ("rev", "mechanistic"),
    "motivated_by": ("rev", "raises"),
}

STRENGTH_WIDTH = {"strong": 3.0, "moderate": 2.0, "weak": 1.0}


def _canonical(relation):
    return RELATION_ALIASES.get(relation, relation)


def _kind_of(obj):
    if isinstance(obj, Reference):
        return "reference"
    if isinstance(obj, Evidence):
        return "evidence"
    if isinstance(obj, Assumption):
        return "assumption"
    if isinstance(obj, (OpenQuestion, OpenObligation)):
        return "open_question"
    if isinstance(obj, Hypothesis):
        return "hypothesis"
    return obj.type


# ---------------------------------------------------------------------------
# graph model
# ---------------------------------------------------------------------------


@dataclass
class Node:
    id: str
    obj: object  # a claim_schema model instance
    parent: str = None

    @property
    def kind(self):
        return _kind_of(self.obj)

    @property
    def label_text(self):
        o = self.obj
        if isinstance(o, Reference):
            return o.short_label
        if isinstance(o, Evidence):
            bits = [o.type, o.method_label, o.quantity]
            return " · ".join(_words(b) for b in bits if b) or o.statement or ""
        return o.statement

    @property
    def strength(self):
        return self.obj.strength if isinstance(self.obj, ArgumentNode) else None


@dataclass
class Edge:
    source: str
    target: str
    kind: str
    origin: set = field(default_factory=set)  # {"inline", "relations"}


@dataclass
class Issue:
    level: str  # error | warning | note
    message: str


class ClaimGraph:
    def __init__(self, doc: ClaimDocument):
        self.doc = doc
        self.nodes = {}
        self.edges = {}
        self.issues = []
        self._build()

    @classmethod
    def from_yaml(cls, text):
        return cls(ClaimDocument.from_yaml(text))

    @classmethod
    def from_file(cls, path):
        return cls(ClaimDocument.from_file(path))

    @classmethod
    def from_notebook(cls, path, cell=None):
        """Read the first ```yaml block of the saved notebook and validate it."""
        return cls(ClaimDocument.from_notebook(path, cell))

    # ---------------- building ----------------

    def _issue(self, level, message):
        self.issues.append(Issue(level, message))

    def _add_node(self, obj, where, parent=None):
        if obj.id in self.nodes:
            old = self.nodes[obj.id]
            same = fmt(getattr(old.obj, "statement", "") or "") == fmt(getattr(obj, "statement", "") or "")
            self._issue("warning", f"`{obj.id}` is defined twice ({self._where(old)} and {where})"
                        + ("" if same else " with different statements")
                        + "; the first definition is drawn and both sets of relations are kept.")
            return old
        node = Node(obj.id, obj, parent)
        node.where = where
        self.nodes[obj.id] = node
        return node

    @staticmethod
    def _where(node):
        return getattr(node, "where", "?")

    def _add_edge(self, source, target, kind, origin):
        key = (source, target, kind)
        if key not in self.edges:
            self.edges[key] = Edge(source, target, kind)
        self.edges[key].origin.add(origin)

    def _build(self):
        doc = self.doc
        ref_ids = {r.id for r in doc.references}
        pending = []  # (source_id, field, target_id)

        for ref in doc.references:
            self._add_node(ref, "references")
        for n in doc.argument_nodes:
            self._add_node(n, doc.sections.get(n.id, "claims"))
            for ev in n.evidence:
                self._add_node(ev, f"{n.id}.evidence", parent=n.id)
                self._add_edge(ev.id, n.id, "evidence", "inline")
                for ref in ev.cited_references:
                    if ref in ref_ids:
                        self._add_edge(ref, ev.id, "validates", "inline")
                    else:
                        self._issue("error", f"Evidence `{ev.id}` cites `{ref}`, which is not in `references`.")
            for a in n.assumptions:
                self._add_node(a, f"{n.id}.assumptions", parent=n.id)
                self._add_edge(a.id, n.id, "assumption", "inline")
            for ob in n.missing_evidence:
                self._add_node(ob, f"{n.id}.missing_evidence", parent=n.id)
                self._add_edge(ob.id, n.id, "required_to_validate", "inline")
            if n.inference:
                supports = [(s, f"{n.id}.inference") for s in n.inference.external_support]
                supports += [(s, f"{n.id}.inference.chain[{st.step}]") for st in n.inference.chain for s in st.external_support]
                for s, where in supports:
                    if s.reference in ref_ids:
                        self._add_edge(s.reference, n.id, _canonical(s.relation), "inline")
                    else:
                        self._issue("error", f"`{where}` cites `{s.reference}`, which is not in `references`.")
            for fld in INLINE_FIELDS:
                for target in getattr(n, fld, []):
                    pending.append((n.id, fld, target))
        for q in doc.open_questions:
            self._add_node(q, "open_questions")
            pending += [(q.id, "motivated_by", t) for t in q.motivated_by]

        for src, fld, target in pending:
            if target not in self.nodes:
                self._issue("error", f"`{src}.{fld}` points to `{target}`, which is not defined.")
                continue
            direction, kind = INLINE_FIELDS[fld]
            a, b = (src, target) if direction == "fwd" else (target, src)
            self._add_edge(a, b, kind, "inline")

        for i, rel in enumerate(doc.relations):
            missing = [x for x in (rel.source, rel.target) if x not in self.nodes]
            if missing:
                self._issue("error", f"`relations[{i}]` ({rel.source} → {rel.target}) refers to undefined "
                            + ", ".join(f"`{m}`" for m in missing) + ".")
                continue
            kind = _canonical(rel.relation)
            if kind not in EDGE_STYLE:
                self._issue("note", f"`relations[{i}]` uses relation `{rel.relation}`, which has no drawing style.")
            self._add_edge(rel.source, rel.target, kind, "relations")

        self._check()

    # ---------------- checks ----------------

    def _check(self):
        doc = self.doc
        extra_sections = sorted({s for s in doc.sections.values() if s not in ("claims", "hypotheses", "open_questions", "references")})
        for s in extra_sections:
            ids = [i for i, sec in doc.sections.items() if sec == s]
            self._issue("note", f"`{s}:` is not a schema key; its {len(ids)} claims ({', '.join(f'`{i}`' for i in ids)}) "
                        "were merged into `claims`.")
        for where, name in doc.unknown_fields():
            self._issue("note", f"`{where}` has field `{name}`, which the schema does not define.")

        for n in self.nodes.values():
            if n.kind in ("reference", "evidence", "assumption") or n.parent:
                continue
            if not any(e.kind not in ("evidence", "assumption") and n.id in (e.source, e.target) for e in self.edges.values()):
                self._issue("warning", f"`{n.id}` is not linked to any claim, hypothesis or question.")
        cited = {e.source for e in self.edges.values()}
        for r in doc.references:
            if r.id not in cited:
                self._issue("note", f"Reference `{r.id}` is listed but never cited.")

        if doc.relations:
            only_inline, only_explicit = [], []
            for e in self.edges.values():
                if e.kind in ("evidence", "assumption"):
                    continue
                if e.origin == {"inline"}:
                    parent = self.nodes[e.target].parent
                    if not (parent and (e.source, parent, e.kind) in self.edges):
                        only_inline.append(e)
                elif e.origin == {"relations"}:
                    if not any(x.source == e.source and self.nodes[x.target].parent == e.target and x.kind == e.kind
                               for x in self.edges.values()):
                        only_explicit.append(e)
            fmt_edges = lambda es: ", ".join(f"`{e.source} → {e.target}` ({EDGE_LABEL.get(e.kind, e.kind)})" for e in es)
            if only_inline:
                self._issue("note", "In the item fields but missing from `relations:`: " + fmt_edges(only_inline) + ".")
            if only_explicit:
                self._issue("note", "Only in `relations:`, not in the item fields: " + fmt_edges(only_explicit) + ".")

    def check(self):
        """Display the consistency report as Markdown."""
        from IPython.display import Markdown

        order = {"error": 0, "warning": 1, "note": 2}
        rows = sorted(self.issues, key=lambda i: order[i.level])
        if not rows:
            return Markdown("No issues: every reference resolves and every claim is connected.")
        counts = {lvl: sum(i.level == lvl for i in rows) for lvl in order}
        head = f"**{counts['error']} errors · {counts['warning']} warnings · {counts['note']} notes**\n\n"
        return Markdown(head + "\n".join(f"- **{i.level}**: {i.message}" for i in rows))

    def summary(self):
        counts = defaultdict(int)
        for n in self.nodes.values():
            counts[n.kind] += 1
        return dict(counts) | {"relations": len(self.edges)}

    # ---------------- view selection ----------------

    def _view(self, evidence=True, references=True, open_questions=True, assumptions=True, focus=None, depth=1):
        hidden = {k for k, show in (("evidence", evidence), ("reference", references),
                                    ("open_question", open_questions), ("assumption", assumptions)) if not show}

        def rep(nid):
            """Visible representative: hidden evidence collapses into its claim."""
            n = self.nodes[nid]
            if n.kind == "evidence" and "evidence" in hidden:
                return n.parent
            return None if n.kind in hidden else nid

        edges = {}
        for e in self.edges.values():
            s, t = rep(e.source), rep(e.target)
            if s is None or t is None or s == t:
                continue
            edges.setdefault((s, t, e.kind), Edge(s, t, e.kind, set(e.origin)))
        for key in list(edges):
            s, t, k = key
            # with evidence visible, drop ref -> claim edges duplicated by ref -> evidence-of-claim
            if any(s2 == s and k2 == k and self.nodes[t2].parent == t for (s2, t2, k2) in edges):
                del edges[key]
            # a more specific relation for the same pair replaces a plain "supports"
            elif k == "supports" and any((s, t, k2) in edges for k2 in ("mechanistic", "conditional")):
                del edges[key]
            # "X raises O" is redundant when O is already "required to validate" X
            elif k == "raises" and (t, s, "required_to_validate") in edges:
                del edges[key]

        visible = {nid for nid in self.nodes if rep(nid) == nid}
        if focus:
            if focus not in self.nodes:
                raise KeyError(f"Unknown node id {focus!r}")
            adj = defaultdict(set)
            for s, t, _ in edges:
                adj[s].add(t)
                adj[t].add(s)
            keep, queue = {focus}, deque([(focus, 0)])
            while queue:
                nid, d = queue.popleft()
                if d < depth:
                    for nb in adj[nid] - keep:
                        keep.add(nb)
                        queue.append((nb, d + 1))
            visible &= keep
            edges = {k: e for k, e in edges.items() if e.source in visible and e.target in visible}
        return visible, list(edges.values())

    def _tooltip(self, n):
        o = n.obj
        parts = [f"{n.id} [{_words(n.kind)}]"]
        if isinstance(o, Reference):
            parts += [fmt(o.title or o.note or ""), o.citation]
            if o.roles:
                parts.append("roles: " + ", ".join(_words(x) for x in o.roles))
            return "\n".join(p for p in parts if p)
        if getattr(o, "statement", None):
            parts.append(fmt(o.statement))
        if isinstance(o, ArgumentNode):
            if o.epistemic_status:
                es = o.epistemic_status.model_dump(exclude_none=True, exclude={"reason"})
                parts.append("status: " + ", ".join(f"{_words(k)}={v}" for k, v in es.items()))
            if o.inference and o.inference.rule:
                parts.append(f"inference ({o.strength}): {fmt(o.inference.rule)}")
            parts += ["limitation: " + fmt(lim) for lim in o.limitations]
        if isinstance(o, Evidence):
            if o.observation:
                parts.append(fmt(o.observation))
            if o.data:
                parts.append("data: " + fmt(json.dumps(o.data, ensure_ascii=False))[:400])
        if isinstance(o, OpenQuestion) and o.reason:
            parts.append(fmt(o.reason))
        return "\n".join(p for p in parts if p)

    def _badge(self, n):
        o = n.obj
        tags = []
        if isinstance(o, ArgumentNode) and o.epistemic_status:
            tags += [o.epistemic_status.assessment, o.epistemic_status.validation_status]
        if isinstance(o, OpenQuestion):
            tags.append(o.importance)
        if n.kind not in ("main_conclusion", "hypothesis") and n.strength:
            tags.append(f"inference: {n.strength}")
        return " · ".join(str(t) for t in tags if t)

    # ---------------- graphviz ----------------

    def to_graphviz(self, evidence=False, references=True, open_questions=True, assumptions=True,
                    focus=None, depth=1, rankdir="LR", width=34):
        """Return a graphviz.Digraph; it renders as SVG in Jupyter (hover for details)."""
        import graphviz

        visible, edges = self._view(evidence, references, open_questions, assumptions, focus, depth)
        g = graphviz.Digraph("claims", engine="dot")
        g.attr(rankdir=rankdir, nodesep="0.18", ranksep="0.55", fontname="Helvetica", bgcolor="transparent", newrank="true")
        g.attr("node", fontname="Helvetica", fontsize="11", margin="0.12,0.06", color="#5a6a75")
        g.attr("edge", fontname="Helvetica", fontsize="9", arrowsize="0.8", penwidth="1.4")

        def add(gr, n):
            style = dict(NODE_STYLE.get(n.kind, NODE_STYLE["intermediate_claim"]))
            small = n.kind in ("evidence", "reference", "assumption")
            lines = _wrap_plain(n.label_text, 28 if small else width, 3 if small else 5)
            muted = "#c9d3d9" if n.kind == "main_conclusion" else "#5a6a75"
            badge = self._badge(n)
            label = (
                f"<<b>{_html(n.id)}</b>"
                + (f'  <font point-size="8" color="{muted}">{_html(badge)}</font>' if badge else "")
                + "".join(f'<br align="left"/>{_html_sub(l)}' for l in lines)
                + '<br align="left"/>>'
            )
            attrs = dict(style, label=label, tooltip=self._tooltip(n), fontcolor=style.get("fontcolor", "#14212a"))
            if isinstance(n.obj, Reference):
                attrs["URL"] = "https://scholar.google.com/scholar?q=" + urllib.parse.quote(fmt(n.obj.title or n.label_text))
                attrs["target"] = "_blank"
            gr.node(n.id, **attrs)

        refs = sorted((self.nodes[i] for i in visible if self.nodes[i].kind == "reference"), key=lambda n: n.id)
        if refs:
            with g.subgraph(name="cluster_refs") as c:
                c.attr(label="External literature", fontsize="10", fontcolor="#3b6ea8", color="#c5d6ea",
                       style="rounded,dashed", tooltip="References cited by the argument")
                for n in refs:
                    add(c, n)
        for nid in sorted(visible):
            if self.nodes[nid].kind != "reference":
                add(g, self.nodes[nid])

        for e in edges:
            attrs = dict(EDGE_STYLE.get(e.kind, {}))
            if e.kind in ("supports", "evidence", "mechanistic"):
                # line width encodes the strength of the inference the claim makes
                holder = self.nodes[e.target] if e.kind == "evidence" else self.nodes[e.source]
                if holder.strength in STRENGTH_WIDTH:
                    attrs["penwidth"] = str(STRENGTH_WIDTH[holder.strength] * (0.6 if e.kind == "evidence" else 1))
            attrs["tooltip"] = f"{e.source} {EDGE_LABEL.get(e.kind, e.kind)} {e.target}  [{'/'.join(sorted(e.origin))}]"
            if e.kind in ("challenges", "conditional"):
                attrs["label"] = EDGE_LABEL[e.kind]
                attrs["fontcolor"] = attrs.get("color", "#5a6a75")
            g.edge(e.source, e.target, **attrs)
        return g

    def legend(self):
        """A small graphviz legend of node and edge styles."""
        import graphviz

        g = graphviz.Digraph("legend")
        g.attr(rankdir="LR", nodesep="0.1", ranksep="0.3", bgcolor="transparent")
        g.attr("node", fontname="Helvetica", fontsize="9")
        g.attr("edge", fontname="Helvetica", fontsize="8")
        kinds = ["main_conclusion", "intermediate_claim", "methodological_conclusion", "counter_claim",
                 "hypothesis", "open_question", "evidence", "assumption", "reference"]
        with g.subgraph(name="cluster_n") as c:
            c.attr(label="nodes", fontsize="9", color="#d3dce1")
            for i, k in enumerate(kinds):
                c.node(f"n{i}", _words(k), **NODE_STYLE[k])
            for i in range(len(kinds) - 1):
                c.edge(f"n{i}", f"n{i + 1}", style="invis")
        with g.subgraph(name="cluster_e") as c:
            c.attr(label="edges (width = inference strength)", fontsize="9", color="#d3dce1")
            for i, (k, st) in enumerate(EDGE_STYLE.items()):
                c.node(f"a{i}", "", shape="point", width="0.05")
                c.node(f"b{i}", EDGE_LABEL[k], shape="plaintext")
                c.edge(f"a{i}", f"b{i}", **st)
                if i % 4:  # chain four samples per row so the legend forms a grid
                    c.edge(f"b{i - 1}", f"a{i}", style="invis")
        return g

    # ---------------- mermaid ----------------

    def to_mermaid(self, evidence=False, references=True, open_questions=True, assumptions=False,
                   focus=None, depth=1, direction="LR", width=40):
        """Return Mermaid flowchart source."""
        visible, edges = self._view(evidence, references, open_questions, assumptions, focus, depth)
        mid = {nid: "n_" + re.sub(r"\W", "_", nid) for nid in visible}
        shape = {
            "reference": ('[/"', '"/]'), "open_question": ('{{"', '"}}'), "evidence": ('["', '"]'),
            "assumption": ('[/"', '"\\]'), "hypothesis": ('(["', '"])'),
        }
        css = {
            "main": "fill:#14212a,color:#fff,stroke:#14212a",
            "claim": "fill:#fff,stroke:#5a6a75,color:#14212a",
            "method": "fill:#eef3f6,stroke:#5a6a75,color:#14212a",
            "counter": "fill:#fff4f2,stroke:#b23a2f,stroke-width:2px,color:#14212a",
            "hyp": "fill:#fff8ec,stroke:#a8700f,stroke-dasharray:5 3,color:#14212a",
            "oq": "fill:#fff8ec,stroke:#a8700f,color:#14212a",
            "ev": "fill:#e6edf0,stroke:#e6edf0,color:#14212a",
            "asm": "fill:#f3f0f7,stroke:#7a6a8f,color:#14212a",
            "ref": "fill:#e9f1fb,stroke:#3b6ea8,color:#14212a",
        }
        cls_of = {"main_conclusion": "main", "counter_claim": "counter", "hypothesis": "hyp", "open_question": "oq",
                  "evidence": "ev", "assumption": "asm", "reference": "ref", "methodological_conclusion": "method"}
        arrow = {"challenges": "--x", "conditional": "-.->", "motivates": "-.->", "raises": "-.->",
                 "required_to_validate": "-.-o", "rule": "-.->", "validates": "-.->", "background": "-.->",
                 "assumption": "-.->", "mechanistic": "-.->"}
        out = [f"flowchart {direction}"]
        refs = sorted(n for n in visible if self.nodes[n].kind == "reference")
        if refs:
            out.append('  subgraph literature["External literature"]')
        for nid in refs + sorted(n for n in visible if self.nodes[n].kind != "reference"):
            n = self.nodes[nid]
            text = "<br/>".join(_wrap(n.label_text, width, 4)).replace('"', "#quot;")
            o, c = shape.get(n.kind, ('("', '")'))
            out.append(f"  {mid[nid]}{o}<b>{nid}</b><br/>{text}{c}")
            out.append(f"  class {mid[nid]} {cls_of.get(n.kind, 'claim')}")
            if refs and nid == refs[-1]:
                out.append("  end")
        link_styles = []
        for i, e in enumerate(edges):
            label = f"|{EDGE_LABEL[e.kind]}|" if e.kind in ("challenges", "conditional") else ""
            out.append(f"  {mid[e.source]} {arrow.get(e.kind, '-->')}{label} {mid[e.target]}")
            w = STRENGTH_WIDTH.get(self.nodes[e.source].strength, 1.6) if e.kind == "supports" else 1.4
            link_styles.append(f"  linkStyle {i} stroke:{EDGE_STYLE.get(e.kind, {}).get('color', '#5a6a75')},stroke-width:{w}px")
        out += [f"  classDef {name} {style}" for name, style in css.items()]
        return "\n".join(out + link_styles)

    def show_mermaid(self, **kwargs):
        """Render the Mermaid diagram (JupyterLab >= 4.1 renders ```mermaid natively)."""
        from IPython.display import Markdown, display

        display(Markdown("```mermaid\n" + self.to_mermaid(**kwargs) + "\n```"))

    # ---------------- details ----------------

    def describe(self, node_id):
        """Markdown summary of one node: statement, status, inference, data, relations."""
        from IPython.display import Markdown

        n = self.nodes[node_id]
        o = n.obj
        md = [f"### {n.id} · {_words(n.kind)}"]
        if isinstance(o, Reference):
            md.append(f"**{fmt(o.title or o.note or '')}**  ")
            md.append(", ".join(o.authors) + f" ({o.year or '?'}) — {o.citation}")
            if o.roles:
                md.append("\nRoles: " + ", ".join(f"`{x}`" for x in o.roles))
        elif getattr(o, "statement", None):
            md.append(f"> {fmt(o.statement)}")

        if isinstance(o, ArgumentNode):
            ps = o.paper_statement
            if ps:
                md.append(f"\n**In the paper:** {fmt(ps.paraphrase)}" + (f" *({ps.source})*" if ps.source else ""))
            es = o.epistemic_status
            if es:
                fields = es.model_dump(exclude_none=True, exclude={"reason"})
                md.append("\n**Epistemic status:** " + ", ".join(f"{_words(k)}: `{v}`" for k, v in fields.items()))
                if es.reason:
                    md.append(f"\n{fmt(es.reason)}")
            inf = o.inference
            if inf:
                md.append(f"\n**Inference** (`{inf.effective_strength}`): {fmt(inf.rule or '')}")
                for st in inf.chain:
                    refs = ", ".join(s.reference for s in st.external_support) or "no external support"
                    md.append(f"- {fmt(st.from_)} → {fmt(st.to)} (`{st.strength}`, {refs})")
                if inf.caveat:
                    md.append(f"\n*Caveat:* {fmt(inf.caveat)}")
            md += [f"- *Limitation:* {fmt(lim)}" for lim in o.limitations]

        for ev in [o] if isinstance(o, Evidence) else getattr(o, "evidence", []):
            head = f"\n**{ev.id}** · {ev.origin or ''} {ev.type or ''}".rstrip()
            if ev.source:
                head += f" — {ev.source}"
            if ev.cited_references:
                head += " — cites " + ", ".join(ev.cited_references)
            md.append(head)
            for key in ("data", "derived"):
                value = getattr(ev, key)
                if value:
                    md.append(f"\n{key} ({ev.unit or ''}):\n```yaml\n"
                              + yaml.safe_dump(value, sort_keys=False, allow_unicode=True) + "```")
            if ev.observation or ev.statement:
                md.append(fmt(ev.observation or ev.statement))

        incoming = [e for e in self.edges.values() if e.target == n.id]
        outgoing = [e for e in self.edges.values() if e.source == n.id]
        if incoming or outgoing:
            md.append("\n**Relations**")
            md += [f"- `{e.source}` {EDGE_LABEL.get(e.kind, e.kind)} **this**" for e in incoming]
            md += [f"- **this** {EDGE_LABEL.get(e.kind, e.kind)} `{e.target}`" for e in outgoing]
        return Markdown("\n".join(md))

    # ---------------- interactive ----------------

    def explore(self):
        """ipywidgets explorer: toggle layers, focus on a node, inspect details."""
        import ipywidgets as w
        from IPython.display import display

        def natural(s):
            return [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", s)]

        ids = sorted(self.nodes, key=natural)
        ev = w.Checkbox(value=False, description="evidence", indent=False)
        refs = w.Checkbox(value=True, description="references", indent=False)
        oq = w.Checkbox(value=True, description="open questions", indent=False)
        asm = w.Checkbox(value=False, description="assumptions", indent=False)
        focus = w.Dropdown(options=[("— whole graph —", None)] + [(i, i) for i in ids], description="focus")
        depth = w.IntSlider(value=1, min=1, max=4, description="depth")
        graph_out, detail_out = w.Output(), w.Output(layout=w.Layout(max_width="520px"))

        def redraw(*_):
            graph_out.clear_output(wait=True)
            with graph_out:
                display(self.to_graphviz(evidence=ev.value, references=refs.value, open_questions=oq.value,
                                         assumptions=asm.value, focus=focus.value, depth=depth.value))
            detail_out.clear_output(wait=True)
            if focus.value:
                with detail_out:
                    display(self.describe(focus.value))

        for ctl in (ev, refs, oq, asm, focus, depth):
            ctl.observe(redraw, names="value")
        redraw()
        controls = w.HBox([ev, refs, oq, asm, focus, depth], layout=w.Layout(flex_flow="row wrap", gap="12px"))
        display(w.VBox([controls, w.HBox([graph_out, detail_out])]))
