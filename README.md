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
3. Record the inference rule (warrant) behind each step and, where the paper gives numbers, checks that can be recomputed.
4. Assess every claim: *does the data presented in the paper support it?*

**Output:**
1. **Logic:** a verdict for each claim (YES, PARTIAL, INCONCLUSIVE or NO) and a **logic score** for the paper.
2. **Limitations:** those stated by the authors, the assumptions the argument rests on, weak inference rules, and the weaknesses we find.
3. **Missing evidence:** what would be needed to support the claims that are not yet supported.

Every result comes in a machine-readable form (YAML, plus JSON Schema and RDF exports) and a human-readable one (Markdown report and argument map).

### Scope decisions so far

- **One paper at a time.** The paper stands on its own. There is no linking to other papers and no external ontology.
- **References are not looked up.** We assume every cited reference is cited for the right reasons and provides the evidence it is cited for. A statement backed by a citation therefore counts as supported, and only the **internal logic** of the paper is evaluated. `cited_works` records what each reference is assumed to provide.
- **Background knowledge is allowed but labelled.** Links that need knowledge from outside the paper (from a human or an LLM) are marked `ANNOTATOR_BACKGROUND`, so they stay separate from what the paper itself argues.

## Repository layout

```
schema/claim_chain.yaml           LinkML schema: the format (v0.4)
schema/claim_chain.schema.json    JSON Schema generated from it (e.g. for LLM structured output)
scripts/render.py                 YAML -> readable chain, report, argument maps, scores, recomputed checks
examples/<paper>/                 encoded papers; generated/ holds the outputs
test_papers/                      10 recent arXiv cond-mat.mtrl-sci papers to test on (BibTeX only; fetch PDFs yourself)
test_papers/yaml/                 the 10 test papers encoded in the format (LLM drafts)
docs/blackboard_2026-10-21/       photos and transcription of the team's blackboard discussion
ideas/<name>/                     each team member's approaches and experiments
.claude/skills/annotating-claim-chains/  skill for annotating a paper with an LLM: workflow, verdicts, review checklist
```

## Team approaches

Each person's approach is in `ideas/<name>/`. The first versions were written from Markus's notes of the discussion, to be filled in by each person. All four are combined in the format:

| Who | Approach | In the format |
|---|---|---|
| Sepideh | **Divide and conquer:** analyse parts of the paper separately. Start with the introduction to set up the hypothesis properly, then assess the whole-paper logic. | `paper_part` on every statement; the report lists statements per part |
| Soroush | **Quantify the support:** rate the evidence for each claim as strong, intermediate or weak. | `support_strength` on relations and warrants |
| Jan | **Reviewer / investigator:** each claim creates open proof obligations; gather the evidence and check which obligations it discharges. His Zhuang 2017 encoding (branch `jan-janssen`) added recomputable checks, explicit inference rules, claim roles, the authors' own certainty, structured data requests and reference roles. | `proof_obligations` with `priority` and `requested_data`; `derived_checks`; `warrant`; `claim_role`; `author_certainty`; `cited_works` |
| Markus | **Typed argument chain:** statements typed by role and evidence kind, typed relations including "undercuts", a verdict per claim and a logic score. | the core schema and `render.py` |

## The format in short

- An **ArgumentChain** is one paper. It contains **Statements**, **Relations** between them, the **Entities** they refer to (materials, techniques, quantities), and the **cited works** with what each is cited for.
- **Statements** have:
  - a type, a section and the part of the paper they come from
  - evidence: its kind (citation, argument, data judged by eye, numbers, none), where it is in the paper (figure, table, equation), its values, and **derived checks** (e.g. Born stability criteria) that `render.py` recomputes from the values
  - a scope (materials, sample count)
  - for claims, a modality (descriptive, comparative, correlational, causal, generalization, conceptual), a **role** (main conclusion, intermediate, quantitative support, mechanistic interpretation, methodological, counter-claim) and the **authors' certainty** (demonstrated, predicted, proposed, speculative)
  - a **warrant**: the inference rule that links the statement's own evidence to it, with its basis (citation, definition, empirical correlation, domain convention, author argument, unstated) and strength
  - concerns flagged by the annotator
- **Assumptions** say whether they are community-accepted or the authors' own choice, and what open question they leave.
- **Relations** say:
  - who asserts them: the authors, the annotator, or the annotator using background knowledge
  - how they support: qualitatively, quantitatively or logically
  - how strongly they support: strong, intermediate or weak
  - how uncertain they are
  - optionally the warrant behind the step
- Every **claim and hypothesis** gets an **assessment** by the annotator: a validity verdict, a rationale, the missing evidence, and **proof obligations** with status, priority and the data that would discharge them. The authors' own stance stays separate in `author_certainty`.
- The **paper assessment** holds the overall verdict, key limitations and missing evidence.

**Scores (draft):**
- **Logic score:** the mean over all claims and hypotheses of YES = 1, PARTIAL = 0.5, INCONCLUSIVE = 0.25, NO = 0.
- **Weighted logic score:** the same, with main conclusions weighted 3, counter-claims 0 and all other claims 1.
- **Obligation coverage:** the share of proof obligations discharged, with partially discharged ones counting half.

None of these weightings is agreed yet.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

E=examples/wang2026_lattice_genome
linkml-validate -s schema/claim_chain.yaml $E/wang2026_lattice_genome.yaml
python scripts/render.py $E/wang2026_lattice_genome.yaml $E/generated/
linkml-convert -s schema/claim_chain.yaml -t ttl -o $E/generated/wang2026_lattice_genome.ttl $E/wang2026_lattice_genome.yaml
gen-json-schema schema/claim_chain.yaml > schema/claim_chain.schema.json

# all test papers
for f in test_papers/yaml/*.yaml; do python scripts/render.py $f /tmp/out/; done

# test papers: PDFs are not in the repo, each user fetches them individually
(cd test_papers && ./fetch_papers.sh)
# optional diagram: npx @mermaid-js/mermaid-cli -i $E/generated/wang2026_lattice_genome_core.mmd -o $E/generated/wang2026_lattice_genome_core.png
```

## Automated conversion: the `claimchain` command

The Python package in `src/claimchain/` converts a PDF into a claim-chain YAML with Claude. Claude reads the PDF, figures included. The package checks the returned YAML against `schema/claim_chain.yaml` and against the reference rules (unique ids, no dangling references, every claim assessed). Any problems are sent back to Claude for up to two rounds of correction.

```bash
pip install .                      # or: pip install -e ".[test]" for development
export ANTHROPIC_API_KEY=...       # any Anthropic SDK credential source works

claimchain paper.pdf               # writes paper.yaml next to the PDF
claimchain paper.pdf -o out.yaml --effort xhigh --max-repairs 3
claimchain --help
```

Exit status: 0 = valid YAML written; 1 = YAML written but it still fails validation (the problems are printed); 2 = error (refusal, API error, unreadable input). The default model is `claude-opus-5-5`, with adaptive thinking at effort `high`. Server-side refusal fallback is on by default; pass `--no-fallback` on Amazon Bedrock, Vertex AI or Microsoft Foundry.

From Python, e.g. inside a backend:

```python
from claimchain import convert_pdf

result = convert_pdf("paper.pdf")         # anthropic.Anthropic() client by default
result.valid, result.issues, result.usage # validation outcome, token counts
open("paper.yaml", "w").write(result.yaml_text)
```

The prompt (`src/claimchain/prompts/`) contains the annotation instructions and the review checklist from the `annotating-claim-chains` skill. The installed package ships with the schema and the Wang example. For the RDF export, add the paper's prefix to `schema/claim_chain.yaml`, as you would for a hand-encoded paper. Run the offline tests with `pytest`. GitHub Actions (`.github/workflows/tests.yml`) runs them on Python 3.10–3.13 for every push to `main` and every pull request. They use a fake client, so CI needs no API key.

## Example

## Examples

All scores are drafts. Claim roles in the Wang example and the test papers were assigned afterwards from the claim text and section.

| Paper | Statements | Score | Weighted | Obligations discharged |
|---|---|---|---|---|
| `examples/wang2026_lattice_genome/`: Wang et al. 2026, "Lattice genome", arXiv:2606.09611, encoded by hand | 64 | 0.46 | 0.46 | 0.25 (of 10) |
| `examples/zhuang2017_d019_mgal/`: Zhuang, Chen & Carter 2017, D0₁₉ Mg₃Al, MSMSE 25, 075002. Converted from Jan's encoding (`zhuang2017_d019_mgal.yaml`, with his Pydantic model, graph explorer and notebook in the same folder); shows warrants and recomputed checks | 21 | 0.75 | 0.68 | 0.50 (of 8) |
| `test_papers/yaml/`: 10 arXiv papers from 21 October 2026, LLM drafts | 27–36 each | 0.36–0.93 | 0.37–0.91 | 0.25–1.00 |

The examples illustrate the format only; the tool is meant for any paper. No PDFs are included.

## Status and next steps

- [x] Schema v0.2 with verdicts and logic score; one hand-encoded example.
- [x] Schema v0.3: team approaches added (paper parts, support strength, proof obligations).
- [x] All 10 test papers encoded (LLM drafts).
- [x] Schema v0.4: Jan's additions (derived checks, warrants, claim roles, author certainty, requested data, cited works).
- [ ] Each team member refines their `ideas/` folder.
- [x] Annotation skill (`.claude/skills/annotating-claim-chains/`), updated for v0.4.
- [x] LLM extraction: paper → YAML instance validated against the schema (`claimchain` command, first version).
- [ ] Evaluate the `claimchain` output against hand-checked chains (e.g. the ten test papers).
- [ ] Agree on the scoring (weighting, central vs. peripheral claims, propagation of uncertainty).
- [ ] Decide whether claims backed only by argument count against internal logic.
- [ ] Test set: e.g. retracted papers (expected to be inconclusive or invalid) vs. well-regarded ones.
- [ ] Check reliability: agreement between several annotators or LLM runs on the same paper.

## Open design questions

- `support_strength` and `uncertainty` on relations overlap: keep both, merge them, or derive one from the other?
- Should verdicts be derived from proof obligations (all discharged = YES, some = PARTIAL, none = NO)?
- Should each paper part get a sub-score before the whole-paper score?
- Should the critique (concerns, assessments) be stored separately from the encoded paper?
- How should uncertain links propagate to the claims that depend on them? Warrants with weak or unstated bases are natural places to start.
- `UNDERCUTS` and `CONTRADICTS` both map to `mp:challenges` in the RDF export, so the distinction is lost there.
- The namespaces (`w3id.org/claim-chain/...`) are placeholders.

## Background

The format is loosely modelled on the Micropublications ontology (Clark et al. 2014, doi:10.1186/2041-1480-5-28) and written in [LinkML](https://linkml.io). Warrants follow Toulmin's argument model (claim, data, warrant).

## License

GPL-3.0, see `LICENSE`.
