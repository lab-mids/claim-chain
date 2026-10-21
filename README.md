# claim-chain

**Turn a single research paper into a chain of claims, check whether its internal logic holds, and give the paper a logic score.**

Started at the Open Science Hackathon, 21 October 2026. Team: Markus, Jan, Sepideh, Soroush.

## Motivation

Review is the bottleneck of scientific progress. LLMs speed up the production of research, but checking whether a paper's conclusions follow from its evidence is still slow, manual work. There is no shared format for the logical chain of arguments inside a paper, including how uncertain each step is and whether a claim is correlational or causal.

## What claim-chain does

**Input:** one paper (text, tables, figures, supplementary information). Any field; materials science is our home domain.

**Processing:**
1. Extract the paper's argument as typed statements: background, gap, hypothesis, assumption, method, data, observation, claim, limitation, outlook.
2. Record the evidence the paper gives for each statement, and the links between statements: supports, undercuts, qualifies, alternative explanation, and so on.
3. Assess every claim: *does the data presented in the paper support it?*

**Output:**
1. **Logic:** a verdict for each claim (YES, PARTIAL, INCONCLUSIVE or NO) and a **logic score** for the paper.
2. **Limitations:** those stated by the authors, the assumptions the argument rests on, and the weaknesses we find.
3. **Missing evidence:** what would be needed to support the claims that are not yet supported.

Every result comes in a machine-readable form (YAML, plus JSON Schema and RDF exports) and a human-readable one (Markdown report and argument map).

### Scope decisions so far

- **One paper at a time.** The paper stands on its own. There is no linking to other papers and no external ontology.
- **References are not looked up.** We assume every cited reference is cited for the right reasons and provides the evidence it is cited for. A statement backed by a citation therefore counts as supported, and only the **internal logic** of the paper is evaluated.
- **Background knowledge is allowed but labelled.** Links that need knowledge from outside the paper (from a human or an LLM) are marked `ANNOTATOR_BACKGROUND`, so they stay separate from what the paper itself argues.

## Repository layout

```
schema/claim_chain.yaml           LinkML schema: the format (v0.3)
schema/claim_chain.schema.json    JSON Schema generated from it (e.g. for LLM structured output)
scripts/render.py                 YAML -> readable chain, report, argument maps, logic score
examples/<paper>/                 encoded papers; generated/ holds the outputs
test_papers/                      10 recent arXiv cond-mat.mtrl-sci papers to test on (BibTeX only; fetch PDFs yourself)
docs/blackboard_2026-10-21/       photos and transcription of the team's blackboard discussion
ideas/<name>/                     each team member's approaches and experiments
```

## Team approaches

Each person's approach is in `ideas/<name>/`. The first versions were written from Markus's notes of the discussion, to be filled in by each person. All four are combined in the format:

| Who | Approach | In the format |
|---|---|---|
| Sepideh | **Divide and conquer:** analyse parts of the paper separately. Start with the introduction to set up the hypothesis properly, then assess the whole-paper logic. | `paper_part` on every statement; the report lists statements per part |
| Soroush | **Quantify the support:** rate the evidence for each claim as strong, intermediate or weak. | `support_strength` on relations |
| Jan | **Reviewer / investigator:** each claim creates open proof obligations; gather the evidence and check which obligations it discharges. | `proof_obligations` (open, partially discharged, discharged; `discharged_by`) in each claim's assessment; open obligations listed in the report |
| Markus | **Typed argument chain:** statements typed by role and evidence kind, typed relations including "undercuts", a verdict per claim and a logic score. | the core schema and `render.py` |

## The format in short

- An **ArgumentChain** is one paper. It contains **Statements**, **Relations** between them, and the **Entities** they refer to (materials, techniques, quantities).
- **Statements** have:
  - a type and a section
  - evidence: its kind (citation, argument, data judged by eye, numbers, none) and where it is in the paper (figure, table, equation)
  - a scope (materials, sample count)
  - for claims, a modality (descriptive, comparative, correlational, causal, generalization, conceptual)
  - concerns flagged by the annotator
- **Assumptions** say whether they are community-accepted or the authors' own choice, and what open question they leave.
- Statements also record which **part of the paper** they come from.
- **Relations** say:
  - who asserts them: the authors, the annotator, or the annotator using background knowledge
  - how they support: qualitatively, quantitatively or logically
  - how strongly they support: strong, intermediate or weak
  - how uncertain they are
- Every **claim and hypothesis** gets an **assessment**: a validity verdict, a rationale, the missing evidence, and **proof obligations** with their status.
- The **paper assessment** holds the overall verdict, key limitations and missing evidence.

**Logic score (draft):** the mean over all claims and hypotheses of YES = 1, PARTIAL = 0.5, INCONCLUSIVE = 0.25, NO = 0. The weighting is not agreed yet.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

E=examples/wang2026_lattice_genome
linkml-validate -s schema/claim_chain.yaml $E/wang2026_lattice_genome.yaml
python scripts/render.py $E/wang2026_lattice_genome.yaml $E/generated/
linkml-convert -s schema/claim_chain.yaml -t ttl -o $E/generated/wang2026_lattice_genome.ttl $E/wang2026_lattice_genome.yaml
gen-json-schema schema/claim_chain.yaml > schema/claim_chain.schema.json

# test papers: PDFs are not in the repo, each user fetches them individually
(cd test_papers && ./fetch_papers.sh)
# optional diagram: npx @mermaid-js/mermaid-cli -i $E/generated/wang2026_lattice_genome_core.mmd -o $E/generated/wang2026_lattice_genome_core.png
```

## Example

`examples/wang2026_lattice_genome/` holds one paper encoded by hand: Wang et al. 2026, "Lattice genome", arXiv:2606.09611. It has 64 statements and 68 relations, and its logic score is 0.46. It illustrates the format only; the tool is meant for any paper. The paper's PDF is not included.

## Status and next steps

- [x] Schema v0.2 with verdicts and logic score; one hand-encoded example.
- [x] Schema v0.3: team approaches added (paper parts, support strength, proof obligations).
- [ ] Each team member refines their `ideas/` folder.
- [ ] LLM extraction: paper → YAML instance validated against the schema.
- [ ] Agree on the scoring (weighting, central vs. peripheral claims, propagation of uncertainty).
- [ ] Decide whether claims backed only by argument count against internal logic.
- [ ] Test set: e.g. retracted papers (expected to be inconclusive or invalid) vs. well-regarded ones.
- [ ] Check reliability: agreement between several annotators or LLM runs on the same paper.

## Open design questions

- `support_strength` and `uncertainty` on relations overlap: keep both, merge them, or derive one from the other?
- Should verdicts be derived from proof obligations (all discharged = YES, some = PARTIAL, none = NO)?
- Should each paper part get a sub-score before the whole-paper score?
- Should the critique (concerns, assessments) be stored separately from the encoded paper?
- How should uncertain links propagate to the claims that depend on them?
- `UNDERCUTS` and `CONTRADICTS` both map to `mp:challenges` in the RDF export, so the distinction is lost there.
- The namespaces (`w3id.org/claim-chain/...`) are placeholders.

## Background

The format is loosely modelled on the Micropublications ontology (Clark et al. 2014, doi:10.1186/2041-1480-5-28) and written in [LinkML](https://linkml.io).

## License

GPL-3.0, see `LICENSE`.
