# claim-chain report: A non-orthogonal representation for materials based on chemical similarity

Tiago F. T. Cerqueira, Haichen Wang, Silvana Botti, Miguel A. L. Marques (2026), doi:10.1038/s41524-025-01916-8. Generated; do not edit by hand.

## 1. Logic

**Overall: ◐ PARTIAL** · **Logic score: 0.57** · weighted: 0.53 · proof obligations discharged: 0.00 (of 1)  
Score method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting). Weighted: as the logic score, but MAIN_CONCLUSION weighs 3, COUNTER_CLAIM 0 and every other claim or hypothesis 1 (draft weighting).  
Verdicts: 4 YES, 6 PARTIAL, 4 WEAK, 0 INCONCLUSIVE, 1 NO.

A coherent methods paper: all four aims are delivered, and three are restated in the abstract or conclusion. The construction is fully specified, the element-level results are shown against a one-hot control, and the CrabNet benchmark covers 27 datasets against four alternatives, on which the new embedding has the best mean rank. The weak spots are wording rather than logic: the abstract turns "on average the best" into "systematically outperform", the claim of particular strength on small datasets is contradicted by the paper's own table, the unit-sphere description in the abstract conflicts with the Methods, and the analogue-finding claim generalises from two examples. Benchmark spreads over the 8 runs are not given.

**Score from derived verdicts: 0.46**, 6 claim(s) where the derived verdict differs from the annotator's. Method: verdicts derived from the links: an incoming CONTRADICTS gives NO; otherwise the strongest support link decides (STRONG YES, INTERMEDIATE PARTIAL, WEAK WEAK, none INCONCLUSIVE); UNDERCUTS, QUALIFIES or an alternative explanation caps at PARTIAL; CONDITIONALLY_SUPPORTS counts as WEAK at most; an essential link caps the claim at its own strength and at the derived verdict of the claim it comes from. Links without a strength count as INTERMEDIATE. Claims without links keep the annotator's verdict.  

| Statement | Role | Modality | Authors say | Verdict | Derived | Rationale |
|---|---|---|---|---|---|---|
| **ABS1** Pettifor embeddings systematically outperform other commonly used elemental embeddings in compositional machine learning models. | main conclusion | comparative | demonstrated | ◐ PARTIAL | **◔ WEAK** | Best mean rank across 27 benchmarks (1.96 against 2.30 for CGCNN), but it loses to at least one alternative in 15 of them and no run-to-run spread is given. |
| **ABS2** Two-dimensional maps of thermodynamically stable compounds built from the Pettifor embeddings separate material classes according to basic physical properties. | main conclusion | descriptive | demonstrated | ◐ PARTIAL | same | Shown for crystal system and metal versus non-metal; the paper itself shows that magnetic and non-magnetic compounds are not separated. |
| **ABS3** In the non-orthogonal composition space, a chemical composition is defined by a point on the unit sphere. | methodological | conceptual | demonstrated | ◔ WEAK | **✗ NO** | Contradicted by the paper's own Methods for every compound except elementary substances; a wording slip, not a flaw of the method. |
| **CLAIM1** Chemically similar elements cluster in the embedding, purely from substitution patterns and without encoding the periodic table. | intermediate | descriptive | demonstrated | ✓ YES | **◐ PARTIAL** | Fig. 2 shows the grouping against a one-hot control; robustness to UMAP parameters is shown in the ESI. |
| **CLAIM2** The embedding separates degrees of similarity that a one-dimensional scale cannot, e.g. Se is much closer to S than O is, although both are nearest neighbours of S on the modified Pettifor scale. | intermediate | comparative | demonstrated | ✓ YES | same | Follows from the construction and is shown by the Table 1 distances; illustrated for three elements only. |
| **CLAIM3** Used as input to CrabNet, the Pettifor embedding yields on average the best results of the five embeddings while remaining simple and interpretable. | main conclusion | comparative | demonstrated | ◐ PARTIAL | same | The mean rank is best, but margins are often a few percent and no spread over the 8 runs is given to show they are significant. |
| **CLAIM4** The Pettifor embedding performs particularly well for small- and medium-sized datasets. | intermediate | comparative | demonstrated | ✗ NO | same | On the three smallest datasets it ranks 4th, 3rd and 2nd; its wins lie between about 3 400 and 60 000 entries. |
| **CLAIM5** The improved performance suggests that the representation captures the chemical relationships relevant to materials properties, which makes it valuable where training data are scarce. | mechanistic interpretation | causal | proposed | ◔ WEAK | **✗ NO** | The first half follows plausibly from the benchmark; the data-scarce half rests on CLAIM4, which the table does not support. |
| **CLAIM6** Despite the diversity of the data set, the map gives a reasonable structural separation of compounds and an excellent separation of metals and non-metals. | main conclusion | descriptive | demonstrated | ◐ PARTIAL | same | Visible in Figures 4 and 5, but judged by eye and dependent on UMAP parameters, as the authors note. |
| **CLAIM7** The missing separation of magnetic compounds suggests that magnetism will be much harder to predict with machine learning than the other properties. | intermediate | generalization | proposed | ◔ WEAK | **? INCONCLUSIVE** | A two-dimensional UMAP projection says little about what a model trained on the full embedding can learn; no model is trained on magnetism. |
| **CLAIM8** The information can probably be compressed into a much smaller feature vector. | intermediate | descriptive | demonstrated | ✓ YES | same | Follows directly from the PCA counts. |
| **CLAIM9** Proximity in the embedding space correlates with comparable physical properties, so the embedding can find functional analogues of known materials without any calculation. | main conclusion | generalization | demonstrated | ◔ WEAK | **? INCONCLUSIVE** | Two illustrative cases, no systematic test of how well distance predicts property similarity. |
| **CLAIM10** The uniqueness measure highlights compounds with few similar alternatives that may merit attention in experiments. | intermediate | conceptual | proposed | ◐ PARTIAL | same | A definition with two examples; its usefulness for experiments is argued, not shown. |
| **CON1** The fingerprint can be used to create structure or property maps that span families of materials or the entire material space. | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | Restates the map results, which hold for structure and metallicity but not for magnetism. |
| **CON2** The human-generated fingerprint can compete with machine-learned opaque representations as input to machine learning models. | intermediate | comparative | demonstrated | ✓ YES | same | "Can compete" is exactly what Table 2 shows; more cautious than the abstract. |

**Support links tested on the five criteria** (directness, sufficiency, controls, alternatives, scope match; ✓ met, ◐ partly, ✗ not met, – not applicable):

| Link | Criteria | Strength | Note |
|---|---|---|---|
| OBS1 → CLAIM1 (essential) | ✓✓✓–✓ | strong | One-hot map as control; UMAP robustness in the ESI. |
| OBS2 → CLAIM2 (essential) | ✓✓✓–✓ | strong | Direct distances against ElMD, C-GRID, Mat2Vec, Magpie and CGCNN. |
| OBS4 → CLAIM3 (essential) | ✓◐✓◐✓ | intermediate | Same model, same data, four alternative embeddings; no run-to-run spread, so small margins could be noise. |
| OBS4 → ABS1 (essential) | ✓◐✓◐◐ | weak (annotator: intermediate) | 'Systematically' is wider than the 12 of 27 wins in Table 2. |
| OBS5 → CLAIM6 (essential) | ✓◐––◐ | intermediate | Judged by eye on one UMAP projection. |
| OBS5 → CLAIM7 (essential) | ✗◐–◐◐ | unsupported (annotator: weak) | A 2D projection is not a test of learnability. |
| OBS6 → CLAIM8 (essential) | ✓✓––✓ | strong |  |
| OBS7 → CLAIM9 (essential) | ✓✗✗◐◐ | unsupported (annotator: weak) | Two chosen examples, no systematic distance-property test. |

**Golden thread** (each aim from the introduction to the end of the paper):

| Aim | Gap | Method | Result | Claim (verdict) | Outcome |
|---|---|---|---|---|---|
| **AIM1** The paper builds a fingerprint of a compound from its composition and crystal structure only, such that distances between fingerprints reflect the similarity of compounds. | GAP1 | METH2 | - | CON1 (◐) | DELIVERED |
| **AIM2** The paper introduces a composition embedding in a non-orthogonal space whose axis angles encode element similarity from ICSD substitution statistics, combining the efficiency of learned embeddings with transparency. | GAP2 | METH1 | - | CLAIM1 (✓) | NOT RESTATED |
| **AIM3** The paper shows that the representation gives interpretable maps of material space. | - | - | - | CLAIM6 (◐) | DELIVERED |
| **AIM4** The paper shows that the representation provides powerful embeddings for machine learning. | GAP2 | - | - | CLAIM3 (◐) | DELIVERED |

Outcomes: DELIVERED, NOT RESTATED (delivered but absent from the conclusion and abstract), METHOD ONLY (carried out but no result shown), DROPPED (nothing delivers it).

**Main conclusions no aim or hypothesis promised:** CLAIM9.

**Presented as demonstrated, but the verdict is weak, inconclusive or no:** ABS3 (WEAK), CLAIM4 (NO), CLAIM9 (WEAK).

**Recomputed checks:**

- **METH2** 61 x 4 = 244 ✓ satisfied (recomputed)
- **OBS4** Pettifor has the best mean rank ✓ satisfied (recomputed)
- **OBS4** Pettifor is best in most benchmarks ✗ not satisfied (recomputed)

**Statements per paper part:**

| Part | Statements |
|---|---|
| abstract | ABS1, ABS2, ABS3 |
| introduction | BG1, GAP1, GAP2, AIM1, AIM2, AIM3, AIM4, ASM1 |
| methods | METH1, METH2, METH3 |
| results | OBS1, OBS2, CLAIM1, CLAIM2, OBS3, OBS4, CLAIM3, CLAIM4, CLAIM5, OBS5, CLAIM6, CLAIM7, LIM2 |
| discussion | OBS6, OBS7, CLAIM8, CLAIM9, OBS8, CLAIM10 |
| conclusion | CON1, CON2, LIM1 |

Causal claims (check against correlational evidence): CLAIM5.

## 2. Limitations

- No run-to-run spread in Table 2, so small margins cannot be judged (CLAIM3).
- The small-dataset advantage is not in the table (CLAIM4).
- Abstract wording stronger than the results (ABS1, ABS3).
- Property similarity from embedding distance rests on two examples (CLAIM9).

**Stated by the authors:**

- **LIM1** (data): The similarity data lack information for rare gases and some actinides, and ICSD bias may create spurious correlations.
- **LIM2** (method): The shape of the two-dimensional maps depends on the UMAP parameters, and two dimensions may distort distances.

**Assumptions the argument rests on:**

- **ASM1** (-): Element substitution counts in ICSD measure chemical similarity, although the database is biased and incomplete. *Open question:* -

**Flagged by the annotator:**

- **ABS1** overclaim (medium): Table 2 shows the Pettifor embedding best (or tied) in 12 of 27 benchmarks, ahead of one-hot in 19 and of CGCNN in 17; the results section says 'on average the best', which the table supports, but not 'systematically'.
- **ABS3** internal inconsistency (low): Methods state that composition vectors are in general not on the unit sphere but on an (N-1)-dimensional simplex, because they are normalised with the L1 norm; only elementary substances lie on the unit sphere.
- **METH1** ad hoc parameter (low): The exponent alpha = 1/2 is taken from an earlier procedure; its effect on the results is not shown.
- **METH2** ad hoc parameter (low): Equal weights for composition and structure are chosen for simplicity; other weights are not tested.
- **METH3** missing quantification (medium): The spread over the 8 runs is not reported, so it is unclear which of the many small differences in Table 2 are significant.
- **OBS5** missing quantification (low): Separation is judged by eye; no clustering or classification score is given.
- **CLAIM9** overgeneralization (medium): A general correlation is stated from two hand-picked cases; the paper's own hBN-graphite pair (close neighbours with very different electronic properties) is a counterexample that is not discussed as such.

**Local checks per part** (issues found; failed derived checks count as arithmetic):

| Part | Completeness | Arithmetic | Consistency | Argument | High or critical |
|---|---|---|---|---|---|
| abstract | 0 | 0 | 1 | 1 | 0 |
| methods | 1 | 0 | 0 | 2 | 0 |
| results | 1 | 0 | 0 | 0 | 0 |
| discussion | 0 | 0 | 0 | 1 | 0 |

## 3. Missing evidence

- Standard deviations over the 8 CrabNet runs
- A systematic test of distance versus property similarity over many compound pairs
- A quantitative separation score for the maps instead of visual judgement

**Open proof obligations:**

- **CLAIM3** (open, medium): Report the standard deviation over the 8 runs for each benchmark and embedding.

**Per statement:**

