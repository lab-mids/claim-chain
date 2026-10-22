# Ideas: Soroush

*First drafted from Markus's notes of the 21 Oct 2026 team discussion, now filled in by Soroush.*

## Approach: quantify the supporting evidence

Rate how strongly each piece of evidence supports the claim it is attached to. The rating is not a gut feeling: every link is tested against five fixed criteria, and the overall strength follows from those tests. Claim verdicts are then derived from the strength of their incoming links.

## How it maps to the format

- Each relation gets a `support_strength` field.
- I propose **four levels** instead of three:

  | Level | Meaning | Schema v0.3 equivalent |
  |---|---|---|
  | `STRONG` | Evidence directly measures the claim, with adequate statistics and controls | `STRONG` |
  | `MODERATE` | Relevant evidence, but one or two criteria are weak | `INTERMEDIATE` |
  | `WEAK` | Indirect, thin, or uncontrolled evidence | `WEAK` |
  | `UNSUPPORTED` | The link does not carry the claim at all (wrong quantity, wrong scope, no control) | *(missing)* |

  `UNSUPPORTED` matters because papers often cite evidence that does not actually bear on the claim. With only three levels, such links end up as `WEAK`, which overstates them. If the team prefers to keep three levels, `MODERATE` maps to `INTERMEDIATE`, and `UNSUPPORTED` links could instead be recorded as relation type `UNRELATED`.

- It sits alongside `support_basis` (qualitative, quantitative, logical) and `uncertainty` (low, medium, high) from the blackboard discussion.

## What I tried

I wrote an LLM prompt that performs the full analysis on one paper and tested it on two papers. The prompt is in [`prompt_v3.txt`](prompt_v3.txt).

### The prompt in five steps

1. **Extract claims** (C1, C2, ...), typed as `MAIN`, `SUB`, `BACKGROUND` or `METHOD`, each with a verbatim quote, location and scope.
2. **Extract evidence** (E1, E2, ...): kind, location, quote, key numbers. Anything missing is written as `NOT REPORTED`.
3. **Build the argument map**: links (L1, L2, ...) with relation (`SUPPORTS`, `PARTIALLY SUPPORTS`, `CONTRADICTS`, `UNRELATED`), a one-sentence warrant, and hidden assumptions (A1, A2, ...).
4. **Score each link** on five criteria, each `PASS`, `WEAK` or `FAIL`:
   - **Directness:** does the evidence measure the claimed quantity, or only a proxy?
   - **Sufficiency:** enough samples, repeats, statistics?
   - **Controls:** were confounders and baselines addressed?
   - **Alternatives:** are other explanations ignored?
   - **Scope:** does the claim stay within what was tested?

   These give the overall `support_strength`.
5. **Propagate to claims**: `SUPPORTED`, `PARTIALLY SUPPORTED`, `WEAKLY SUPPORTED`, `UNSUPPORTED` or `CONTRADICTED`.

Outputs: verdict summary, claim table, link table, two Mermaid flowcharts (a one-page summary and a detailed map), JSON, and questions for the authors.

Two extra rules turned out to be important:
- Numbers the model calculates itself are marked `computed`, so they are not mistaken for reported values.
- The model must actively compare abstract, main text, captions, tables and supplement for inconsistencies. **Both test papers contained one.**

### Test 1: MultiMat (Moro et al. 2025, Newton)

Multimodal pre-training for crystal property prediction and materials discovery.

- The accuracy gain over the PotNet baseline is real in the authors' setup, but "state of the art" rests on a single in-house comparison.
- **Biggest gap:** there is no unimodal pre-training control, so the gain cannot be attributed to multimodality rather than to pre-training itself.
- The discovery test selects the best of n candidates using their *true* spectrum, so the improving trend is guaranteed by construction.
- The supplement contradicts the main text: methods called "on par" are 6 to 9% worse on band gap.

Detailed flowchart: [`examples/multimat_argument_map.mmd`](examples/multimat_argument_map.mmd)

### Test 2: Supervised Contrastive Learning (Khosla et al. 2020, NeurIPS)

- SupCon beats cross-entropy in every comparison, and good controls rule out batch size, epochs and two-stage training.
- **Biggest gap:** each gain is 0.5 to 1.1 points from a single run, while the paper's own cross-entropy baseline appears as 77.1, 77.6, 78.2 and 78.24% in different tables.
- The Fig. 6 caption claims stable calibration under corruption; the paper's own Table 6 shows the opposite (`CONTRADICTED`).
- The record claim drops from 0.8 to 0.5 points against a baseline with matched augmentation.

Summary flowchart: [`examples/supcon_main_claims.mmd`](examples/supcon_main_claims.mmd)
Detailed flowchart: [`examples/supcon_argument_map.mmd`](examples/supcon_argument_map.mmd)

To view the charts, paste the `.mmd` code into [mermaid.live](https://mermaid.live).

### Lessons

- The five criteria make the strength rating reproducible: two readers may disagree on a verdict, but they can point to the exact criterion they disagree on.
- Missing statistics (single runs, no error bars) was the most common weakness in both papers. "Sufficiency" was the criterion that failed most often.
- Hidden assumptions are where the real gaps sit. Both biggest gaps were unstated assumptions, not wrong numbers.
- For readers outside the field, a separate one-page summary chart works much better than a single detailed map.

## Open questions

- **Overlap:** should `support_strength` and `uncertainty` both be kept? My suggestion: `support_strength` describes the *link* (does this evidence bear on this claim?), while `uncertainty` describes the *evidence itself* (how precise is the measurement?). A precise measurement of the wrong quantity is low uncertainty but `UNSUPPORTED`. So both are needed.
- **Criteria:** answered by the five criteria above. The blackboard example (statistics = strong, visual = intermediate, argument = weak) fits better as `support_basis` than as strength, since a statistical result can still fail on controls or scope.
- **Propagation:** I use the weakest-link rule: *a main claim cannot be stronger than its weakest essential sub-claim.* "Essential" has to be marked explicitly, otherwise one minor weak sub-claim drags every main claim down.
- **Three or four levels:** see the table above.
- **Next step:** align the prompt's JSON output with `schema/claim_chain.yaml`, so its results can go straight into `scripts/render.py`.
