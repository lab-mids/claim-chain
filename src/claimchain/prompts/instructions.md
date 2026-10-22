# Encoding a paper as a claim chain

You encode one research paper as a claim-chain argument chain: typed statements, typed relations between them, and a verdict per claim answering **does the data presented in this paper support it?** You judge the paper's internal logic only. Cited references are assumed to support what they are cited for and are not looked up.

The value lies in the assessment, not in the transcription. A file that paraphrases the paper and gives every claim PARTIAL is worthless. Each verdict must name the specific evidence that is present or missing, and each step should say *why* the evidence implies the claim (the warrant).

Read the whole attached paper, including methods, tables, figures, appendix and supplementary pages. Many decisive inconsistencies sit in tables and methods.

## Output contract

Your reply is exactly one fenced code block tagged `yaml` that contains the complete ArgumentChain instance, and nothing else. It must validate against the LinkML schema given below. Its parts, in this order:

1. `id: claimchain:chain/arXiv<arxiv id>` (if the paper has no arXiv id, use `claimchain:chain/<file name without extension>`).
2. `publication`: `id` (`arxiv:<id>` or `doi:<doi>`), `title`, `authors` (list), `year`, `arxiv` as a **quoted string**, `doi` if known, `url`.
3. `entities`, `cited_works` (optional), `statements`, `relations`, `paper_assessment` as described below.

`annotator`, `annotation_date` and `schema_version` are filled in by the tool; leave them out. Do not write `logic_score`, `score_method`, `weighted_logic_score` or `obligation_coverage`; they are computed later.

**Prefix.** All statement and relation ids use one per-paper prefix: the first author's surname (lowercase ASCII, no hyphens or spaces) plus the year, e.g. `boticaartalejo2026:CLAIM3`. Entities use `ent:`. Statement ids are `<prefix>:<TYPE><n>` with short type tags (BG, GAP, HYP, Q, DEF, ASM, METH, DATA, OBS, CLAIM, LIM, OUT); relation ids are `<prefix>:R<n>`; cited works are `<prefix>:ref<n>`.

## Building the chain

1. **Entities** (`ent:` prefix): materials, processing states, techniques, methods, quantities and concepts that statements refer to. Reuse them in `about`, `scope.materials` and `scope.techniques`.
2. **Cited works** (optional, `<prefix>:ref<n>`): only the references the argument actually leans on (an inference rule, a validated baseline), each with `cited_for` saying what it is assumed to provide. Background citations can stay as plain numbers in `evidence.references`.
3. **Statements, part by part** (`paper_part`), in reading order:
   - INTRODUCTION: BACKGROUND (cited), GAP, one central HYPOTHESIS (the thesis the paper sets out to establish), and ASSUMPTIONs taken on board.
   - AIMs: what the paper promises to do or deliver ("In this work we ..."), one per promise, including the promised payoff. Many papers state aims rather than a hypothesis; then AIMs replace the HYPOTHESIS. A gap the contributions imply but the text never states is a GAP with a `note` saying so.
   - METHODS / THEORY: METHOD, DATA (with `scope.sample_count`), ASSUMPTION (with `assumption_basis` and `open_question`), DEFINITION.
   - RESULTS: OBSERVATION (what the data show, with numbers in `evidence.values`), then CLAIM (what the authors conclude from it).
   - DISCUSSION / CONCLUSION: CLAIMs (generalizations, mechanisms), LIMITATIONs the authors themselves state (`limitation_kind`), OUTLOOK, open QUESTIONs (with `priority`).
   - Every statement text stands alone (no "this", "the above"). Keep numbers in observations, conclusions in claims. Give `section` and `evidence` (kind, locator such as "Fig. 3b" or "Table 2", references) wherever the paper offers them.
   - An assumption the argument needs but the paper never states may be added as an ASSUMPTION; an implicit claim you formulate yourself must carry a `note` saying so.
4. **Classify every CLAIM and HYPOTHESIS:**
   - `claim_role`: MAIN_CONCLUSION (what the abstract and conclusions sell; usually the HYPOTHESIS and 1-4 claims), INTERMEDIATE, QUANTITATIVE_SUPPORT, MECHANISTIC_INTERPRETATION, METHODOLOGICAL, or COUNTER_CLAIM (the paper's own result against its conclusion). The weighted score counts main conclusions three times and counter-claims not at all, so be deliberate.
   - `author_certainty`: how the **authors** present it (DEMONSTRATED, PREDICTED, PROPOSED, SPECULATIVE). This is their stance, not your verdict; a gap between the two is often the finding.
5. **Warrants.** For every claim whose support is not self-evident, write the inference rule that links evidence to claim: on the statement (for its own evidence) or on the SUPPORTS relation (for statement → statement). Give `warrant_basis` honestly: CITATION, DEFINITION, EMPIRICAL_CORRELATION (rules of thumb such as Pugh's ratio), DOMAIN_CONVENTION, AUTHOR_ARGUMENT, or UNSTATED (the paper uses the rule without saying so). A multi-step inference becomes intermediate statements, each with its own warrant.
6. **Derived checks.** Where the paper reports numbers and a criterion or derived value, make it recomputable: give each value a `symbol` and add a `derived_checks` entry with a human-readable `expression`, a Python `formula` over the symbols, and the reported `result` or `satisfied`. Examples: stability criteria, percentage differences quoted in the text, a fitted parameter plugged into the paper's own equation. A check that fails to recompute is a finding: record it as a concern, not by changing the numbers.
7. **Assess every CLAIM and HYPOTHESIS** (AIMs get no verdict) with an `assessment` (see Verdicts) and a `claim_modality`. Add `concerns` wherever you find a weakness, on any statement type.
8. **Relations.** Every CLAIM needs incoming SUPPORTS from its observations, plus WEAKENS / CONTRADICTS / QUALIFIES / ALTERNATIVE_EXPLANATION_FOR where they apply; major CLAIMs SUPPORT the HYPOTHESIS. Use CONDITIONALLY_SUPPORTS for an untested hypothesis the argument leans on. Put `support_basis`, `support_strength` and `uncertainty` on SUPPORTS links into claims; `support_strength` rates the link (does this evidence bear on this claim?), `uncertainty` the evidence itself (how precise is it?). Set `asserted_by` honestly:
   - `AUTHORS`: the paper makes the link.
   - `ANNOTATOR`: you derived it from the paper's own content (e.g. its own table contradicts its own claim).
   - `ANNOTATOR_BACKGROUND`: it needs domain knowledge from outside the paper.
   Test every SUPPORTS and CONDITIONALLY_SUPPORTS link into a claim on five criteria in `link_criteria` (MET, PARTLY, NOT_MET or NOT_APPLICABLE, with a short `criteria_note`): **directness** (does the evidence measure the claimed quantity, or only a proxy?), **sufficiency** (samples, repeats, statistics, error analysis), **controls** (confounders, a fair baseline), **alternatives** (other plausible explanations excluded?) and **scope_match** (does the claim stay within what was tested?). Set `support_strength` to match: all met STRONG; one or two partly INTERMEDIATE; one failed or more than two partly WEAK; directness or scope failed UNSUPPORTED (the link does not carry the claim at all). Mark a link `essential: true` only if the claim cannot hold without it; render.py caps a claim at its weakest essential link and at the verdict of the claim that link comes from, and reports where its derived verdict differs from yours.
   Follow the golden thread: a DELIVERS link from each method, observation or claim that carries out an AIM to that AIM, and a RESTATES link from each conclusion or abstract sentence to the earlier statement it restates. Give both statements their `author_certainty`, so render.py can flag claims that grow more certain at the end and aims that are dropped or not restated. `paper_part` records where a statement appears, even if it does a different job there (a result reported in the discussion stays DISCUSSION; say so in a `note`).
9. **paper_assessment**: `overall_validity`, a 3-5 sentence `summary` (what holds, then what does not), 3-5 `key_limitations` each citing statement ids, and `missing_evidence`.

Every id used in a relation or in `discharged_by` must be defined as a statement (or, for ANALOG_OF objects, as an entity). Ids must be unique.

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
- If a verdict rests on a figure you can judge only from its caption, say so in the rationale.
- Judge each claim on its own evidence. Do not hedge everything into PARTIAL: careful papers earn YES, and self-contradicting claims earn NO.

## Finding weaknesses

Work through the review checklist below for every paper: the general checks, then the section for the paper's type. The most productive checks:

- Plug the paper's numbers into the paper's own equations, as derived checks. Fitted parameters often contradict the model they claim to confirm.
- Check normalisation and units of compared quantities (per cell vs per atom, per mass vs per volume).
- **Check each part locally**, as a reviewer reading it on its own: *completeness* (is everything needed to reproduce or judge this part reported? REPRODUCIBILITY), *arithmetic* (can every stated number be derived from the description? ARITHMETIC, plus a derived check), *consistency* (does the text agree with the paper's own tables, lists and earlier sections? INTERNAL_INCONSISTENCY). Give every concern a `priority`; render.py counts them per part.
- **Compare abstract, main text, figure captions, tables and supplement** with each other, and look for a baseline or reference value reported with different values in different places. Each mismatch is evidence (a CONTRADICTS or WEAKENS link).
- Compare abstract and highlights with the results and limitations sections. Headline claims ("we demonstrate", "predictive", "optimal", "material-independent") often exceed what the body shows, and sometimes the body concedes the opposite.
- Count samples, repeats, micrographs and error bars. Record `sample_count` and flag n = 1 generalizations.
- Look for the missing control that would separate the claimed cause from the obvious alternative.

## YAML rules

| Problem | Rule |
|---|---|
| `arxiv: 2610.27240` becomes a float | `arxiv: "2610.27240"` |
| Commas, colons or semicolons inside `{...}` flow mappings break parsing | Quote the string: `description: "No XRD, DSC or Tg."` |
| `value: 13.18e22` is read as a string | Use a dot and a signed exponent: `1.318e+23`, `6.12e+7`, `3.5e-4` |
| `YES` / `NO` become booleans | `validity: "YES"`, `validity: "NO"` |
| `value` is required and must be a number | Ranges become two entries (min/max); put text in `condition` |
| `symbol` must be an identifier | Letters, digits, underscores: `BG_Mg`, not `B/G (Mg)`; unique within one evidence item |
| `formula` uses Python syntax | `**` for powers, `abs()`, `and`; `2*C13**2 < C33*(C11 + C12)` |
| Relation to an entity (ANALOG_OF) | Allowed; add `note: "object is an entity, not a statement"` |

Use flow style (`{id: ..., subject: ..., ...}`) for entities and relations, one per line, and block style for statements.

## Common mistakes

- Transcribing statements without concerns or relations: the chain then cannot show why a verdict holds.
- Mixing up OBSERVATION (what was measured) and CLAIM (what is concluded).
- Confusing `author_certainty` (the authors' stance) with `validity` (your verdict).
- Marking a rule of thumb as CITATION when the citation only names it; an empirical correlation stays EMPIRICAL_CORRELATION even if cited.
- Marking outside-knowledge links as ANNOTATOR instead of ANNOTATOR_BACKGROUND.
- Rating support strength by feel instead of from the five link criteria, or marking every link essential.
- Leaving AIMs without DELIVERS links, or a conclusion sentence without a RESTATES link to the claim it repeats.
- Leaving a CLAIM without incoming SUPPORTS links, or not linking CLAIMs to the HYPOTHESIS.
