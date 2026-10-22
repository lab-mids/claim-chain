# Showcase: a well-regarded paper and a retracted paper

The two papers test whether the score separates good logic from bad logic. Both are encoded in schema v0.6 and scored with `scripts/render.py`. The PDFs are not in git (`*.pdf` is ignored).

| | Cerqueira et al. 2026 | Singh et al. 2023 |
|---|---|---|
| Paper | *A non-orthogonal representation for materials based on chemical similarity*, npj Comput. Mater. 12:48, doi:10.1038/s41524-025-01916-8 | *Characterization of Microstructure and Mechanical Properties of Cast Materials using Advanced Techniques*, E3S Web Conf. 430, 01111, doi:10.1051/e3sconf/202343001111 (retracted) |
| Chain | `cerqueira2026_pettifor_embedding.yaml` | `singh2023_cast_materials.yaml` |
| Claims | 15 | 14 |
| Verdicts | 4 YES, 6 PARTIAL, 4 WEAK, 1 NO | 2 PARTIAL, 11 INCONCLUSIVE, 1 NO |
| **Logic score** | **0.57** | **0.27** |
| Weighted score | 0.53 | 0.26 |
| Derived score (from links) | 0.46 | 0.27 |
| Golden thread | 4 aims delivered, 3 restated | 4 aims "delivered", but every delivering claim is unsupported |
| Demonstrated claims with weak, inconclusive or no verdict | 3 of 15 | 12 of 14 |
| High or critical issues found by the per-part checks | 0 | 7 |

The two papers are about 0.3 apart on every score. Their profiles also differ in kind.

**The good paper's problems are about wording.**
- The abstract turns "on average the best" into "systematically outperform". Recomputed from Table 2, the new embedding is best in 12 of 27 benchmarks, and best by mean rank (1.96 against 2.30 for CGCNN).
- The paper says the embedding does "particularly well for small datasets". Its own table contradicts this: it ranks 4th, 3rd and 2nd on the three smallest datasets.
- The abstract places compositions "on the unit sphere", but the Methods say they lie on a simplex.
- The claim that it finds functional analogues rests on two examples.
- The construction, controls and benchmark are sound.

**The retracted paper's problems are about substance.**
- The results are one row of values for each of three different alloys.
- Every main conclusion is asserted with no data behind it: the Hall-Petch trend, the "strong correlations" from a statistical analysis that is never reported, the effect of casting parameters that are never given, and the advantage of advanced techniques with no baseline.
- The abstract and the conclusion restate all of these as demonstrated.
- The per-part checks found:
  - a discussion claim that contradicts the paper's own table (A356 called highly ductile at 5%, against 30% for SS316)
  - a wrong Hall-Petch equation
  - nanoindentation hardness given in Vickers units
  - a corrosion figure with no method behind it
  - a literature review whose 14 cited studies do not match the paper's own reference list (found within the paper; nothing was looked up)

## Caveats

- **The first annotation was not blind.** I annotated both papers knowing which one was retracted, since the file names and the watermark said so. See the blind rerun below.
- **Few runs.** One non-blind and one blind run per paper.
- **The absolute scale is not calibrated.** 0.57 for a sound npj paper sits in the middle of the 0.36–0.93 range of the 10 test papers. The separation between the two papers is what this shows, not the absolute value.
- **The golden thread marks the retracted paper's aims as DELIVERED,** because a claim answers each aim, even though every one of those claims is unsupported. An outcome such as "CLAIMED, NOT SUPPORTED", for aims whose delivering claim is INCONCLUSIVE or NO, would show this directly.

## Blind rerun (paper1.pdf, paper2.pdf)

To remove the annotator's knowledge of which paper was retracted, two fresh annotators each saw one paper only, as plain text under a neutral name (`paper1`, `paper2`), with the same prompt kit as `claimchain` (instructions, review checklist, schema, worked examples). The RETRACTED watermark was stripped from paper 2's text. Outputs: `blind/paper1.yaml`, `blind/paper2.yaml`, reports in `blind/generated/`.

| | paper1 (Cerqueira) | paper2 (Singh, retracted) |
|---|---|---|
| Claims assessed | 23 | 18 |
| Verdicts | 4 YES, 11 PARTIAL, 4 WEAK, 3 INCONCLUSIVE, 1 NO | 1 YES, 2 PARTIAL, 2 WEAK, 12 INCONCLUSIVE, 1 NO |
| **Logic score** | **0.51** (non-blind 0.57) | **0.32** (non-blind 0.27) |
| Weighted score | 0.54 (0.53) | 0.30 (0.26) |
| Derived score | 0.45 (0.46) | 0.31 (0.27) |
| Demonstrated claims with weak, inconclusive or no verdict | 5 of 23 | 13 of 18 |

The gap shrinks from about 0.3 to 0.14–0.24 (logic 0.19, weighted 0.24, derived 0.14) but keeps its sign on all three scores. The blind annotators independently found every key issue of the non-blind pass:
- paper 1: "systematically outperform" against 12 of 27 wins, no advantage on the smallest datasets, and the unit-sphere wording against the Methods
- paper 2: "high ductility" at 5%, the wrong Hall-Petch equation, Vickers units from nanoindentation, a colony size tabulated as grain size, and a reference list that does not match the cited studies

They also found more. Paper 1: the MgB2 to Mg4AlB10 distance (0.16) is larger than the composition change alone allows, and the candidate found "without any calculation" rests on a Tc calculation.

The golden thread now separates the papers somewhat: in paper 2, the characterisation aim is METHOD ONLY and the "advanced techniques" aim is NOT RESTATED. But two aims are still DELIVERED by claims rated "?".

## Regenerate

```
for f in showcase_examples/*.yaml; do python scripts/render.py $f showcase_examples/generated/; done
```
