---
name: annotating-claim-chains
description: Use when encoding a research paper (PDF, arXiv preprint, manuscript) into a claim-chain argument-chain YAML for this repository, assessing whether its claims follow from its evidence, or computing a paper's logic score with schema/claim_chain.yaml and scripts/render.py.
---

# Annotating papers as claim chains

## Overview

A claim chain encodes one paper's argument as typed statements, typed relations between them, and a verdict per claim: **does the data presented in this paper support it?** You judge the paper's internal logic only. Cited references are assumed to support what they are cited for and are not looked up.

The value lies in the assessment, not in the transcription. A file that paraphrases the paper and gives every claim PARTIAL is worthless. Each verdict must name the specific evidence that is present or missing, and each step should say *why* the evidence implies the claim (the warrant).

## Before you start

1. Read `schema/claim_chain.yaml` (enums, required slots) and two reference examples:
   - `examples/wang2026_lattice_genome/wang2026_lattice_genome.yaml`: style. Short self-contained statement texts, a comment header per paper section, flow-style relations on one line each.
   - `examples/zhuang2017_d019_mgal/zhuang2017_d019_mgal_claimchain.yaml`: the v0.4 and v0.5 features. Warrants, link criteria and essential links, derived checks with formulas, claim roles, author certainty, prioritized proof obligations with requested data, `cited_works`.
2. Set up the tools once (in a scratch directory, not the repo):
   ```bash
   python3 -m venv venv && venv/bin/pip install -q pypdf pyyaml linkml
   venv/bin/python -I .claude/skills/annotating-claim-chains/extract_pdf_text.py paper.pdf > paper.txt
   ```
   Read the **whole** text, including methods, tables, appendix and SI pages. Many decisive inconsistencies sit in tables and methods. Figures come through only as captions; say so in the summary if a verdict depends on a figure you could not inspect.

## Workflow

1. **Name the output after the input.** `<pdf basename>.yaml` (e.g. `2610.28152.pdf` → `2610.28152.yaml`), placed where the user asks (test papers: `test_papers/yaml/`).
2. **Pick a per-paper prefix**: first author's surname (lowercase, ASCII, no hyphens) plus year, e.g. `boticaartalejo2026`. Add it to `prefixes:` in `schema/claim_chain.yaml` (`<prefix>: https://w3id.org/claim-chain/arXiv<id>/`), otherwise the TTL export fails.
3. **Header**: `id: claimchain:chain/arXiv<id>`, `schema_version` (the schema's `version`), `annotator` (model plus "from PDF"), `annotation_date` (quoted ISO date), and `publication` with `arxiv:` as a **quoted string**.
4. **Entities** (`ent:` prefix): materials, processing states, techniques, methods, quantities and concepts that statements refer to. Reuse them in `about`, `scope.materials` and `scope.techniques`.
5. **Cited works** (optional, `<prefix>:ref<n>`): only the references the argument actually leans on (an inference rule, a validated baseline), each with `cited_for` saying what it is assumed to provide. Background citations can stay as plain numbers in `evidence.references`.
6. **Statements, part by part** (`paper_part`), in reading order:
   - INTRODUCTION: BACKGROUND (cited), GAP, one central HYPOTHESIS (the thesis the paper sets out to establish), and ASSUMPTIONs taken on board.
   - METHODS / THEORY: METHOD, DATA (with `scope.sample_count`), ASSUMPTION (with `assumption_basis` and `open_question`), DEFINITION.
   - RESULTS: OBSERVATION (what the data show, with numbers in `evidence.values`), then CLAIM (what the authors conclude from it).
   - DISCUSSION / CONCLUSION: CLAIMs (generalizations, mechanisms), LIMITATIONs the authors themselves state (`limitation_kind`), OUTLOOK, open QUESTIONs (with `priority`).
   - An assumption the argument needs but the paper never states may be added as an ASSUMPTION; an implicit claim you formulate yourself must carry a `note` saying so.
7. **Classify every CLAIM and HYPOTHESIS:**
   - `claim_role`: MAIN_CONCLUSION (what the abstract and conclusions sell; usually the HYPOTHESIS and 1-4 claims), INTERMEDIATE, QUANTITATIVE_SUPPORT, MECHANISTIC_INTERPRETATION, METHODOLOGICAL, or COUNTER_CLAIM (the paper's own result against its conclusion). The weighted score counts main conclusions three times and counter-claims not at all, so be deliberate.
   - `author_certainty`: how the **authors** present it (DEMONSTRATED, PREDICTED, PROPOSED, SPECULATIVE). This is their stance, not your verdict; a gap between the two is often the finding.
8. **Warrants.** For every claim whose support is not self-evident, write the inference rule that links evidence to claim: on the statement (for its own evidence) or on the SUPPORTS relation (for statement → statement). Give `warrant_basis` honestly: CITATION, DEFINITION, EMPIRICAL_CORRELATION (rules of thumb such as Pugh's ratio), DOMAIN_CONVENTION, AUTHOR_ARGUMENT, or UNSTATED (the paper uses the rule without saying so). A multi-step inference becomes intermediate statements, each with its own warrant. Weak, empirical and unstated warrants appear in the report's limitations.
9. **Derived checks.** Where the paper reports numbers and a criterion or derived value, make it recomputable: give each value a `symbol` and add a `derived_checks` entry with a human-readable `expression`, a Python `formula` over the symbols, and the reported `result` or `satisfied`. Examples: Born stability criteria, percentage differences quoted in the text, a fitted parameter plugged into the paper's own equation. A check that fails to recompute is a finding: record it as a concern, not by changing the numbers.
10. **Assess every CLAIM and HYPOTHESIS** (see Verdicts). Add `concerns` wherever you find a weakness, on any statement type.
11. **Relations** (`<prefix>:R<n>`). Every CLAIM needs incoming SUPPORTS from its observations, plus UNDERCUTS / CONTRADICTS / QUALIFIES / ALTERNATIVE_EXPLANATION_FOR where they apply. Use CONDITIONALLY_SUPPORTS for an untested hypothesis the argument leans on. Put `support_basis`, `support_strength` and `uncertainty` on SUPPORTS links into claims; `support_strength` rates the link (does this evidence bear on this claim?), `uncertainty` the evidence itself (how precise is it?). Set `asserted_by` honestly:
    - `AUTHORS`: the paper makes the link.
    - `ANNOTATOR`: you derived it from the paper's own content (e.g. its own table contradicts its own claim).
    - `ANNOTATOR_BACKGROUND`: it needs outside domain knowledge (e.g. "a 3-7 nm grain size alone can stabilize t-ZrO2").
    Test every SUPPORTS and CONDITIONALLY_SUPPORTS link into a claim on five criteria in `link_criteria` (MET, PARTLY, NOT_MET or NOT_APPLICABLE, with a short `criteria_note`): **directness** (does the evidence measure the claimed quantity, or only a proxy?), **sufficiency** (samples, repeats, statistics, error analysis), **controls** (confounders, a fair baseline), **alternatives** (other plausible explanations excluded?) and **scope_match** (does the claim stay within what was tested?). Set `support_strength` to match: all met STRONG; one or two partly INTERMEDIATE; one failed or more than two partly WEAK; directness or scope failed UNSUPPORTED (the link does not carry the claim at all). Mark a link `essential: true` only if the claim cannot hold without it; render.py caps a claim at its weakest essential link and at the verdict of the claim that link comes from, and reports where its derived verdict differs from yours.
12. **paper_assessment**: `overall_validity`, a 3-5 sentence `summary` (what holds, then what does not), 3-5 `key_limitations` each citing statement ids, and `missing_evidence`. Do not write `logic_score`; render.py computes it.
13. **Validate and render** (both must be clean before you report):
    ```bash
    linkml-validate -s schema/claim_chain.yaml -C ArgumentChain <file>.yaml
    python scripts/render.py <file>.yaml <scratch-out-dir>/      # dangling refs, derived checks, scores
    linkml-convert -s schema/claim_chain.yaml -C ArgumentChain -t ttl -o <scratch>/x.ttl <file>.yaml
    ```
    render.py must print `checks ok: True`. Look at the claims where the derived verdict differs from yours: either a link rating or your verdict is wrong. Write render output to a scratch directory unless the user wants `generated/` files committed.

## Verdicts

| Validity | Use when |
|---|---|
| `"YES"` | The presented data support the claim as worded, including by construction or a large benchmark. |
| `PARTIAL` | Part is shown (e.g. the trend), part is not (mechanism, generality, "better", "optimal"). |
| `WEAK` | Only weak support: indirect, thin or uncontrolled evidence (only WEAK links). |
| `INCONCLUSIVE` | No data in the paper decide it: argued by analogy, mechanism proposed but not tested, outlook dressed as a claim. |
| `"NO"` | The paper's own data or statements contradict it. |

- `rationale` (required) names the decisive evidence or gap in one or two sentences.
- `missing_evidence` lists concrete experiments or analyses ("slow-anneal control of the same film"), not "more data".
- `proof_obligations` on the HYPOTHESIS and on main conclusions: one per thing that must be shown, with `obligation_status` and `discharged_by` ids. Give OPEN obligations a `priority` (CRITICAL if the main conclusion fails without it) and `requested_data` (quantity, unit, method) where you can name the measurement. An OPEN obligation is what a reviewer would ask for.
- Judge each claim on its own evidence. Do not hedge everything into PARTIAL: careful papers earn YES, and self-contradicting claims earn NO.

## Finding weaknesses

Work through **review-checklist.md** (in this directory) for every paper: the general checks, then the section for the paper's type. These are the checks that found the real problems in the test papers. The most productive ones:

- **Plug the paper's numbers into the paper's own equations**, as derived checks. Fitted parameters often contradict the model they claim to confirm.
- **Check normalisation and units of compared quantities** (per cell vs per atom, per mass vs per volume). *Zhuang 2017: DOS(E_F) compared per cell across cells of 8, 4 and 2 atoms.*
- **Compare abstract, main text, figure captions, tables and supplement** with each other, and look for a baseline or reference value reported with different values in different places. Each mismatch is evidence (a CONTRADICTS or UNDERCUTS link).
- **Compare abstract and highlights with the results and limitations sections.** Headline claims ("we demonstrate", "predictive", "optimal", "material-independent") often exceed what the body shows, and sometimes the body concedes the opposite.
- **Count samples, repeats, micrographs and error bars.** Record `sample_count` and flag n = 1 generalizations.
- **Look for the missing control** that would separate the claimed cause from the obvious alternative.

## YAML pitfalls (all hit in practice)

| Problem | Fix |
|---|---|
| `arxiv: 2610.27240` becomes a float | `arxiv: "2610.27240"` |
| Commas, colons or semicolons inside `{...}` flow mappings break parsing | Quote the string: `description: "No XRD, DSC or Tg."` |
| `value: 13.18e22` is read as a string | Use a dot and a signed exponent: `1.318e+23`, `6.12e+7`, `3.5e-4` |
| `YES` / `NO` become booleans | `validity: "YES"`, `validity: "NO"` |
| `value` is required and must be a number | Ranges become two entries (min/max); put text in `condition` |
| `symbol` must be an identifier | Letters, digits, underscores: `BG_Mg`, not `B/G (Mg)`; unique within one evidence item |
| `formula` uses Python syntax | `**` for powers, `abs()`, `and`; `2*C13**2 < C33*(C11 + C12)` |
| Relation to an entity (ANALOG_OF) | Allowed; add `note: "object is an entity, not a statement"` |
| Dangling id in `discharged_by` or a relation | render.py reports it; fix it before reporting |

## Common mistakes

- Transcribing statements without concerns or relations: the chain then cannot show why a verdict holds.
- Writing statement text that only makes sense in context ("this shows…"); each text must stand alone.
- Mixing up OBSERVATION (what was measured) and CLAIM (what is concluded); keep the numbers in the observation.
- Confusing `author_certainty` (the authors' stance) with `validity` (your verdict).
- Marking a rule of thumb as CITATION when the citation only names it; an empirical correlation stays EMPIRICAL_CORRELATION even if cited.
- Marking outside-knowledge links as ANNOTATOR instead of ANNOTATOR_BACKGROUND.
- Rating support strength by feel instead of from the five link criteria, or marking every link essential.
- Citing a statement as support for itself or skipping SUPPORTS links from CLAIMs to the HYPOTHESIS.
- Reporting completion before linkml-validate and render.py both pass.
- Overstating your own certainty in the summary: say that the file is a draft, which verdicts rest on figures you could not see, and which links are background knowledge.
