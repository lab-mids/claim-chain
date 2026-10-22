# Argument chain: A non-orthogonal representation for materials based on chemical similarity

Tiago F. T. Cerqueira, Haichen Wang, Silvana Botti, Miguel A. L. Marques (2026), doi:10.1038/s41524-025-01916-8. Generated from the claim-chain YAML (schema 0.6.0); do not edit by hand.

**Logic score: 0.51** (4 YES, 11 PARTIAL, 4 WEAK, 3 INCONCLUSIVE, 1 NO), weighted by claim role: 0.54. Method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting).

## Motivation

**BG1** `BACKGROUND`  Introduction, para. 1  
High-throughput density functional theory and machine learning have produced materials databases that catalogue most known compounds and millions of hypothetical phases together with their properties.  
Evidence: citation [1, 2, 3, 4, 5, 6, 7]  
→ motivates **GAP1**  

**BG2** `BACKGROUND`  Introduction, para. 2-3  
Structure maps correlate the structure type of a compound with its constituents, and for binary compounds two-dimensional maps along an element ordering such as the Pettifor scale are easy to make.  
Evidence: citation [8, 9, 10, 11, 12, 13, 14, 15, 16]  
→ motivates **GAP1**  

**GAP1** `GAP`  Introduction, para. 2-4  
For ternary or multinary compounds and for datasets with several crystal structures there is no representation of a compound that is both humanly interpretable and suitable for materials informatics.  
Evidence: none given  
→ motivates **HYP1**  
→ motivates **AIM2**  
→ motivates **AIM4**  

**BG3** `BACKGROUND`  Introduction, para. 4  
Embeddings from trained neural networks such as crystal graph networks, combined with dimension reduction, are used to map properties over materials space.  
Evidence: citation [17, 18, 19, 20, 21]  
→ motivates **GAP2**  

**GAP2** `GAP`  Introduction, para. 4 and 6  
Trained embeddings contain information about the target property and learned or text-mined elemental embeddings act as black boxes, so they hamper interpretation of structure-property relationships even though they perform better in predictive tasks.  
Evidence: citation [34]  
→ motivates **HYP1**  
→ motivates **AIM5**  
→ qualifies **CLAIM1**  

**BG4** `BACKGROUND`  Introduction, para. 7  
A chemical similarity scale between elements was previously built from substitution statistics of experimentally known compounds in the ICSD.  
Evidence: citation [35, 36]  
→ motivates **AIM1**  

**BG5** `BACKGROUND`  Introduction, para. 8  
Earth Mover's Distance approaches such as ElMD compare compositions using data-mined chemical similarity encoded in a one-dimensional element ordering.  
Evidence: citation [15, 37, 38, 39]  
→ motivates **AIM3**  

**HYP1** `HYPOTHESIS` `main conclusion` `demonstrated` Introduction, para. 6-9  
A non-orthogonal compositional space in which the angle between element axes encodes ICSD substitution similarity, combined with a structural fingerprint, gives a material representation that is both humanly interpretable and a more powerful machine-learning input than commonly used elemental embeddings.  
Modality: comparative  
**Verdict: ◐ PARTIAL**. Interpretability holds by construction and the elemental similarities look chemically sensible; the ML advantage is best on average in Table 2 but not systematic, has no error bars, and fails for small datasets; map interpretability rests on visual inspection only.  
Missing: Run-to-run spread and significance of the Table 2 differences  
Missing: Quantitative measure of map quality against baseline embeddings  
Missing: Sensitivity of results to the exponent alpha and the composition/structure weighting  
Obligation (partially discharged, high): The similarity encoded in S reflects chemical similarity. ← CLAIM3, CLAIM5, CLAIM6  
Obligation (partially discharged, critical): The embedding improves ML predictions over the baselines beyond training noise. ← CLAIM9  
&nbsp;&nbsp;&nbsp;needs: MAE mean and standard deviation over 8 runs [dataset units] via CrabNet on 27 benchmarks  
Obligation (partially discharged, high): Maps from the embedding separate material classes in an interpretable way. ← CLAIM8, CLAIM12, CLAIM14  
Obligation (open, medium): Results are robust to the ad hoc choices (alpha = 1/2, equal weights, UMAP parameters).  
&nbsp;&nbsp;&nbsp;needs: Table 2 MAE and Table 1 neighbours for alpha in 0.25-1 [dataset units] via recomputed S  

**AIM1** `AIM` `demonstrated` Introduction, para. 7  
The paper constructs a non-orthogonal compositional space from the ICSD similarity measure and represents compositions in it (Pettifor embeddings).  
Evidence: none given  

**AIM2** `AIM` `demonstrated` Introduction, para. 5  
The paper combines the compositional representation with the pymatgen structural fingerprint to represent compounds with arbitrary composition and structure.  
Evidence: none given  

**AIM3** `AIM` `demonstrated` Introduction, final para.  
The paper shows that the non-orthogonal representation captures meaningful chemical relationships between elements.  
Evidence: none given  

**AIM4** `AIM` `demonstrated` Introduction, final para.  
The paper generates interpretable two-dimensional visualizations of material space from the representation.  
Evidence: none given  

**AIM5** `AIM` `demonstrated` Introduction, final para.  
The paper shows that the representation provides powerful embeddings for machine learning while keeping human-understandable connections to chemistry.  
Evidence: none given  

## Concept

**DEF1** `DEFINITION`  Discussion, para. 5  
The uniqueness U of a compound on the convex hull is its minimal Euclidean distance to any other material in the Pettifor + STR embedding space.  
→ depends on **METH4**  
→ supports **CLAIM19** [logical, weak]  

## Methods and data

**ASM1** `ASSUMPTION`  Introduction, para. 8  
Co-occurrence of two elements on the same site of the same crystal structure in the ICSD measures their chemical similarity.  
Evidence: citation [15, 35]  
Basis: community accepted. Open question: How much of the measured similarity reflects ICSD bias and incompleteness (sparsely studied elements such as Po or actinides) rather than chemistry?  

**METH1** `METHOD`  Methods, Pettifor embeddings, para. 1  
The raw symmetric matrix M from ref. 35 counts, for each element pair, the ICSD compounds that share a crystal structure with one element substituted by the other, with the number of compounds containing the element on the diagonal; each row is normalized to unity to give substitution probabilities.  
Evidence: citation [35]  
→ depends on **ASM1** *(annotator)*  
→ supports **CLAIM7** [logical, strong]  

**METH2** `METHOD`  Methods, Pettifor embeddings, para. 2  
To counter the ICSD bias toward diagonal terms, the substitution probabilities are raised to the power alpha = 1/2 and renormalized row-wise; the rows of the resulting matrix S are unit vectors whose dot products give element similarities.  
Evidence: citation [15]  
→ depends on **METH1**  
→ delivers **AIM1**  
→ supports **CLAIM6** [logical, strong] *(annotator)*  
⚠ ad hoc parameter (medium): alpha = 1/2 is chosen to rebalance diagonal and off-diagonal terms, but no sensitivity of Table 1 or Table 2 to alpha is shown.  
⚠ reproducibility (low): The norm used in the row-wise renormalization is not stated; the square root of an L1-normalized row already has unit L2 norm, so an L2 renormalization would be redundant and an L1 one would not give unit vectors.  

**METH3** `METHOD`  Methods, Pettifor embeddings, para. 3-4, Figs. 7-8  
The fingerprint of a composition is f = c x S, with c the vector of stoichiometric fractions; because c is L1-normalized, compositions lie on an (N-1)-dimensional simplex and only elementary substances lie on the unit sphere.  
Evidence: none given  
→ depends on **METH2**  
→ delivers **AIM1**  
⚠ internal inconsistency (medium): The abstract and introduction say the chemical composition is defined by a point on the unit sphere of the non-orthogonal space; the Methods state the composition vectors are in general not on the unit sphere.  

**METH4** `METHOD`  Results, Embeddings with structural information; Discussion para. 1  
Composition and structure are combined by concatenating the Pettifor embedding with the pymatgen local-coordination fingerprint (61 order parameters x 4 statistics = 244 dimensions) with equal weights, giving the Pettifor + STR embedding.  
Evidence: data_quantitative (Discussion, para. 1)  
Check: 61 x 4 = 244 = 244 (recomputed)  
→ depends on **METH3**  
→ delivers **AIM2**  
⚠ ad hoc parameter (medium): Equal weights are chosen 'for simplicity'; the effect of the weight on maps, PCA and neighbour searches is not shown.  
⚠ reproducibility (medium): What 'equal weights' means for blocks of 244 and about 90 dimensions with different norms (scaling, normalization of the STR block) is not stated.  

**METH5** `METHOD`  Results, Similarity of chemical elements  
Embeddings are reduced to two dimensions with UMAP; the effect of UMAP parameters is shown only in the ESI.  
Evidence: none given  
⚠ reproducibility (low): The UMAP parameters (number of neighbours, minimum distance, metric) used for Figs. 2-5 are not given in the main text.  

**METH6** `METHOD`  Results, Fingerprint for chemical composition, Table 2  
CrabNet is trained with Mat2Vec, Magpie, CGCNN initial atomic features, one-hot and Pettifor embeddings on 27 benchmark datasets of ref. 34, and the errors are averaged over 8 runs.  
Evidence: none given  
→ depends on **DATA1**  
→ supports **CLAIM9** [logical, intermediate]  
⚠ reproducibility (medium): Train/test splits, hyperparameters and whether hyperparameters were re-tuned per embedding are not reported.  
⚠ missing quantification (high): No spread over the 8 runs is reported.  

**DATA1** `DATA`  Table 2  
The ML benchmark comprises 27 datasets from 312 (steel yield strength) to 239190 entries (OQMD), 25 regression tasks scored by MAE and 2 classification tasks scored by ROC AUC.  
Evidence: none given  
Scope: n = 27; 27 datasets, 312-239190 entries each  

**DATA2** `DATA`  Results, Fingerprint for chemical composition, Fig. 3  
The perovskite dataset of ref. 42 contains cubic Pm-3m ABC3 compounds with 5-atom cells, of which the lower-energy member of each ABC3/BAC3 pair is plotted.  
Evidence: citation [42]  
→ supports **CLAIM8** [logical, intermediate]  

**DATA3** `DATA`  Results, Embeddings with structural information  
The structure maps use all compounds on the convex hull of the Alexandria database, over 115 thousand compounds.  
Evidence: citation [3]  
Scope: n = 115000; over 115 thousand hull compounds; exact number not given  
→ supports **CLAIM12** [logical, intermediate]  

**ASM2** `ASSUMPTION`  Results, Figs. 2-5  
Proximity and clusters in a two-dimensional UMAP projection reflect similarity in the full embedding space.  
Evidence: none given  
Basis: author choice. Open question: How much of the clustering in Figs. 2-5 is an artefact of UMAP, which is known to form clusters and to distort global distances?  
→ conditionally supports **CLAIM3** *(annotator)*  
→ conditionally supports **CLAIM13** *(annotator)*  
→ alternative explanation for **CLAIM15** *(annotator, background knowledge)*  

**METH7** `METHOD`  Discussion, para. 1  
A principal component analysis of the Pettifor and Pettifor + STR embeddings of the hull compounds estimates how many dimensions are needed to represent them.  
Evidence: none given  
→ depends on **METH4**  

**ASM3** `ASSUMPTION`  Discussion, para. 5 (annotator)  
The minimal distance to other hull compounds measures chemical and structural distinctiveness rather than how densely a chemical region has been sampled in the database.  
Evidence: none given  
Basis: author choice. Open question: Does U mainly reflect database coverage (few computed neighbours) rather than intrinsic distinctiveness?  
→ alternative explanation for **CLAIM19** *(annotator, background knowledge)*  

## Observations

**OBS1** `OBSERVATION`  Results, Similarity of chemical elements, Fig. 2 (top)  
In the UMAP map of the Pettifor element embeddings, lanthanides and actinides lie in the top left, transition metals in the middle, and non-metals together with the alkali elements in the bottom right.  
Evidence: data_qualitative (Fig. 2 top): Figure not available; judged from caption, text and extracted labels. The extracted label positions place alkalis (Li, Na, K, Rb, Cs, Fr) next to halogens, H and O.  
Scope: n = 1; one map of about 90 elements, noble gases removed  
→ supports **CLAIM3** [qualitative, weak, medium uncertainty]  

**OBS2** `OBSERVATION`  Results, Similarity of chemical elements, Fig. 2 (bottom), ESI Fig. S1  
The one-hot embedding gives an unstructured element map because all elements are equidistant, and Magpie, Mat2Vec, Jarvis and CGCNN maps are shown only in the ESI.  
Evidence: data_qualitative (Fig. 2 bottom, ESI Fig. S1)  
→ supports **CLAIM4** [qualitative, weak, high uncertainty]  

**OBS3** `OBSERVATION`  Results, Table 1  
In Table 1 the three Pettifor nearest neighbours are Se (0.77), Po (0.88), Te (0.94) for S; Ge (0.64), Sn (0.96), Ga (1.04) for Si; Au (0.74), Cu (0.85), Pd (0.90) for Ag; ElMD gives Se, O, Te; Ge, B, Sn; Cu, Au, Pd; Magpie gives Ga, P, I for S and Mat2Vec gives N, O, C for S.  
Evidence: data_quantitative (Table 1)  
Check: distance between non-negative unit vectors <= sqrt(2) ✓ satisfied (recomputed)  
Check: cosine similarity S-Se = 1 - d^2/2 = 0.7 (recomputed)  
Check: cosine similarity S-O = 1 - d^2/2 = 0.21 (recomputed)  
Scope: n = 3; three query elements (S, Si, Ag)  
→ supports **CLAIM5** [quantitative, weak, medium uncertainty]  
⚠ unaddressed counterevidence (low): Po is the second most similar element to S, ahead of Te and far ahead of O; Po chemistry is sparsely represented in the ICSD, which may reflect the data bias the authors acknowledge (LIM1) rather than chemical similarity; not discussed.  
⚠ internal inconsistency (low): Table 1 caption lists CGCNN while the text describing Table 1 omits it.  

**OBS4** `OBSERVATION`  Results, Similarity of chemical elements  
The Pettifor distance of S to Se (0.77) is much smaller than that of S to O (1.26), whereas both Se and O are first neighbours of S on the one-dimensional modified Pettifor scale used by ElMD.  
Evidence: none given  
→ supports **CLAIM6** [quantitative, strong, low uncertainty]  

**OBS5** `OBSERVATION`  Results, Fingerprint for chemical composition, Fig. 3  
The UMAP map of cubic ABC3 perovskites splits into one cluster per C element with fine structure from A and B; most compounds are far above the hull, oxide perovskites centre near (15.3, 2.5), and the most stable are inverted perovskites ABCa3 near (3.8, 18.8), ABSr3 near (5.2, 15.9) and ABSc3 near (3.2, 8.8).  
Evidence: data_qualitative (Fig. 3): Figure not available; judged from caption and text. C occupies 3 of 5 sites, so C dominates the composition vector.  
Check: fraction of composition from C = 3/5 = 0.6 (recomputed)  
→ supports **CLAIM8** [qualitative, intermediate, medium uncertainty]  

**OBS6** `OBSERVATION`  Table 2 (annotator count)  
Across the 27 benchmarks of Table 2 the Pettifor embedding has the best score in 12 (one tied with CGCNN), CGCNN in 9, one-hot in 6, Mat2Vec in 3 and Magpie in 1; the mean rank is 1.96 for Pettifor, 2.30 for CGCNN, 2.74 for one-hot, 2.93 for Mat2Vec and 4.70 for Magpie; Pettifor beats one-hot in 19, CGCNN in 17, Mat2Vec in 20 and Magpie in 25 of 27 tasks.  
Evidence: data_quantitative (Table 2)  
Check: Pettifor win share = 0.44 (recomputed)  
Check: Pettifor has the best mean rank ✓ satisfied (recomputed)  
Check: share of tasks in which plain one-hot beats Pettifor = 0.3 (recomputed)  
Scope: n = 27  
→ supports **CLAIM9** [quantitative, intermediate, medium uncertainty]  
→ supports **CLAIM10** [quantitative, unsupported, medium uncertainty]  
→ supports **CLAIM1** [quantitative, weak, medium uncertainty]  
→ supports **CLAIM22** [quantitative, intermediate, medium uncertainty]  

**OBS7** `OBSERVATION`  Table 2 (annotator count)  
In the five smallest datasets (312-3422 entries) the Pettifor embedding is never best and ranks 4, 3, 2, 2, 2; CGCNN is best in four and one-hot in steel yield strength (126 vs 136 MPa); Pettifor wins 8 of the 12 medium datasets (3428-10987 entries) and 4 of the 10 largest.  
Evidence: data_quantitative (Table 2)  
Check: Pettifor worse than the best embedding on all five smallest datasets ✓ satisfied (recomputed)  
Check: excess error on phonons vs CGCNN, % = 19.2 % (recomputed)  
Check: excess error on steels_yield vs one-hot, % = 7.9 % (recomputed)  
Scope: n = 5; steels_yield, jdft2d, phonons, Aflow thermal expansion, Aflow thermal conductivity  
→ contradicts **CLAIM10** *(annotator)*  
→ undercuts **CLAIM1** *(annotator)*  
→ undercuts **HYP1** *(annotator)*  

**OBS8** `OBSERVATION`  Table 2  
Many differences between the Pettifor embedding and the best alternative are about 1 % (e.g. OQMD formation enthalpy 0.0426 vs 0.0421 for one-hot, Aflow thermal conductivity 2.31 vs 2.29 for CGCNN), and no run-to-run spread is given for the 8-run averages.  
Evidence: data_quantitative (Table 2)  
Check: relative difference OQMD formation enthalpy, % = 1.2 % (recomputed)  
Check: relative Pettifor advantage MP shear modulus, % = 1.6 % (recomputed)  
→ undercuts **CLAIM9** *(annotator)*  
→ undercuts **CLAIM1** *(annotator)*  

**OBS9** `OBSERVATION`  Results, Embeddings with structural information, Fig. 4  
In the UMAP map of the Alexandria hull compounds with Pettifor + STR embeddings most compounds form large continents with a few small islands; some continents are dominated by one crystal system, and islands group hexagonal and trigonal layered materials or the cubic-tetragonal-orthorhombic sequence.  
Evidence: data_qualitative (Fig. 4): Figure not available; judged from caption and text.  
Scope: n = 115000  
→ supports **CLAIM12** [qualitative, intermediate, medium uncertainty]  
→ supports **CLAIM13** [qualitative, unsupported, high uncertainty]  

**OBS10** `OBSERVATION`  Results, Embeddings with structural information, Fig. 5 (top)  
In the Alexandria map coloured by band gap, metals and non-metals occupy clearly separated regions.  
Evidence: data_qualitative (Fig. 5 top): Figure not available; judged from caption and text.  
→ supports **CLAIM14** [qualitative, intermediate, medium uncertainty]  

**OBS11** `OBSERVATION`  Results, Embeddings with structural information, Fig. 5 (bottom)  
In the Alexandria map coloured by magnetic moment, magnetic and non-magnetic compounds are not well separated.  
Evidence: data_qualitative (Fig. 5 bottom): Figure not available; judged from caption and text.  
→ supports **CLAIM15** [qualitative, unsupported, high uncertainty]  
→ undercuts **CLAIM2** *(annotator)*  
→ qualifies **CLAIM21** *(annotator)*  

**OBS12** `OBSERVATION`  Discussion, para. 1  
Seven principal components capture 60 % of the compositional variance and six capture 60 % of the composition plus structure variance; 95 % needs 39 and 42 components, against more than 300 original dimensions.  
Evidence: data_quantitative (Discussion, para. 1)  
Check: compression ratio at 95 % = 0.14 (recomputed)  
→ supports **CLAIM16** [quantitative, intermediate, low uncertainty]  
⚠ missing quantification (low): Adding 244 structural dimensions lowers the components needed for 60 % (7 to 6); this depends on the unstated relative scaling of the two blocks and is not discussed.  

**OBS13** `OBSERVATION`  Discussion, para. 3, Fig. 6, ESI Fig. S5  
The nearest compounds to diamond Si in Pettifor + STR space are Ge (0.64), SiC (0.70) and NiSi3P4 (0.71), and the band structure of NiSi3P4 is shown against the upfolded Si bands.  
Evidence: data_quantitative (Discussion para. 3; Table 1; Fig. 6)  
Check: isostructural Si and Ge: combined distance equals element distance (structure part contributes zero) ✓ satisfied (recomputed)  
Check: SiC composition distance = 0.5 |S_C - S_Si| <= 0.5 sqrt(2) ✓ satisfied (recomputed)  
Scope: n = 1; one query compound; one band structure in the main text  
→ supports **CLAIM17** [qualitative, weak, high uncertainty]  

**OBS14** `OBSERVATION`  Discussion, para. 4  
The compounds closest to MgB2 include Mg4AlB10 (distance 0.16), described as a five-layer MgB2 supercell with one Mg layer replaced by Al, and LiMgB4 (0.123 eV/atom above the hull) with a calculated superconducting Tc of about 20.8 K.  
Evidence: data_quantitative (Discussion, para. 4)  
Check: composition part of the distance <= (1/15) sqrt(2) = 0.094 (recomputed)  
Check: reported distance explainable by composition alone ✗ not satisfied (recomputed)  
Scope: n = 1  
→ supports **CLAIM18** [qualitative, weak, high uncertainty]  
⚠ arithmetic (medium): MgB2 to Mg4AlB10 differs by 1/15 Mg replaced by Al, so the composition distance is at most 0.094; the reported 0.16 needs a structural contribution of at least 0.13 for a compound described as an MgB2 supercell, which is not explained.  
⚠ reproducibility (medium): How the 20.8 K Tc of LiMgB4 was calculated is not described, and the neighbour search includes an off-hull compound although the maps and U use hull compounds only; the search set is not specified.  

**OBS15** `OBSERVATION`  Discussion, para. 5  
As is the most unique elementary substance on the hull (distance 1.06 to P) and hexagonal BN the most unique binary compound (distance 1.17 to graphite), although BN and graphite are isovalent and isostructural yet electronically very different.  
Evidence: none given  
→ supports **CLAIM19** [qualitative, unsupported, high uncertainty]  

## Claims

**CLAIM1** `CLAIM` `main conclusion` `demonstrated` Abstract  
Pettifor embeddings systematically outperform other commonly used elemental embeddings in compositional machine learning models.  
Evidence: none given  
Modality: comparative  
→ restates **CLAIM9** *(annotator)*  
⚠ overclaim (high): Table 2 shows Pettifor best in 12 of 27 tasks and beaten by plain one-hot encoding in 8 of 27 and by CGCNN initial features in 9 of 27; this is not systematic outperformance.  
⚠ missing quantification (high): MAEs are averages of 8 runs but no standard deviation is given, so most margins (often 1-2 %) cannot be distinguished from training noise.  
⚠ confounded comparison (medium): Only one learned embedding (Mat2Vec) is compared; the stronger learned or data-mined embeddings named in the introduction (refs. 28-30) are not benchmarked, although the introduction says they consistently perform better.  
**Verdict: ◐ PARTIAL**. Pettifor has the best mean rank (1.96) and the most wins (12/27) in Table 2, but loses to one-hot in 8 and to CGCNN in 9 tasks, wins none of the five smallest datasets, and no run-to-run spread is reported; 'systematically' is not supported.  
Missing: Standard deviation of the MAE over the 8 CrabNet runs for every embedding and dataset  
Missing: Paired significance test (e.g. Wilcoxon over datasets) of Pettifor vs one-hot and vs CGCNN  
Missing: Benchmark against the learned embeddings of refs. 28-30  
Obligation (open, critical): Show that Pettifor beats each baseline by more than run-to-run noise on most datasets. ← OBS7  
&nbsp;&nbsp;&nbsp;needs: MAE standard deviation over 8 runs per embedding and dataset [dataset units] via CrabNet retraining with fixed splits  
Obligation (partially discharged, high): Show that Pettifor wins against the strongest baselines, not only on average rank. ← OBS7  

**CLAIM2** `CLAIM` `main conclusion` `demonstrated` Abstract  
Two-dimensional maps built from Pettifor embeddings and UMAP succeed in physically separating material classes according to basic physical properties.  
Evidence: none given  
Modality: generalization  
→ restates **CLAIM14** *(annotator)*  
⚠ overgeneralization (high): The paper's own Fig. 5 (bottom) shows no good separation of magnetic and non-magnetic compounds; separation is shown for metal/non-metal and roughly for crystal system only.  
⚠ missing quantification (high): Separation is judged by eye; no cluster-purity, silhouette or nearest-neighbour classification score and no comparison map from another embedding is given for Figs. 4-5.  
**Verdict: ◐ PARTIAL**. Metal/non-metal and partial crystal-system separation are reported (judged from captions and text of Figs. 4-5; figures not available), but the magnetic map in the same figure fails, and no metric or baseline map is given.  
Missing: Quantitative separation score (kNN accuracy or silhouette in the 2D map and in the full space) for each property  
Missing: Same maps from one-hot, Magpie and Mat2Vec embeddings as baselines  
Obligation (open, critical): Quantify separation of each property class in the map and compare with baseline embeddings.  
&nbsp;&nbsp;&nbsp;needs: kNN classification accuracy of metal/non-metal and magnetic labels [%] via in 2D UMAP and in full Pettifor + STR space, vs one-hot baseline  
Obligation (partially discharged, medium): Show the separation is robust to UMAP parameters. ← LIM2  

**CLAIM3** `CLAIM` `intermediate` `demonstrated` Results, Similarity of chemical elements  
The two-dimensional map of Pettifor element embeddings clusters chemically similar elements together, and the clustering emerges solely from substitution patterns in crystal structures.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM3**  
⚠ missing quantification (medium): Clustering is judged by eye; no measure such as nearest-neighbour agreement with periodic-table group is given.  
⚠ unaddressed counterevidence (low): The text itself places alkali metals in the same region as non-metals (halogens, H, O), which are chemically dissimilar; this is not discussed.  
**Verdict: ◐ PARTIAL**. Lanthanide/actinide and transition-metal grouping is described (judged from text and caption; figure unavailable), but alkalis share a region with non-metals and no quantitative clustering measure is given.  
Missing: Fraction of elements whose nearest neighbour in the full embedding is in the same periodic-table group, vs one-hot and Magpie  

**CLAIM4** `CLAIM` `intermediate` `demonstrated` Results, Similarity of chemical elements  
Other common elemental embeddings (Magpie, Mat2Vec, Jarvis, CGCNN) give element maps of intermediate quality between the Pettifor and one-hot embeddings, with Magpie second best.  
Evidence: none given  
Modality: comparative  
⚠ missing quantification (medium): 'Performance' of a map is not defined; the ranking is a visual judgement on ESI figures.  
⚠ confounded comparison (low): The one-hot reference is equidistant by construction, so its unstructured map is a trivial baseline.  
**Verdict: ◔ WEAK**. Rests on visual comparison of maps in the ESI (not available here) without any criterion for map quality.  
Missing: A numeric map-quality score per embedding (e.g. group-label kNN accuracy or trustworthiness)  

**CLAIM5** `CLAIM` `intermediate` `demonstrated` Results, Similarity of chemical elements  
Pettifor element distances generally agree with ElMD and differ significantly from property-based (Magpie) and text-mined (Mat2Vec) embeddings, which give chemically unexpected neighbours such as Ga for S.  
Evidence: none given  
Modality: comparative  
→ delivers **AIM3**  
→ supports **HYP1** [quantitative, weak]  
⚠ overgeneralization (medium): 'General agreement' is read from three query elements.  
⚠ unfalsifiable validation (low): Agreement with ElMD is not independent validation: both derive from the same ICSD similarity matrix, as the authors note.  
**Verdict: ◐ PARTIAL**. Table 1 shows the agreement and the odd Magpie/Mat2Vec neighbours for S, Si and Ag, but three elements do not establish general agreement and ElMD shares the same source data.  
Missing: Overlap of nearest-neighbour lists with ElMD and with chemical group for all elements  

**CLAIM6** `CLAIM` `methodological` `demonstrated` Results, Similarity of chemical elements; Introduction para. 8  
Unlike ElMD, the Pettifor embedding distinguishes neighbours of the same order by their absolute distance, reflecting the higher replaceability of S by Se than by O in real compounds.  
Evidence: none given  
Warrant: Distances are built from substitution counts, so a pair that substitutes more often has a smaller distance; a 1D ordering can only give integer rank differences. (definition)  
Modality: comparative  
→ delivers **AIM3**  
→ supports **CLAIM20** [logical, strong]  
**Verdict: ✓ YES**. Follows by construction from S and is illustrated by S-Se 0.77 vs S-O 1.26 against equal ElMD ranks.  

**CLAIM7** `CLAIM` `methodological` `demonstrated` Results, Similarity of chemical elements; Introduction para. 8  
The Pettifor embedding is unsupervised and independent of any target property, so its geometry can be interpreted and validated against chemical knowledge.  
Evidence: none given  
Warrant: S is computed from ICSD substitution counts only, without any property labels. (definition)  
Modality: conceptual  
→ supports **CLAIM20** [logical, strong]  
**Verdict: ✓ YES**. The construction in the Methods uses only substitution counts, so target-independence holds by construction.  

**CLAIM8** `CLAIM` `intermediate` `demonstrated` Results, Fingerprint for chemical composition  
The Pettifor composition map of ABC3 perovskites is divided into clusters by C element whose arrangement follows the similarity of the C atoms, with fine structure reflecting A and B similarity, and shows stability trends within and across perovskite subfamilies.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM4**  
→ supports **CLAIM21** [qualitative, intermediate]  
⚠ untested assertion (low): Clustering by C follows from C being 60 % of the composition; that cluster positions and fine structure follow element similarity is stated, not measured.  
⚠ confounded comparison (low): The stability facts (inverted perovskites most stable) belong to the dataset of ref. 42; no baseline map shows what the Pettifor embedding adds.  
**Verdict: ◐ PARTIAL**. The split by C is expected by construction (C = 3/5 of the composition) and is described in text and caption (figure unavailable); the claimed ordering by similarity and the added value for reading stability trends are not quantified or compared with another embedding.  

**CLAIM9** `CLAIM` `quantitative support` `demonstrated` Results, Fingerprint for chemical composition, Table 2  
CrabNet with the Pettifor embedding gives on average the best results of the five embeddings while retaining simplicity and interpretability.  
Evidence: none given  
Modality: comparative  
→ delivers **AIM5**  
→ supports **CLAIM11** [logical, weak, high uncertainty]  
&nbsp;&nbsp;&nbsp;warrant: Better downstream accuracy implies that the input encodes the relevant chemistry. (unstated)  
→ supports **CLAIM1** [logical, intermediate]  
→ supports **HYP1** [quantitative, intermediate]  
⚠ missing quantification (high): 'On average' is not defined (MAEs have different units, so presumably rank or wins), and without run-to-run spread the ~1 % margins may be noise.  
**Verdict: ◐ PARTIAL**. By the annotator's count of Table 2 Pettifor has the best mean rank (1.96 vs 2.30) and most wins (12/27), but margins are often about 1 % and no spread over the 8 runs is given, so 'best' is not shown to exceed training noise.  
Missing: Standard deviation over the 8 runs and a paired test across datasets  

**CLAIM10** `CLAIM` `intermediate` `demonstrated` Results, Fingerprint for chemical composition  
The Pettifor embedding performs particularly well for small and medium-sized datasets, making it especially valuable where extensive training data are not available.  
Evidence: none given  
Modality: comparative  
⚠ internal inconsistency (high): Table 2 shows Pettifor is never best on the five smallest datasets (312-3422 entries), ranking 4th of 5 on the smallest; its wins lie at medium sizes.  
**Verdict: ✗ NO**. The paper's own Table 2 contradicts the small-data part: Pettifor loses all five smallest datasets (up to 19 % higher MAE than CGCNN on phonons); only the medium-size part (8 of 12 wins) holds.  
Missing: Learning curves (MAE vs training-set size) for each embedding on the same task  

**CLAIM11** `CLAIM` `mechanistic interpretation` `proposed` Results, Fingerprint for chemical composition *(hedged)*  
The improved ML performance suggests that the Pettifor representation captures the essential chemical relationships relevant to materials properties.  
Evidence: none given  
Modality: causal  
⚠ causal overreach (medium): Small average gains over one-hot in a flexible attention model do not show which relationships are captured; no ablation (e.g. alpha = 0 or shuffled S) isolates the similarity information.  
**Verdict: ◔ WEAK**. Inferred from modest, noise-unqualified MAE gains; no ablation links the gain to the encoded similarity.  
Missing: Ablation with a randomly permuted similarity matrix S of the same sparsity  

**CLAIM12** `CLAIM` `intermediate` `demonstrated` Results, Embeddings with structural information  
Despite the large diversity of the Alexandria hull, the Pettifor + STR map provides a reasonable structural separation of compounds and groups similar structural motifs.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM2**  
→ delivers **AIM4**  
→ supports **CLAIM2** [qualitative, intermediate]  
→ supports **CLAIM21** [qualitative, intermediate]  
→ supports **HYP1** [qualitative, intermediate]  
⚠ missing quantification (medium): No measure of how pure the crystal-system regions are.  
**Verdict: ◐ PARTIAL**. The modest wording ('reasonable', 'some continents') matches a visual result described from Fig. 4 (caption and text only), partly expected because the structure fingerprint is an input, but nothing is quantified and the map depends on UMAP parameters.  

**CLAIM13** `CLAIM` `mechanistic interpretation` `proposed` Results, Embeddings with structural information *(hedged)*  
Small islands in the Alexandria map can be interpreted as structurally and compositionally exotic compounds with few related materials on the convex hull.  
Evidence: none given  
Modality: descriptive  
**Verdict: ? INCONCLUSIVE**. Offered as a reasonable interpretation; the paper never checks, e.g. with its own uniqueness measure U, whether island members have larger nearest-neighbour distances.  
Missing: Distribution of uniqueness U for island vs continent compounds  

**CLAIM14** `CLAIM` `intermediate` `demonstrated` Results, Embeddings with structural information  
UMAP combined with the Pettifor + STR fingerprint provides an excellent separation between metals and non-metals.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM4**  
→ supports **CLAIM2** [qualitative, intermediate]  
→ supports **HYP1** [qualitative, intermediate]  
⚠ overclaim (medium): 'Excellent' is not backed by any classification score or misclassification count.  
⚠ confounded comparison (medium): No map from a baseline embedding and no split into composition and structure parts shows how much the Pettifor part contributes.  
**Verdict: ◐ PARTIAL**. A separation is reported from Fig. 5 top (judged from caption and text; figure unavailable), but 'excellent' is unquantified and there is no baseline map.  
Missing: kNN metal/non-metal classification accuracy in the map and in the full space vs one-hot  

**CLAIM15** `CLAIM` `mechanistic interpretation` `proposed` Results, Embeddings with structural information  
Because magnetic and non-magnetic compounds are not separated in the map, the magnetic distinction will be much more difficult to predict with machine learning than the previous properties.  
Evidence: none given  
Modality: generalization  
⚠ causal overreach (medium): Separability in a 2D UMAP projection does not measure learnability in the full feature space; no classifier is trained on the magnetic label.  
**Verdict: ? INCONCLUSIVE**. No ML model for the magnetic label is trained; the inference from a 2D projection to ML difficulty is untested.  
Missing: Classification ROC AUC for magnetic vs non-magnetic and for metal vs non-metal with the same model and embedding  

**CLAIM16** `CLAIM` `intermediate` `speculative` Discussion, para. 1 *(hedged)*  
The information in the Pettifor + STR embedding may be compressed into a much smaller feature vector more suitable for efficient machine learning.  
Evidence: none given  
Modality: descriptive  
**Verdict: ◐ PARTIAL**. PCA shows 95 % of variance in about 40 of more than 300 dimensions; that the compressed vectors keep ML accuracy is not tested.  
Missing: CrabNet or other model accuracy with PCA-compressed embeddings  

**CLAIM17** `CLAIM` `intermediate` `demonstrated` Discussion, para. 3  
The Pettifor + STR embedding captures both chemical and electronic similarities between materials and can accelerate the discovery of functional analogues of known materials.  
Evidence: none given  
Modality: generalization  
→ supports **CLAIM18** [logical, weak]  
⚠ overgeneralization (high): Electronic similarity is shown by one band structure (NiSi3P4) for one query (Si); no band-structure similarity measure and no correlation over many pairs.  
**Verdict: ◔ WEAK**. One example judged visually from Fig. 6 (caption only) plus ESI band structures; no quantitative link between embedding distance and electronic similarity.  
Missing: Correlation of embedding distance with band-gap difference or band-structure distance over many compound pairs  

**CLAIM18** `CLAIM` `intermediate` `demonstrated` Discussion, para. 4  
The embeddings can uncover promising candidates with a desired functionality without performing any calculation, because proximity in the representation space correlates with comparable physical properties.  
Evidence: none given  
Modality: correlational  
⚠ untested assertion (high): The correlation between proximity and physical properties is asserted but never computed.  
⚠ overclaim (medium): The example candidate's promise rests on a Tc calculation, so it was not identified 'without performing any calculation'.  
**Verdict: ◔ WEAK**. One case (MgB2 neighbours, one computed Tc) with no measure of how often near neighbours share the property.  
Missing: Hit rate of nearest neighbours sharing superconductivity (or another target property) vs random compounds  

**CLAIM19** `CLAIM` `intermediate` `demonstrated` Discussion, para. 5  
A high uniqueness U reveals truly distinctive compounds that merit special attention and offers valuable insight for theoretical and experimental materials design.  
Evidence: none given  
Modality: generalization  
⚠ untested assertion (medium): No analysis shows that high-U compounds have unusual properties; one anecdote (h-BN) is given.  
**Verdict: ? INCONCLUSIVE**. U is defined and two extremes are named, but no data show that high U predicts distinctive properties.  
Missing: Property statistics (e.g. band gap outliers) of high-U vs low-U hull compounds  

**CLAIM20** `CLAIM` `main conclusion` `demonstrated` Discussion, final para.  
The proposed fingerprint is a simple and interpretable representation of a compound, built so that chemically similar compounds lie closer to each other than unrelated materials.  
Evidence: none given  
Warrant: Distances derive from element dot products equal to substitution similarity, so similarity is directly readable from the geometry. (definition)  
Modality: conceptual  
→ restates **CLAIM7** *(annotator)*  
→ supports **HYP1** [logical, strong]  
**Verdict: ✓ YES**. Holds by construction of S and f = c x S, and Table 1 illustrates that close elements are chemically similar; interpretability is a design property, not tested with users.  
Obligation (discharged): Distances in the embedding follow element substitution similarity. ← METH2, METH3, CLAIM6  
Obligation (partially discharged, medium): Chemically similar elements are near each other in practice. ← OBS3, CLAIM3  

**CLAIM21** `CLAIM` `intermediate` `demonstrated` Discussion, final para.  
The fingerprint can create structure or property maps spanning entire families of materials or the whole material space, which can be used to visualize and interpret how material properties change across chemical space.  
Evidence: none given  
Modality: generalization  
→ restates **CLAIM12** *(annotator)*  
**Verdict: ◐ PARTIAL**. Maps of one family (perovskites) and of the Alexandria hull are produced; interpretation of property changes is qualitative, UMAP-dependent, and fails for magnetism.  

**CLAIM22** `CLAIM` `intermediate` `demonstrated` Discussion, final para.  
The human-generated Pettifor fingerprint can compete with machine-learned opaque representations when used as an input feature to machine learning models.  
Evidence: none given  
Modality: comparative  
→ restates **CLAIM9** *(annotator)*  
→ motivates **OUT1**  
**Verdict: ✓ YES**. Table 2 shows Pettifor competitive with or better than Mat2Vec (better in 20 of 27 tasks), the only machine-learned embedding tested; 'compete' is weaker than the abstract's 'systematically outperform'.  

## Limitations (stated by authors)

**LIM1** `LIMITATION`  Introduction, para. 8  
Spurious correlations may arise from bias and incompleteness of the ICSD, and the statistics and embeddings should be updated as new experimental data appear.  
Evidence: none given  
Kind: data  
→ qualifies **ASM1**  
→ undercuts **CLAIM5** *(annotator)*  

**LIM2** `LIMITATION`  Results, Similarity of chemical elements; Fingerprint for chemical composition  
Reduction to two dimensions may distort distances, and the shape of the UMAP maps depends on the UMAP parameters, although the authors state that the relative distribution of elements is robust (ESI).  
Evidence: none given  
Kind: method  
→ qualifies **CLAIM3**  
→ qualifies **CLAIM12**  

**LIM3** `LIMITATION`  Discussion, final para.  
The representation lacks information for rare gases and some actinides.  
Evidence: none given  
Kind: data  
→ qualifies **CLAIM20**  

## Outlook

**OUT1** `OUTLOOK`  Discussion, final para.; Results, Table 2 paragraph  
The representation may become an important tool for accurate machine prediction of properties and for human interpretation of high-throughput studies, and could serve as a node embedding in graph neural networks.  
Evidence: none given  
