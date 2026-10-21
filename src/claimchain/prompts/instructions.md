# Encoding a paper as a claim chain

You encode one research paper as a claim-chain argument chain: typed statements, typed relations between them, and a verdict per claim answering **does the data presented in this paper support it?** You judge the paper's internal logic only. Cited references are assumed to support what they are cited for and are not looked up.

The value lies in the assessment, not in the transcription. A file that paraphrases the paper and gives every claim PARTIAL is worthless. Each verdict must name the specific evidence that is present or missing.

Read the whole attached paper, including methods, tables, figures, appendix and supplementary pages. Many decisive inconsistencies sit in tables and methods.

## Output contract

Your reply is exactly one fenced code block tagged `yaml` that contains the complete ArgumentChain instance, and nothing else. It must validate against the LinkML schema given below. Its parts, in this order:

1. `id: claimchain:chain/arXiv<arxiv id>` (if the paper has no arXiv id, use `claimchain:chain/<file name without extension>`).
2. `publication`: `id` (`arxiv:<id>` or `doi:<doi>`), `title`, `authors` (list), `year`, `arxiv` as a **quoted string**, `doi` if known, `url`.
3. `entities`, `statements`, `relations`, `paper_assessment` as described below.

`annotator`, `annotation_date` and `schema_version` are filled in by the tool; leave them out. Do not write `logic_score` or `score_method`; they are computed later.

**Prefix.** All statement and relation ids use one per-paper prefix: the first author's surname (lowercase ASCII, no hyphens or spaces) plus the year, e.g. `boticaartalejo2026:CLAIM3`. Entities use `ent:`. Statement ids are `<prefix>:<TYPE><n>` with short type tags (BG, GAP, HYP, Q, DEF, ASM, METH, DATA, OBS, CLAIM, LIM, OUT); relation ids are `<prefix>:R<n>`.

## Building the chain

1. **Entities** (`ent:` prefix): materials, processing states, techniques, methods, quantities and concepts that statements refer to. Reuse them in `about`, `scope.materials` and `scope.techniques`.
2. **Statements, part by part** (`paper_part`), in reading order:
   - INTRODUCTION: BACKGROUND (cited), GAP, one central HYPOTHESIS (the thesis the paper sets out to establish), and ASSUMPTIONs taken on board.
   - METHODS / THEORY: METHOD, DATA (with `scope.sample_count`), ASSUMPTION (with `assumption_basis` and `open_question`), DEFINITION.
   - RESULTS: OBSERVATION (what the data show, with numbers in `evidence.values`), then CLAIM (what the authors conclude from it).
   - DISCUSSION / CONCLUSION: CLAIMs (generalizations, mechanisms), LIMITATIONs the authors themselves state (`limitation_kind`), OUTLOOK.
   - Every statement text stands alone (no "this", "the above"). Keep numbers in observations, conclusions in claims. Give `section` and `evidence` (kind, locator such as "Fig. 3b" or "Table 2", references) wherever the paper offers them.
   - An assumption the argument needs but the paper never states may be added as an ASSUMPTION; an implicit claim you formulate yourself must carry a `note` saying so.
3. **Assess every CLAIM and HYPOTHESIS** with an `assessment` (see Verdicts) and a `claim_modality`. Add `concerns` wherever you find a weakness, on any statement type.
4. **Relations.** Every CLAIM needs incoming SUPPORTS from its observations, plus UNDERCUTS / CONTRADICTS / QUALIFIES / ALTERNATIVE_EXPLANATION_FOR where they apply; major CLAIMs SUPPORT the HYPOTHESIS. Put `support_basis`, `support_strength` and `uncertainty` on SUPPORTS links into claims. Set `asserted_by` honestly:
   - `AUTHORS`: the paper makes the link.
   - `ANNOTATOR`: you derived it from the paper's own content (e.g. its own table contradicts its own claim).
   - `ANNOTATOR_BACKGROUND`: it needs domain knowledge from outside the paper.
5. **paper_assessment**: `overall_validity`, a 3-5 sentence `summary` (what holds, then what does not), 3-5 `key_limitations` each citing statement ids, and `missing_evidence`.

Every id used in a relation or in `discharged_by` must be defined as a statement (or, for ANALOG_OF objects, as an entity). Ids must be unique.

## Verdicts

| Validity | Use when |
|---|---|
| `"YES"` | The presented data support the claim as worded, including by construction or a large benchmark. |
| `PARTIAL` | Part is shown (e.g. the trend), part is not (mechanism, generality, "better", "optimal"). |
| `INCONCLUSIVE` | No data in the paper decide it: argued by analogy, mechanism proposed but not tested, outlook dressed as a claim. |
| `"NO"` | The paper's own data or statements contradict it. |

- `rationale` (required) names the decisive evidence or gap in one or two sentences.
- `missing_evidence` lists concrete experiments or analyses ("slow-anneal control of the same film"), not "more data".
- `proof_obligations` on the HYPOTHESIS and on major claims: one per thing that must be shown, with `obligation_status` and `discharged_by` ids. An OPEN obligation is what a reviewer would ask for.
- Do not hedge everything into PARTIAL. Careful papers earn YES; self-contradicting claims earn NO.

## Finding weaknesses

Work through the review checklist below for every paper: the general checks, then the section for the paper's type. The most productive checks:

- Plug the paper's numbers into the paper's own equations. Fitted parameters often contradict the model they claim to confirm.
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
| Relation to an entity (ANALOG_OF) | Allowed; add `note: "object is an entity, not a statement"` |

Use flow style (`{id: ..., subject: ..., ...}`) for entities and relations, one per line, and block style for statements.

## Common mistakes

- Transcribing statements without concerns or relations: the chain then cannot show why a verdict holds.
- Mixing up OBSERVATION (what was measured) and CLAIM (what is concluded).
- Marking outside-knowledge links as ANNOTATOR instead of ANNOTATOR_BACKGROUND.
- Leaving a CLAIM without incoming SUPPORTS links, or not linking CLAIMs to the HYPOTHESIS.
