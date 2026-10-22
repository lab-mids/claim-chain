# claim-chain report: A non-orthogonal representation for materials based on chemical similarity

Tiago F. T. Cerqueira, Haichen Wang, Silvana Botti, Miguel A. L. Marques (2026), doi:10.1038/s41524-025-01916-8. Generated; do not edit by hand.

## 1. Logic

**Overall: ◐ PARTIAL** · **Logic score: 0.51** · weighted: 0.54 · proof obligations discharged: 0.40 (of 10)  
Score method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting). Weighted: as the logic score, but MAIN_CONCLUSION weighs 3, COUNTER_CLAIM 0 and every other claim or hypothesis 1 (draft weighting).  
Verdicts: 4 YES, 11 PARTIAL, 4 WEAK, 3 INCONCLUSIVE, 1 NO.

The construction is sound and transparent: the Pettifor embedding is target-independent and interpretable by design, distinguishes neighbours that a one-dimensional scale cannot, and in CrabNet has the best mean rank (1.96) and most wins (12 of 27) in Table 2, competitive with the one learned embedding tested. The headline wording outruns the data: the abstract's 'systematically outperform' meets 8 losses to plain one-hot and 9 to CGCNN, margins are about 1 % without run-to-run spread, and the claim of particular strength on small datasets is contradicted by the same table, where Pettifor wins none of the five smallest. The map results (element, perovskite, Alexandria) and the discovery applications (Si, MgB2, uniqueness) are visual or anecdotal, without metrics or baselines, and the abstract's 'separation by basic physical properties' is undercut by the failed magnetic map.

**Score from derived verdicts: 0.45**, 6 claim(s) where the derived verdict differs from the annotator's. Method: verdicts derived from the links: an incoming CONTRADICTS gives NO; otherwise the strongest support link decides (STRONG YES, INTERMEDIATE PARTIAL, WEAK WEAK, none INCONCLUSIVE); UNDERCUTS, QUALIFIES or an alternative explanation caps at PARTIAL; CONDITIONALLY_SUPPORTS counts as WEAK at most; an essential link caps the claim at its own strength and at the derived verdict of the claim it comes from. Links without a strength count as INTERMEDIATE. Claims without links keep the annotator's verdict.  

| Statement | Role | Modality | Authors say | Verdict | Derived | Rationale |
|---|---|---|---|---|---|---|
| **CLAIM1** Pettifor embeddings systematically outperform other commonly used elemental embeddings in compositional machine learning models. | main conclusion | comparative | demonstrated | ◐ PARTIAL | **? INCONCLUSIVE** | Pettifor has the best mean rank (1.96) and the most wins (12/27) in Table 2, but loses to one-hot in 8 and to CGCNN in 9 tasks, wins none of the five smallest datasets, and no run-to-run spread is reported; 'systematically' is not supported. |
| **CLAIM2** Two-dimensional maps built from Pettifor embeddings and UMAP succeed in physically separating material classes according to basic physical properties. | main conclusion | generalization | demonstrated | ◐ PARTIAL | same | Metal/non-metal and partial crystal-system separation are reported (judged from captions and text of Figs. 4-5; figures not available), but the magnetic map in the same figure fails, and no metric or baseline map is given. |
| **HYP1** A non-orthogonal compositional space in which the angle between element axes encodes ICSD substitution similarity, combined with a structural fingerprint, gives a material representation that is both humanly interpretable and a more powerful machine-learning input than commonly used elemental embeddings. | main conclusion | comparative | demonstrated | ◐ PARTIAL | same | Interpretability holds by construction and the elemental similarities look chemically sensible; the ML advantage is best on average in Table 2 but not systematic, has no error bars, and fails for small datasets; map interpretability rests on visual inspection only. |
| **CLAIM3** The two-dimensional map of Pettifor element embeddings clusters chemically similar elements together, and the clustering emerges solely from substitution patterns in crystal structures. | intermediate | descriptive | demonstrated | ◐ PARTIAL | **◔ WEAK** | Lanthanide/actinide and transition-metal grouping is described (judged from text and caption; figure unavailable), but alkalis share a region with non-metals and no quantitative clustering measure is given. |
| **CLAIM4** Other common elemental embeddings (Magpie, Mat2Vec, Jarvis, CGCNN) give element maps of intermediate quality between the Pettifor and one-hot embeddings, with Magpie second best. | intermediate | comparative | demonstrated | ◔ WEAK | same | Rests on visual comparison of maps in the ESI (not available here) without any criterion for map quality. |
| **CLAIM5** Pettifor element distances generally agree with ElMD and differ significantly from property-based (Magpie) and text-mined (Mat2Vec) embeddings, which give chemically unexpected neighbours such as Ga for S. | intermediate | comparative | demonstrated | ◐ PARTIAL | **◔ WEAK** | Table 1 shows the agreement and the odd Magpie/Mat2Vec neighbours for S, Si and Ag, but three elements do not establish general agreement and ElMD shares the same source data. |
| **CLAIM6** Unlike ElMD, the Pettifor embedding distinguishes neighbours of the same order by their absolute distance, reflecting the higher replaceability of S by Se than by O in real compounds. | methodological | comparative | demonstrated | ✓ YES | same | Follows by construction from S and is illustrated by S-Se 0.77 vs S-O 1.26 against equal ElMD ranks. |
| **CLAIM7** The Pettifor embedding is unsupervised and independent of any target property, so its geometry can be interpreted and validated against chemical knowledge. | methodological | conceptual | demonstrated | ✓ YES | same | The construction in the Methods uses only substitution counts, so target-independence holds by construction. |
| **CLAIM8** The Pettifor composition map of ABC3 perovskites is divided into clusters by C element whose arrangement follows the similarity of the C atoms, with fine structure reflecting A and B similarity, and shows stability trends within and across perovskite subfamilies. | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | The split by C is expected by construction (C = 3/5 of the composition) and is described in text and caption (figure unavailable); the claimed ordering by similarity and the added value for reading stability trends are not quantified or compared with another embedding. |
| **CLAIM9** CrabNet with the Pettifor embedding gives on average the best results of the five embeddings while retaining simplicity and interpretability. | quantitative support | comparative | demonstrated | ◐ PARTIAL | same | By the annotator's count of Table 2 Pettifor has the best mean rank (1.96 vs 2.30) and most wins (12/27), but margins are often about 1 % and no spread over the 8 runs is given, so 'best' is not shown to exceed training noise. |
| **CLAIM10** The Pettifor embedding performs particularly well for small and medium-sized datasets, making it especially valuable where extensive training data are not available. | intermediate | comparative | demonstrated | ✗ NO | same | The paper's own Table 2 contradicts the small-data part: Pettifor loses all five smallest datasets (up to 19 % higher MAE than CGCNN on phonons); only the medium-size part (8 of 12 wins) holds. |
| **CLAIM11** The improved ML performance suggests that the Pettifor representation captures the essential chemical relationships relevant to materials properties. | mechanistic interpretation | causal | proposed | ◔ WEAK | same | Inferred from modest, noise-unqualified MAE gains; no ablation links the gain to the encoded similarity. |
| **CLAIM12** Despite the large diversity of the Alexandria hull, the Pettifor + STR map provides a reasonable structural separation of compounds and groups similar structural motifs. | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | The modest wording ('reasonable', 'some continents') matches a visual result described from Fig. 4 (caption and text only), partly expected because the structure fingerprint is an input, but nothing is quantified and the map depends on UMAP parameters. |
| **CLAIM13** Small islands in the Alexandria map can be interpreted as structurally and compositionally exotic compounds with few related materials on the convex hull. | mechanistic interpretation | descriptive | proposed | ? INCONCLUSIVE | **◔ WEAK** | Offered as a reasonable interpretation; the paper never checks, e.g. with its own uniqueness measure U, whether island members have larger nearest-neighbour distances. |
| **CLAIM14** UMAP combined with the Pettifor + STR fingerprint provides an excellent separation between metals and non-metals. | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | A separation is reported from Fig. 5 top (judged from caption and text; figure unavailable), but 'excellent' is unquantified and there is no baseline map. |
| **CLAIM15** Because magnetic and non-magnetic compounds are not separated in the map, the magnetic distinction will be much more difficult to predict with machine learning than the previous properties. | mechanistic interpretation | generalization | proposed | ? INCONCLUSIVE | same | No ML model for the magnetic label is trained; the inference from a 2D projection to ML difficulty is untested. |
| **CLAIM16** The information in the Pettifor + STR embedding may be compressed into a much smaller feature vector more suitable for efficient machine learning. | intermediate | descriptive | speculative | ◐ PARTIAL | same | PCA shows 95 % of variance in about 40 of more than 300 dimensions; that the compressed vectors keep ML accuracy is not tested. |
| **CLAIM17** The Pettifor + STR embedding captures both chemical and electronic similarities between materials and can accelerate the discovery of functional analogues of known materials. | intermediate | generalization | demonstrated | ◔ WEAK | same | One example judged visually from Fig. 6 (caption only) plus ESI band structures; no quantitative link between embedding distance and electronic similarity. |
| **CLAIM18** The embeddings can uncover promising candidates with a desired functionality without performing any calculation, because proximity in the representation space correlates with comparable physical properties. | intermediate | correlational | demonstrated | ◔ WEAK | same | One case (MgB2 neighbours, one computed Tc) with no measure of how often near neighbours share the property. |
| **CLAIM19** A high uniqueness U reveals truly distinctive compounds that merit special attention and offers valuable insight for theoretical and experimental materials design. | intermediate | generalization | demonstrated | ? INCONCLUSIVE | same | U is defined and two extremes are named, but no data show that high U predicts distinctive properties. |
| **CLAIM20** The proposed fingerprint is a simple and interpretable representation of a compound, built so that chemically similar compounds lie closer to each other than unrelated materials. | main conclusion | conceptual | demonstrated | ✓ YES | **◐ PARTIAL** | Holds by construction of S and f = c x S, and Table 1 illustrates that close elements are chemically similar; interpretability is a design property, not tested with users. |
| **CLAIM21** The fingerprint can create structure or property maps spanning entire families of materials or the whole material space, which can be used to visualize and interpret how material properties change across chemical space. | intermediate | generalization | demonstrated | ◐ PARTIAL | same | Maps of one family (perovskites) and of the Alexandria hull are produced; interpretation of property changes is qualitative, UMAP-dependent, and fails for magnetism. |
| **CLAIM22** The human-generated Pettifor fingerprint can compete with machine-learned opaque representations when used as an input feature to machine learning models. | intermediate | comparative | demonstrated | ✓ YES | **◐ PARTIAL** | Table 2 shows Pettifor competitive with or better than Mat2Vec (better in 20 of 27 tasks), the only machine-learned embedding tested; 'compete' is weaker than the abstract's 'systematically outperform'. |

**Support links tested on the five criteria** (directness, sufficiency, controls, alternatives, scope match; ✓ met, ◐ partly, ✗ not met, – not applicable):

| Link | Criteria | Strength | Note |
|---|---|---|---|
| OBS1 → CLAIM3 (essential) | ◐◐◐◐✓ | weak | 2D UMAP view as proxy for full-space similarity; judged by eye; one-hot as only in-text baseline; UMAP artefacts not excluded. |
| OBS2 → CLAIM4 (essential) | ◐✗◐–✓ | weak | Ranking of maps without a quality criterion; ESI figures only. |
| OBS3 → CLAIM5 (essential) | ✓◐◐–◐ | weak | Three query elements; ElMD shares the same source matrix, so agreement is not independent; 'general' exceeds three cases. |
| OBS4 → CLAIM6 (essential) | ✓✓✓–✓ | strong | Property of the construction; one example suffices to illustrate it. |
| METH2 → CLAIM6 | ✓✓––✓ | strong | Continuous distances follow from the definition of S. |
| METH1 → CLAIM7 (essential) | ✓✓––✓ | strong | S uses only substitution counts. |
| OBS5 → CLAIM8 (essential) | ✓◐◐–✓ | intermediate | Clustering by C by construction; similarity ordering and stability reading not quantified, no baseline map. |
| DATA2 → CLAIM8 | ✓◐––◐ | intermediate | One dataset of one structure type. |
| OBS6 → CLAIM9 (essential) | ✓◐◐–✓ | intermediate | 27 datasets but no run-to-run spread; hyperparameters per embedding not reported. |
| METH6 → CLAIM9 | ✓◐◐–✓ | intermediate | Same architecture for all embeddings, 8 runs, but no spread reported. |
| OBS6 → CLAIM10 (essential) | ✓◐◐–✗ | unsupported | Wins lie in medium datasets; for small datasets the same table shows the opposite. |
| CLAIM9 → CLAIM11 (essential) | ◐◐✗◐◐ | weak | No ablation separates the similarity information from other effects; gains small. |
| OBS6 → CLAIM1 (essential) | ✓◐◐–✗ | unsupported (annotator: weak) | Best on average, but beaten in 8-9 of 27 tasks by single baselines; 'systematically' exceeds the data; stronger learned baselines absent. |
| CLAIM9 → CLAIM1 | ✓◐◐–◐ | weak (annotator: intermediate) | Average superiority does not imply systematic superiority. |
| OBS6 → CLAIM22 (essential) | ✓◐✓–◐ | intermediate | 'Compete' is modest and matches Table 2; only one learned embedding (Mat2Vec) tested, CGCNN features are untrained. |
| OBS9 → CLAIM12 (essential) | ✓◐◐–✓ | intermediate | Large dataset, visual reading only; no baseline map. |
| DATA3 → CLAIM12 | ✓✓◐–◐ | intermediate | Over 115k hull compounds; only hull compounds. |
| OBS9 → CLAIM13 | ✗✗✗✗◐ | unsupported | Islands are observed; their exoticness is not measured (U for island members not computed). |
| OBS10 → CLAIM14 (essential) | ✓◐◐–✓ | intermediate | Visual; no score, no baseline map. |
| OBS11 → CLAIM15 (essential) | ✗✗✗✗◐ | unsupported | 2D separability is not ML predictability; no model trained. |
| CLAIM14 → CLAIM2 (essential) | ✓◐◐–✓ | intermediate | Supports separation for one property. |
| CLAIM12 → CLAIM2 | ✓◐◐–✓ | intermediate | Crystal system, visually. |
| OBS12 → CLAIM16 (essential) | ◐✓––◐ | intermediate | Variance retained is a proxy for information useful to ML; ML with compressed vectors not tested. |
| OBS13 → CLAIM17 (essential) | ◐✗◐◐◐ | weak | One query and one band structure compared by eye. |
| OBS14 → CLAIM18 (essential) | ◐✗◐◐◐ | weak | One query (MgB2), one computed Tc; correlation of distance and property never computed. |
| CLAIM17 → CLAIM18 | ◐✗◐◐◐ | weak | Second anecdotal case. |
| OBS15 → CLAIM19 (essential) | ✗✗✗✗◐ | unsupported | Two named extremes; no property analysis of high-U compounds. |
| DEF1 → CLAIM19 | ◐✗–◐◐ | weak | Definition only. |
| CLAIM7 → CLAIM20 (essential) | ✓✓––✓ | strong | By construction. |
| CLAIM6 → CLAIM20 | ✓✓––✓ | strong | Distances follow substitution similarity. |
| CLAIM8 → CLAIM21 | ✓◐◐–✓ | intermediate | One family map. |
| CLAIM12 → CLAIM21 (essential) | ✓◐◐–✓ | intermediate | Whole-hull map, visual. |
| CLAIM9 → HYP1 (essential) | ✓◐◐–✓ | intermediate | ML advantage on average, no error bars. |
| CLAIM20 → HYP1 (essential) | ✓✓––✓ | strong | Interpretability by construction. |
| CLAIM5 → HYP1 | ✓◐◐–◐ | weak | Three elements. |
| CLAIM12 → HYP1 | ✓◐◐–✓ | intermediate | Visual map evidence. |
| CLAIM14 → HYP1 | ✓◐◐–✓ | intermediate | Visual map evidence. |

**Golden thread** (each aim from the introduction to the end of the paper):

| Aim | Gap | Method | Result | Claim (verdict) | Outcome |
|---|---|---|---|---|---|
| **AIM1** The paper constructs a non-orthogonal compositional space from the ICSD similarity measure and represents compositions in it (Pettifor embeddings). | - | METH2, METH3 | - | - | METHOD ONLY |
| **AIM2** The paper combines the compositional representation with the pymatgen structural fingerprint to represent compounds with arbitrary composition and structure. | GAP1 | METH4 | - | CLAIM12 (◐) | DELIVERED |
| **AIM3** The paper shows that the non-orthogonal representation captures meaningful chemical relationships between elements. | - | - | - | CLAIM3 (◐), CLAIM5 (◐), CLAIM6 (✓) | NOT RESTATED |
| **AIM4** The paper generates interpretable two-dimensional visualizations of material space from the representation. | GAP1 | - | - | CLAIM8 (◐), CLAIM12 (◐), CLAIM14 (◐) | DELIVERED |
| **AIM5** The paper shows that the representation provides powerful embeddings for machine learning while keeping human-understandable connections to chemistry. | GAP2 | - | - | CLAIM9 (◐) | DELIVERED |

Outcomes: DELIVERED, NOT RESTATED (delivered but absent from the conclusion and abstract), METHOD ONLY (carried out but no result shown), DROPPED (nothing delivers it).

**Presented as demonstrated, but the verdict is weak, inconclusive or no:** CLAIM4 (WEAK), CLAIM10 (NO), CLAIM17 (WEAK), CLAIM18 (WEAK), CLAIM19 (INCONCLUSIVE).

**Recomputed checks:**

- **METH4** 61 x 4 = 244 = 244 (recomputed)
- **OBS3** distance between non-negative unit vectors <= sqrt(2) ✓ satisfied (recomputed)
- **OBS3** cosine similarity S-Se = 1 - d^2/2 = 0.7 (recomputed)
- **OBS3** cosine similarity S-O = 1 - d^2/2 = 0.21 (recomputed)
- **OBS5** fraction of composition from C = 3/5 = 0.6 (recomputed)
- **OBS6** Pettifor win share = 0.44 (recomputed)
- **OBS6** Pettifor has the best mean rank ✓ satisfied (recomputed)
- **OBS6** share of tasks in which plain one-hot beats Pettifor = 0.3 (recomputed)
- **OBS7** Pettifor worse than the best embedding on all five smallest datasets ✓ satisfied (recomputed)
- **OBS7** excess error on phonons vs CGCNN, % = 19.2 % (recomputed)
- **OBS7** excess error on steels_yield vs one-hot, % = 7.9 % (recomputed)
- **OBS8** relative difference OQMD formation enthalpy, % = 1.2 % (recomputed)
- **OBS8** relative Pettifor advantage MP shear modulus, % = 1.6 % (recomputed)
- **OBS12** compression ratio at 95 % = 0.14 (recomputed)
- **OBS13** isostructural Si and Ge: combined distance equals element distance (structure part contributes zero) ✓ satisfied (recomputed)
- **OBS13** SiC composition distance = 0.5 |S_C - S_Si| <= 0.5 sqrt(2) ✓ satisfied (recomputed)
- **OBS14** composition part of the distance <= (1/15) sqrt(2) = 0.094 (recomputed)
- **OBS14** reported distance explainable by composition alone ✗ not satisfied (recomputed)

**Statements per paper part:**

| Part | Statements |
|---|---|
| abstract | CLAIM1, CLAIM2 |
| introduction | BG1, BG2, GAP1, BG3, GAP2, BG4, BG5, HYP1, AIM1, AIM2, AIM3, AIM4, AIM5, ASM1, LIM1 |
| methods | METH1, METH2, METH3 |
| results | METH4, METH5, METH6, DATA1, DATA2, DATA3, ASM2, OBS1, OBS2, LIM2, CLAIM3, CLAIM4, OBS3, CLAIM5, OBS4, CLAIM6, CLAIM7, OBS5, CLAIM8, OBS6, OBS7, OBS8, CLAIM9, CLAIM10, CLAIM11, OBS9, CLAIM12, CLAIM13, OBS10, OBS11, CLAIM14, CLAIM15 |
| discussion | METH7, OBS12, CLAIM16, OBS13, CLAIM17, OBS14, CLAIM18, DEF1, OBS15, CLAIM19, ASM3 |
| conclusion | CLAIM20, CLAIM21, CLAIM22, LIM3, OUT1 |

Causal claims (check against correlational evidence): CLAIM11.

## 2. Limitations

- No uncertainty over the 8 CrabNet runs; many Table 2 margins are about 1 %, so 'best' and 'systematically outperform' are not shown beyond noise (CLAIM1, CLAIM9, OBS8).
- Small-dataset advantage contradicted by Table 2: Pettifor never best on the five smallest datasets (CLAIM10, OBS7).
- All map-based claims are judged by eye with no separation metric or baseline map, and the magnetic map fails (CLAIM2, CLAIM12, CLAIM14, OBS11).
- Discovery applications rest on single examples; the distance-property correlation is asserted, never computed, and the MgB2-Mg4AlB10 distance (0.16) exceeds the compositional bound of 0.094 without explanation (CLAIM17, CLAIM18, CLAIM19, OBS14).
- Ad hoc choices (alpha = 1/2, equal composition/structure weights, UMAP parameters) are not tested for sensitivity, and abstract and Methods disagree on whether compositions lie on the unit sphere (METH2, METH3, METH4).

**Stated by the authors:**

- **LIM1** (data): Spurious correlations may arise from bias and incompleteness of the ICSD, and the statistics and embeddings should be updated as new experimental data appear.
- **LIM2** (method): Reduction to two dimensions may distort distances, and the shape of the UMAP maps depends on the UMAP parameters, although the authors state that the relative distribution of elements is robust (ESI).
- **LIM3** (data): The representation lacks information for rare gases and some actinides.

**Assumptions the argument rests on:**

- **ASM1** (community accepted): Co-occurrence of two elements on the same site of the same crystal structure in the ICSD measures their chemical similarity. *Open question:* How much of the measured similarity reflects ICSD bias and incompleteness (sparsely studied elements such as Po or actinides) rather than chemistry?
- **ASM2** (author choice): Proximity and clusters in a two-dimensional UMAP projection reflect similarity in the full embedding space. *Open question:* How much of the clustering in Figs. 2-5 is an artefact of UMAP, which is known to form clusters and to distort global distances?
- **ASM3** (author choice): The minimal distance to other hull compounds measures chemical and structural distinctiveness rather than how densely a chemical region has been sampled in the database. *Open question:* Does U mainly reflect database coverage (few computed neighbours) rather than intrinsic distinctiveness?

**Inference rules that are empirical, unstated, argued only by the authors, or weak:**

- **CLAIM9→CLAIM11**: Better downstream accuracy implies that the input encodes the relevant chemistry. (unstated)

**Flagged by the annotator:**

- **CLAIM1** overclaim (high): Table 2 shows Pettifor best in 12 of 27 tasks and beaten by plain one-hot encoding in 8 of 27 and by CGCNN initial features in 9 of 27; this is not systematic outperformance.
- **CLAIM1** missing quantification (high): MAEs are averages of 8 runs but no standard deviation is given, so most margins (often 1-2 %) cannot be distinguished from training noise.
- **CLAIM1** confounded comparison (medium): Only one learned embedding (Mat2Vec) is compared; the stronger learned or data-mined embeddings named in the introduction (refs. 28-30) are not benchmarked, although the introduction says they consistently perform better.
- **CLAIM2** overgeneralization (high): The paper's own Fig. 5 (bottom) shows no good separation of magnetic and non-magnetic compounds; separation is shown for metal/non-metal and roughly for crystal system only.
- **CLAIM2** missing quantification (high): Separation is judged by eye; no cluster-purity, silhouette or nearest-neighbour classification score and no comparison map from another embedding is given for Figs. 4-5.
- **METH2** ad hoc parameter (medium): alpha = 1/2 is chosen to rebalance diagonal and off-diagonal terms, but no sensitivity of Table 1 or Table 2 to alpha is shown.
- **METH2** reproducibility (low): The norm used in the row-wise renormalization is not stated; the square root of an L1-normalized row already has unit L2 norm, so an L2 renormalization would be redundant and an L1 one would not give unit vectors.
- **METH3** internal inconsistency (medium): The abstract and introduction say the chemical composition is defined by a point on the unit sphere of the non-orthogonal space; the Methods state the composition vectors are in general not on the unit sphere.
- **METH4** ad hoc parameter (medium): Equal weights are chosen 'for simplicity'; the effect of the weight on maps, PCA and neighbour searches is not shown.
- **METH4** reproducibility (medium): What 'equal weights' means for blocks of 244 and about 90 dimensions with different norms (scaling, normalization of the STR block) is not stated.
- **METH5** reproducibility (low): The UMAP parameters (number of neighbours, minimum distance, metric) used for Figs. 2-5 are not given in the main text.
- **METH6** reproducibility (medium): Train/test splits, hyperparameters and whether hyperparameters were re-tuned per embedding are not reported.
- **METH6** missing quantification (high): No spread over the 8 runs is reported.
- **CLAIM3** missing quantification (medium): Clustering is judged by eye; no measure such as nearest-neighbour agreement with periodic-table group is given.
- **CLAIM3** unaddressed counterevidence (low): The text itself places alkali metals in the same region as non-metals (halogens, H, O), which are chemically dissimilar; this is not discussed.
- **CLAIM4** missing quantification (medium): 'Performance' of a map is not defined; the ranking is a visual judgement on ESI figures.
- **CLAIM4** confounded comparison (low): The one-hot reference is equidistant by construction, so its unstructured map is a trivial baseline.
- **OBS3** unaddressed counterevidence (low): Po is the second most similar element to S, ahead of Te and far ahead of O; Po chemistry is sparsely represented in the ICSD, which may reflect the data bias the authors acknowledge (LIM1) rather than chemical similarity; not discussed.
- **OBS3** internal inconsistency (low): Table 1 caption lists CGCNN while the text describing Table 1 omits it.
- **CLAIM5** overgeneralization (medium): 'General agreement' is read from three query elements.
- **CLAIM5** unfalsifiable validation (low): Agreement with ElMD is not independent validation: both derive from the same ICSD similarity matrix, as the authors note.
- **CLAIM8** untested assertion (low): Clustering by C follows from C being 60 % of the composition; that cluster positions and fine structure follow element similarity is stated, not measured.
- **CLAIM8** confounded comparison (low): The stability facts (inverted perovskites most stable) belong to the dataset of ref. 42; no baseline map shows what the Pettifor embedding adds.
- **CLAIM9** missing quantification (high): 'On average' is not defined (MAEs have different units, so presumably rank or wins), and without run-to-run spread the ~1 % margins may be noise.
- **CLAIM10** internal inconsistency (high): Table 2 shows Pettifor is never best on the five smallest datasets (312-3422 entries), ranking 4th of 5 on the smallest; its wins lie at medium sizes.
- **CLAIM11** causal overreach (medium): Small average gains over one-hot in a flexible attention model do not show which relationships are captured; no ablation (e.g. alpha = 0 or shuffled S) isolates the similarity information.
- **CLAIM12** missing quantification (medium): No measure of how pure the crystal-system regions are.
- **CLAIM14** overclaim (medium): 'Excellent' is not backed by any classification score or misclassification count.
- **CLAIM14** confounded comparison (medium): No map from a baseline embedding and no split into composition and structure parts shows how much the Pettifor part contributes.
- **CLAIM15** causal overreach (medium): Separability in a 2D UMAP projection does not measure learnability in the full feature space; no classifier is trained on the magnetic label.
- **OBS12** missing quantification (low): Adding 244 structural dimensions lowers the components needed for 60 % (7 to 6); this depends on the unstated relative scaling of the two blocks and is not discussed.
- **CLAIM17** overgeneralization (high): Electronic similarity is shown by one band structure (NiSi3P4) for one query (Si); no band-structure similarity measure and no correlation over many pairs.
- **OBS14** arithmetic (medium): MgB2 to Mg4AlB10 differs by 1/15 Mg replaced by Al, so the composition distance is at most 0.094; the reported 0.16 needs a structural contribution of at least 0.13 for a compound described as an MgB2 supercell, which is not explained.
- **OBS14** reproducibility (medium): How the 20.8 K Tc of LiMgB4 was calculated is not described, and the neighbour search includes an off-hull compound although the maps and U use hull compounds only; the search set is not specified.
- **CLAIM18** untested assertion (high): The correlation between proximity and physical properties is asserted but never computed.
- **CLAIM18** overclaim (medium): The example candidate's promise rests on a Tc calculation, so it was not identified 'without performing any calculation'.
- **CLAIM19** untested assertion (medium): No analysis shows that high-U compounds have unusual properties; one anecdote (h-BN) is given.

**Local checks per part** (issues found; failed derived checks count as arithmetic):

| Part | Completeness | Arithmetic | Consistency | Argument | High or critical |
|---|---|---|---|---|---|
| abstract | 2 | 0 | 0 | 3 | 4 |
| methods | 1 | 0 | 1 | 1 | 0 |
| results | 8 | 0 | 4 | 10 | 3 |
| discussion | 2 | 1 | 0 | 4 | 2 |

## 3. Missing evidence

- MAE standard deviations over the 8 runs and a paired test across the 27 datasets
- Learning curves of MAE vs training-set size for each embedding
- Benchmark against the learned embeddings of refs. 28-30
- Quantitative separation scores (kNN accuracy, silhouette) for maps from Pettifor and baseline embeddings
- Correlation of embedding distance with property differences (band gap, Tc) over many compound pairs
- Sensitivity of Tables 1-2 to alpha and to the composition/structure weighting

**Open proof obligations:**

- **CLAIM1** (open, critical): Show that Pettifor beats each baseline by more than run-to-run noise on most datasets. (partly: OBS7) Needs: MAE standard deviation over 8 runs per embedding and dataset [dataset units] via CrabNet retraining with fixed splits.
- **CLAIM1** (partially discharged, high): Show that Pettifor wins against the strongest baselines, not only on average rank. (partly: OBS7)
- **CLAIM2** (open, critical): Quantify separation of each property class in the map and compare with baseline embeddings. Needs: kNN classification accuracy of metal/non-metal and magnetic labels [%] via in 2D UMAP and in full Pettifor + STR space, vs one-hot baseline.
- **CLAIM2** (partially discharged, medium): Show the separation is robust to UMAP parameters. (partly: LIM2)
- **HYP1** (partially discharged, high): The similarity encoded in S reflects chemical similarity. (partly: CLAIM3, CLAIM5, CLAIM6)
- **HYP1** (partially discharged, critical): The embedding improves ML predictions over the baselines beyond training noise. (partly: CLAIM9) Needs: MAE mean and standard deviation over 8 runs [dataset units] via CrabNet on 27 benchmarks.
- **HYP1** (partially discharged, high): Maps from the embedding separate material classes in an interpretable way. (partly: CLAIM8, CLAIM12, CLAIM14)
- **HYP1** (open, medium): Results are robust to the ad hoc choices (alpha = 1/2, equal weights, UMAP parameters). Needs: Table 2 MAE and Table 1 neighbours for alpha in 0.25-1 [dataset units] via recomputed S.
- **CLAIM20** (partially discharged, medium): Chemically similar elements are near each other in practice. (partly: OBS3, CLAIM3)

**Per statement:**

- **CLAIM1**: Standard deviation of the MAE over the 8 CrabNet runs for every embedding and dataset
- **CLAIM1**: Paired significance test (e.g. Wilcoxon over datasets) of Pettifor vs one-hot and vs CGCNN
- **CLAIM1**: Benchmark against the learned embeddings of refs. 28-30
- **CLAIM2**: Quantitative separation score (kNN accuracy or silhouette in the 2D map and in the full space) for each property
- **CLAIM2**: Same maps from one-hot, Magpie and Mat2Vec embeddings as baselines
- **HYP1**: Run-to-run spread and significance of the Table 2 differences
- **HYP1**: Quantitative measure of map quality against baseline embeddings
- **HYP1**: Sensitivity of results to the exponent alpha and the composition/structure weighting
- **CLAIM3**: Fraction of elements whose nearest neighbour in the full embedding is in the same periodic-table group, vs one-hot and Magpie
- **CLAIM4**: A numeric map-quality score per embedding (e.g. group-label kNN accuracy or trustworthiness)
- **CLAIM5**: Overlap of nearest-neighbour lists with ElMD and with chemical group for all elements
- **CLAIM9**: Standard deviation over the 8 runs and a paired test across datasets
- **CLAIM10**: Learning curves (MAE vs training-set size) for each embedding on the same task
- **CLAIM11**: Ablation with a randomly permuted similarity matrix S of the same sparsity
- **CLAIM13**: Distribution of uniqueness U for island vs continent compounds
- **CLAIM14**: kNN metal/non-metal classification accuracy in the map and in the full space vs one-hot
- **CLAIM15**: Classification ROC AUC for magnetic vs non-magnetic and for metal vs non-metal with the same model and embedding
- **CLAIM16**: CrabNet or other model accuracy with PCA-compressed embeddings
- **CLAIM17**: Correlation of embedding distance with band-gap difference or band-structure distance over many compound pairs
- **CLAIM18**: Hit rate of nearest neighbours sharing superconductivity (or another target property) vs random compounds
- **CLAIM19**: Property statistics (e.g. band gap outliers) of high-U vs low-U hull compounds
