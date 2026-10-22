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
schema/claim_chain.yaml           LinkML schema: the format (v0.6)
schema/claim_chain.schema.json    JSON Schema generated from it (e.g. for LLM structured output)
scripts/render.py                 YAML -> readable chain, report, argument maps, one-page summary chart, scores, derived verdicts, golden thread, local checks per part, recomputed checks
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
| Sepideh | **Divide and conquer / paper logic map:** analyse each part of the paper against a fixed question spine, check it locally (completeness, arithmetic, consistency), then follow each aim from the introduction to the conclusion (the golden thread). Worked example: Zhang et al. 2013 (`ideas/sepideh/`). | `paper_part`; AIM statements; DELIVERS and RESTATES links; certainty drift; ARITHMETIC concern and concern `priority`; local checks counted per part; question spine in the review checklist; `claimchain --intro-first` |
| Soroush | **Quantify the support:** test every link on five criteria (directness, sufficiency, controls, alternatives, scope), rate it strong to unsupported, and derive claim verdicts with the weakest-link rule. Tested on two ML papers (`ideas/soroush/`). | `support_strength`, `link_criteria`, `essential`; WEAK verdict; derived verdicts and score; summary chart |
| Jan | **Reviewer / investigator:** each claim creates open proof obligations; gather the evidence and check which obligations it discharges. His Zhuang 2017 encoding (branch `jan-janssen`) added recomputable checks, explicit inference rules, claim roles, the authors' own certainty, structured data requests and reference roles. | `proof_obligations` with `priority` and `requested_data`; `derived_checks`; `warrant`; `claim_role`; `author_certainty`; `cited_works` |
| Markus | **Typed argument chain:** statements typed by role and evidence kind, typed relations including "undercuts", a verdict per claim and a logic score. | the core schema and `render.py` |

## The format in short

- An **ArgumentChain** is one paper. It contains **Statements**, **Relations** between them, the **Entities** they refer to (materials, techniques, quantities), and the **cited works** with what each is cited for.
- **Statements** have:
  - a type, a section and the part of the paper they come from; **aims** record what the introduction promises
  - evidence: its kind (citation, argument, data judged by eye, numbers, none), where it is in the paper (figure, table, equation), its values, and **derived checks** (e.g. Born stability criteria) that `render.py` recomputes from the values
  - a scope (materials, sample count)
  - for claims, a modality (descriptive, comparative, correlational, causal, generalization, conceptual), a **role** (main conclusion, intermediate, quantitative support, mechanistic interpretation, methodological, counter-claim) and the **authors' certainty** (demonstrated, predicted, proposed, speculative)
  - a **warrant**: the inference rule that links the statement's own evidence to it, with its basis (citation, definition, empirical correlation, domain convention, author argument, unstated) and strength
  - concerns flagged by the annotator, with a priority
- **Assumptions** say whether they are community-accepted or the authors' own choice, and what open question they leave.
- **Relations** say:
  - who asserts them: the authors, the annotator, or the annotator using background knowledge
  - how they support: qualitatively, quantitatively or logically
  - how strongly they support: strong, intermediate, weak or unsupported, tested on five **link criteria** (directness, sufficiency, controls, alternatives, scope match; Soroush's approach)
  - whether the link is **essential**: the claim cannot hold without it
  - how uncertain they are
  - optionally the warrant behind the step
- **DELIVERS** links connect each aim to the methods, results and claims that carry it out, and **RESTATES** links connect a conclusion sentence to the claim it repeats. Together they give the **golden thread**: `render.py` reports each aim as delivered, not restated at the end, method only, or dropped, and flags claims whose authors' certainty grows between discussion and conclusion.
- Every **claim and hypothesis** gets an **assessment** by the annotator: a validity verdict (YES, PARTIAL, WEAK, INCONCLUSIVE, NO), a rationale, the missing evidence, and **proof obligations** with status, priority and the data that would discharge them. The authors' own stance stays separate in `author_certainty`.
- The **paper assessment** holds the overall verdict, key limitations and missing evidence.

**Scores (draft):**
- **Logic score:** the mean over all claims and hypotheses of YES = 1, PARTIAL = 0.5, WEAK = 0.375, INCONCLUSIVE = 0.25, NO = 0.
- **Weighted logic score:** the same, with main conclusions weighted 3, counter-claims 0 and all other claims 1.
- **Derived score:** the logic score over verdicts that `render.py` derives from the links instead of the annotator's verdicts. A contradiction gives NO; otherwise the strongest support link decides; qualifying or undercutting links cap at PARTIAL; and a claim is no stronger than its weakest essential link (weakest-link rule). The report lists every claim where the derived verdict differs from the annotator's.
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
# *_summary.mmd is a one-page chart for non-experts: thesis, main conclusions, verdict in words, bottom line
```

`render.py` exits with `checks ok: False` and prints the offending item if a relation points to an unknown id or a derived check does not recompute.

## Automated conversion: the `claimchain` command

The Python package in `src/claimchain/` converts a PDF into a claim-chain YAML with Claude. Claude reads the PDF, figures included. The package checks the returned YAML against `schema/claim_chain.yaml` and against the reference rules (unique ids, no dangling references, every claim assessed). Any problems are sent back to Claude for up to two rounds of correction.

```bash
pip install .                      # or: pip install -e ".[test]" for development
export ANTHROPIC_API_KEY=...       # any Anthropic SDK credential source works

claimchain paper.pdf               # writes paper.yaml next to the PDF
claimchain paper.pdf -o out.yaml --effort xhigh --max-repairs 3
claimchain paper.pdf --intro-first  # fix aims from the introduction first, then encode the rest against them
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

The prompt (`src/claimchain/prompts/`) contains the annotation instructions and the review checklist from the `annotating-claim-chains` skill. The installed package ships with the schema and three reference examples: Wang (style), Zhuang (v0.4 and v0.5 features) and Zhang (v0.6 features). The command does not compute scores or run the derived checks; run `scripts/render.py` on its output for that. For the RDF export, add the paper's prefix to `schema/claim_chain.yaml`, as you would for a hand-encoded paper. Run the offline tests with `pytest`. GitHub Actions (`.github/workflows/tests.yml`) runs them on Python 3.10–3.13 for every push to `main` and every pull request. They use a fake client, so CI needs no API key.

## Examples

All scores are drafts. Claim roles in the Wang example and the test papers were assigned afterwards from the claim text and section.

| Paper | Statements | Score | Weighted | Derived | Obligations discharged |
|---|---|---|---|---|---|
| `examples/wang2026_lattice_genome/`: Wang et al. 2026, "Lattice genome", arXiv:2606.09611, encoded by hand | 64 | 0.46 | 0.46 | 0.55 | 0.25 (of 10) |
| `examples/zhuang2017_d019_mgal/`: Zhuang, Chen & Carter 2017, D0₁₉ Mg₃Al, MSMSE 25, 075002. Converted from Jan's encoding (`zhuang2017_d019_mgal.yaml`, with his Pydantic model, graph explorer and notebook in the same folder); shows warrants, recomputed checks and link criteria | 21 | 0.75 | 0.68 | 0.72 | 0.50 (of 8) |
| `examples/zhang2013_mg_sfe/`: Zhang, Dou, Liu & Guo 2013, stacking fault energies in Mg alloys, Comput. Mater. Sci. 79, 564. Converted from Sepideh's paper logic map (not from the paper itself); shows aims, the golden thread, certainty drift and local checks | 45 | 0.55 | 0.54 | 0.55 | 0.00 (of 2) |
| `test_papers/yaml/`: 10 arXiv papers from 21 October 2026, LLM drafts | 27–36 each | 0.36–0.93 | 0.37–0.91 | 0.38–0.71 | 0.25–1.00 |

The examples illustrate the format only; the tool is meant for any paper. No PDFs are included.

## Status and next steps

- [x] Schema v0.2 with verdicts and logic score; one hand-encoded example.
- [x] Schema v0.3: team approaches added (paper parts, support strength, proof obligations).
- [x] All 10 test papers encoded (LLM drafts).
- [x] Schema v0.4: Jan's additions (derived checks, warrants, claim roles, author certainty, requested data, cited works).
- [x] Schema v0.6: Sepideh's approach (aims, golden thread, certainty drift, local checks per part, question spine, intro-first pass); Zhang 2013 example converted from her logic map.
- [x] Schema v0.5: Soroush's approach (five link criteria, UNSUPPORTED strength, WEAK verdict, essential links, derived verdicts, summary chart). Replaces the per-claim criteria draft.
- [ ] Each team member refines their `ideas/` folder.
- [x] Annotation skill (`.claude/skills/annotating-claim-chains/`), updated for v0.6.
- [x] LLM extraction: paper → YAML instance validated against the schema (`claimchain` command, first version).
- [ ] Evaluate the `claimchain` output against hand-checked chains (e.g. the ten test papers).
- [ ] Agree on the scoring. Weighting by claim role hardly separates the test papers (most main conclusions are PARTIAL too), so the verdict scale may need more levels or a link to obligation coverage.
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

## To discuss on 22 October

1. **Sepideh's and Soroush's input.** How do paper-part sub-scores and support strength feed into the score? *Folded in as v0.5 (Soroush) and v0.6 (Sepideh). Local checks are counted per part and kept out of the logic score, as Sepideh suggests; do we want a combined paper score at all?*
2. **Headline score.** Which score is the result: the plain logic score, the role-weighted one, or the graded rubric score? Do we need more verdict levels, or a link to obligation coverage? *v0.5 adds a WEAK level and a derived score (verdicts computed from the links).*
3. **Criteria rubric** (draft in the schema and `render.py`). Do we adopt the six questions, and should the `claimchain` prompt ask the model to fill them in? *v0.5 replaces them with Soroush's five criteria per link, which the prompt now asks for.*
4. **Reliability.** Re-assessing the same claims agrees well (83 % of verdicts), but a fresh extraction finds about twice as many claims and lowers the score by about 0.1 (`docs/reliability_2026-10-21/`). Options: fix claim granularity in the prompt, make number checks mandatory, average 2-3 runs. *The derived score moves less between extraction and re-run (0.41 vs 0.38 and 0.38 vs 0.32) than the annotator's score (0.53 vs 0.42 and 0.40 vs 0.31).*
5. **Contested verdicts.** Who decides when a verdict is debatable, e.g. the near-stoichiometric window of c-BAs in 2610.26996? Do we need a second reviewer or a flag for "contested"?
6. **Evaluate `claimchain` end to end.** Run it on the ten test papers (needs an API key, budget and the PDFs) and compare with the existing drafts.
7. **One place for scoring.** Move the derived checks and scores from `scripts/render.py` into the package (e.g. `claimchain score`), so CLI output is scored the same way.
8. **Held-out test papers.** The review checklist was derived from the ten test papers, so judge it on new papers, e.g. retracted vs. well-regarded ones.
9. **Argument-only claims.** Do claims backed only by argument count against internal logic?
10. **Hackathon deliverable.** What do we show at the end: CLI demo, report for one paper, score comparison across papers?

## Background

The format is loosely modelled on the Micropublications ontology (Clark et al. 2014, doi:10.1186/2041-1480-5-28) and written in [LinkML](https://linkml.io). Warrants follow Toulmin's argument model (claim, data, warrant).

## License

GPL-3.0, see `LICENSE`.
