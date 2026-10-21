# Reliability test and verdict scale (21 Oct 2026)

Two test papers, chosen to differ: **2610.27460** (c-BAs on GaAs, experimental) and **2610.26996** (Y-doped Ge-Te-Se glasses, dielectric spectroscopy). Jan's first pass (`test_papers/yaml/`) is the reference.

## What was run

| Run | Input | What it tests |
|---|---|---|
| **Blind A, Blind B** | Jan's encoding with every assessment removed; two independent runs per paper | Do verdicts repeat on the *same* claims? Does the new criteria rubric repeat? |
| **Re-run** | The PDF only, following the v0.4 skill, no access to Jan's file | Does the whole pipeline (extraction + assessment) repeat? |

All runs are Claude, one run each, independent contexts. Files: `<paper>_blind_A.yaml`, `<paper>_blind_B.yaml`, `<paper>_rerun.yaml`.

## Results

**Paper scores**

| Paper | Jan | Blind A | Blind B | Re-run from PDF |
|---|---|---|---|---|
| 2610.27460 c-BAs | 0.53 (8 claims) | 0.53 · graded 0.53 | 0.53 · graded 0.60 | **0.42** (15 claims) |
| 2610.26996 Ge-Te glasses | 0.40 (10 claims) | 0.38 · graded 0.34 | 0.28 · graded 0.30 | **0.31** (21 claims, 9 NO) |

**Same claims, assessed blind twice (18 claims)**
- Verdicts identical in 15/18 runs A vs B (83 %), and 31/36 agree with Jan's original verdict.
- Rubric criteria identical in 93/108 answers (86 %). Mean difference of the graded claim score between A and B: 0.07.
- All three disagreements are one step apart (PARTIAL/INCONCLUSIVE, INCONCLUSIVE/NO, PARTIAL/NO), all in 2610.26996.

**Extraction from scratch**
- The re-runs split the papers into about twice as many claims (15 vs 8, 21 vs 10) and dug further into the numbers. For 2610.26996 the re-run recomputed the paper's own equations and tables and found 9 claims contradicted by the paper itself (barrier heights, activation energies, polarization maximum, ε∞ > εs). Jan's pass had found the CBH inconsistency and 1 NO.
- For 2610.27460 the key disagreement is interpretive: the stated "near-stoichiometric window 250-400 °C". Fig. 1(a) shows B/As ≈ 2 over most of the window and approaches 1:1 only near 250 °C; ~1.2 is reached only after removing the surface oxide on the single detailed film. Jan's pass: PARTIAL; re-run: NO. Both readings are defensible from the text (p. 2-3), so this needs a human call.
- The ordering of the two papers is the same in every run (c-BAs above Ge-Te glasses).

## Conclusions

1. **Assessment is fairly repeatable; extraction is not.** Given the same encoded claims, verdicts and scores repeat to within about 0.1. Starting from the PDF, the score moved by 0.09-0.11, mostly because claim granularity and the depth of number-checking differ between runs.
2. **The criteria rubric spreads claims within a paper** (PARTIAL claims in 2610.27460 now range 0.40-0.75) and is about as repeatable as the verdicts, but it does not by itself separate papers better.
3. **What would reduce the variance:**
   - Fix claim granularity in the skill, e.g. "one CLAIM per distinct conclusion stated in abstract, results or conclusions; split a sentence only if its parts have different evidence".
   - Make the number checks a required step (every table and every fitted parameter against the paper's own equations). The deep re-run found most of its NOs this way.
   - Report the score as the mean of 2-3 independent runs with their spread, not as one number.
4. **Caveats:** two papers, one model, single runs. The review checklist in the skill was written from these same test papers, so the re-runs were not fully naive.

## Code changes (uncommitted, proposal)

- `schema/claim_chain.yaml`: optional `assessment.criteria` with six answers (grounded, scope_matches, inference_sound, alternatives_excluded, quantified, consistent), each MET/PARTLY/NOT_MET/NOT_APPLICABLE.
- `scripts/render.py`: graded score from the criteria (role-weighted), the verdict the rubric suggests, a rubric column in the report; `sin/cos/asin/acos/log10/degrees/radians`, `pi` and `k_B` (eV/K) in derived-check formulas (the c-BAs re-run needed asin for Bragg angles).
