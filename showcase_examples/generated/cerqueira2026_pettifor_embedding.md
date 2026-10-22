# Argument chain: A non-orthogonal representation for materials based on chemical similarity

Tiago F. T. Cerqueira, Haichen Wang, Silvana Botti, Miguel A. L. Marques (2026), doi:10.1038/s41524-025-01916-8. Generated from the claim-chain YAML (schema 0.6.0); do not edit by hand.

**Logic score: 0.57** (4 YES, 6 PARTIAL, 4 WEAK, 0 INCONCLUSIVE, 1 NO), weighted by claim role: 0.53. Method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting).

## Motivation

**BG1** `BACKGROUND`  Introduction, para. 1-3  
Large materials databases call for representations of compounds that are both machine-readable and humanly understandable; structure maps do this for binaries but not for multinary compounds or mixed crystal structures.  
Evidence: citation [1, 3-7, 8, 9, 10-13]  
→ motivates **GAP1**  
→ motivates **AIM3**  

**GAP1** `GAP`  Introduction, para. 4  
Embeddings taken from trained neural networks already contain information about the target property, which complicates the interpretation of structure-property relationships.  
Evidence: citation [17, 18, 19, 20, 21]  
→ motivates **AIM1**  

**GAP2** `GAP`  Introduction, para. 6  
Learned or database-derived elemental embeddings predict well but act as black boxes, while one-hot encoding is transparent but treats all elements as equally dissimilar.  
Evidence: citation [24, 25-34]  
→ motivates **AIM2**  
→ motivates **AIM4**  

**AIM1** `AIM`  Introduction, para. 5-6  
The paper builds a fingerprint of a compound from its composition and crystal structure only, such that distances between fingerprints reflect the similarity of compounds.  
Evidence: none given  

**AIM2** `AIM`  Introduction, para. 6-7  
The paper introduces a composition embedding in a non-orthogonal space whose axis angles encode element similarity from ICSD substitution statistics, combining the efficiency of learned embeddings with transparency.  
Evidence: none given  

**AIM3** `AIM`  Introduction, final paragraph  
The paper shows that the representation gives interpretable maps of material space.  
Evidence: none given  

**AIM4** `AIM`  Introduction, final paragraph  
The paper shows that the representation provides powerful embeddings for machine learning.  
Evidence: none given  

## Methods and data

**ASM1** `ASSUMPTION`  Introduction, para. 8  
Element substitution counts in ICSD measure chemical similarity, although the database is biased and incomplete.  
Evidence: none given  

**METH1** `METHOD`  Methods, Pettifor embeddings  
The substitution-count matrix M from ICSD is row-normalised, raised element-wise to the power 1/2 to counter the diagonal bias and renormalised, giving unit row vectors S_A; a composition c (stoichiometric fractions) is embedded as f = c x S.  
Evidence: citation [15, 35, 36]  
→ depends on **ASM1** *(annotator)*  
→ delivers **AIM2**  
→ contradicts **ABS3** *(annotator)*  
⚠ ad hoc parameter (low): The exponent alpha = 1/2 is taken from an earlier procedure; its effect on the results is not shown.  

**METH2** `METHOD`  Results, Embeddings with structural information  
The structural part is the pymatgen local-coordination fingerprint (61 x 4 = 244 components), concatenated with equal weight to the composition part.  
Evidence: data_quantitative (Discussion, para. 1)  
Check: 61 x 4 = 244 ✓ satisfied (recomputed)  
→ delivers **AIM1**  
⚠ ad hoc parameter (low): Equal weights for composition and structure are chosen for simplicity; other weights are not tested.  

**METH3** `METHOD`  Results, Fingerprint for chemical composition, Table 2  
CrabNet is trained with five elemental embeddings on 27 benchmark datasets, averaging each result over 8 training runs.  
Evidence: none given  
⚠ missing quantification (medium): The spread over the 8 runs is not reported, so it is unclear which of the many small differences in Table 2 are significant.  

## Observations

**OBS1** `OBSERVATION`  Results, Similarity of chemical elements, Fig. 2  
The UMAP map of the element embeddings places lanthanides and actinides top left, transition metals in the middle and non-metals and alkali metals bottom right, while one-hot elements show no grouping.  
Evidence: none given  
→ supports **CLAIM1** [qualitative, strong]  

**OBS2** `OBSERVATION`  Results, Table 1  
The nearest elements in the Pettifor embedding are Se, Po, Te for S; Ge, Sn, Ga for Si; and Au, Cu, Pd for Ag, with S-Se at 0.77 and S-O at 1.26, while Magpie puts Ga closest to S.  
Evidence: data_quantitative (Table 1)  
→ supports **CLAIM1** [quantitative, intermediate]  
→ supports **CLAIM2** [quantitative, strong]  

**OBS3** `OBSERVATION`  Results, Fig. 3  
In the composition map of cubic ABC3 perovskites, compounds cluster by the C element, with fine structure from A and B; most cubic perovskites are unstable and the most stable ones are inverted perovskites such as ABCa3 and ABSr3.  
Evidence: none given  
→ supports **CLAIM6** [qualitative, intermediate]  

**OBS4** `OBSERVATION`  Results, Table 2  
Across 27 benchmarks the Pettifor embedding is best or tied best in 12, has the best mean rank (1.96, against 2.30 for CGCNN, 2.74 one-hot, 2.93 Mat2Vec, 4.70 Magpie), and is not best in any of the three smallest datasets (312, 636 and 1265 entries; ranks 4, 3 and 2).  
Evidence: data_quantitative (Table 2)  
Check: Pettifor has the best mean rank ✓ satisfied (recomputed)  
Check: Pettifor is best in most benchmarks ✗ not satisfied (recomputed)  
→ supports **CLAIM3** [quantitative, intermediate]  
→ supports **ABS1** [quantitative, intermediate]  
→ supports **CON2** [quantitative, strong]  
→ contradicts **CLAIM4** *(annotator)*  

**OBS5** `OBSERVATION`  Results, Figs. 4 and 5  
The UMAP map of over 115 000 Alexandria hull compounds forms large continents and small islands; regions are dominated by particular crystal systems, metals and non-metals separate well, and magnetic and non-magnetic compounds do not.  
Evidence: none given  
→ supports **CLAIM6** [qualitative, intermediate]  
→ supports **ABS2** [qualitative, intermediate]  
→ qualifies **ABS2**  
→ supports **CON1** [qualitative, intermediate]  
→ supports **CLAIM7** [qualitative, weak]  
⚠ missing quantification (low): Separation is judged by eye; no clustering or classification score is given.  

**OBS6** `OBSERVATION`  Discussion, para. 1  
A PCA needs 39 components for 95% of the variance in composition and 42 for composition plus structure, out of more than 300 dimensions.  
Evidence: none given  
→ supports **CLAIM8** [quantitative, strong]  

**OBS7** `OBSERVATION`  Discussion, para. 3-4, Fig. 6  
The nearest compounds to Si are Ge (0.64), SiC (0.70) and NiSi3P4 (0.71), whose band structure resembles that of Si; the nearest to MgB2 are Mg4AlB10 (0.16) and LiMgB4, with a calculated Tc of about 20.8 K.  
Evidence: none given  
Scope: n = 2; Two reference compounds (Si and MgB2) and their five nearest neighbours each  
→ supports **CLAIM9** [qualitative, weak]  

**OBS8** `OBSERVATION`  Discussion, para. 5  
Defining uniqueness as the distance to the nearest hull compound, As is the most unique element (1.06 to P) and hexagonal BN the most unique binary (1.17 to graphite), although hBN is an insulator and graphite a semimetal.  
Evidence: none given  
→ qualifies **CLAIM9** *(annotator)*  
→ supports **CLAIM10** [qualitative, intermediate]  

## Claims

**ABS1** `CLAIM` `main conclusion` `demonstrated` Abstract  
Pettifor embeddings systematically outperform other commonly used elemental embeddings in compositional machine learning models.  
Evidence: none given  
Modality: comparative  
→ restates **CLAIM3** *(annotator)*  
⚠ overclaim (medium): Table 2 shows the Pettifor embedding best (or tied) in 12 of 27 benchmarks, ahead of one-hot in 19 and of CGCNN in 17; the results section says 'on average the best', which the table supports, but not 'systematically'.  
**Verdict: ◐ PARTIAL**. Best mean rank across 27 benchmarks (1.96 against 2.30 for CGCNN), but it loses to at least one alternative in 15 of them and no run-to-run spread is given.  

**ABS2** `CLAIM` `main conclusion` `demonstrated` Abstract  
Two-dimensional maps of thermodynamically stable compounds built from the Pettifor embeddings separate material classes according to basic physical properties.  
Evidence: none given  
Modality: descriptive  
→ restates **CLAIM6** *(annotator)*  
**Verdict: ◐ PARTIAL**. Shown for crystal system and metal versus non-metal; the paper itself shows that magnetic and non-magnetic compounds are not separated.  

**ABS3** `CLAIM` `methodological` `demonstrated` Abstract  
In the non-orthogonal composition space, a chemical composition is defined by a point on the unit sphere.  
Evidence: none given  
Modality: conceptual  
⚠ internal inconsistency (low): Methods state that composition vectors are in general not on the unit sphere but on an (N-1)-dimensional simplex, because they are normalised with the L1 norm; only elementary substances lie on the unit sphere.  
**Verdict: ◔ WEAK**. Contradicted by the paper's own Methods for every compound except elementary substances; a wording slip, not a flaw of the method.  

**CLAIM1** `CLAIM` `intermediate` `demonstrated` Results, Similarity of chemical elements  
Chemically similar elements cluster in the embedding, purely from substitution patterns and without encoding the periodic table.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM2**  
**Verdict: ✓ YES**. Fig. 2 shows the grouping against a one-hot control; robustness to UMAP parameters is shown in the ESI.  

**CLAIM2** `CLAIM` `intermediate` `demonstrated` Results, Similarity of chemical elements  
The embedding separates degrees of similarity that a one-dimensional scale cannot, e.g. Se is much closer to S than O is, although both are nearest neighbours of S on the modified Pettifor scale.  
Evidence: none given  
Modality: comparative  
**Verdict: ✓ YES**. Follows from the construction and is shown by the Table 1 distances; illustrated for three elements only.  

**CLAIM3** `CLAIM` `main conclusion` `demonstrated` Results, after Table 2  
Used as input to CrabNet, the Pettifor embedding yields on average the best results of the five embeddings while remaining simple and interpretable.  
Evidence: none given  
Modality: comparative  
→ delivers **AIM4**  
→ supports **CLAIM5** [logical, intermediate]  
**Verdict: ◐ PARTIAL**. The mean rank is best, but margins are often a few percent and no spread over the 8 runs is given to show they are significant.  
Obligation (open, medium): Report the standard deviation over the 8 runs for each benchmark and embedding.  

**CLAIM4** `CLAIM` `intermediate` `demonstrated` Results, after Table 2  
The Pettifor embedding performs particularly well for small- and medium-sized datasets.  
Evidence: none given  
Modality: comparative  
→ supports **CLAIM5** [logical, weak]  
**Verdict: ✗ NO**. On the three smallest datasets it ranks 4th, 3rd and 2nd; its wins lie between about 3 400 and 60 000 entries.  

**CLAIM5** `CLAIM` `mechanistic interpretation` `proposed` Results, after Table 2  
The improved performance suggests that the representation captures the chemical relationships relevant to materials properties, which makes it valuable where training data are scarce.  
Evidence: none given  
Modality: causal  
**Verdict: ◔ WEAK**. The first half follows plausibly from the benchmark; the data-scarce half rests on CLAIM4, which the table does not support.  

**CLAIM6** `CLAIM` `main conclusion` `demonstrated` Results, Figs. 4 and 5  
Despite the diversity of the data set, the map gives a reasonable structural separation of compounds and an excellent separation of metals and non-metals.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM3**  
**Verdict: ◐ PARTIAL**. Visible in Figures 4 and 5, but judged by eye and dependent on UMAP parameters, as the authors note.  

**CLAIM7** `CLAIM` `intermediate` `proposed` Results, final paragraph  
The missing separation of magnetic compounds suggests that magnetism will be much harder to predict with machine learning than the other properties.  
Evidence: none given  
Modality: generalization  
**Verdict: ◔ WEAK**. A two-dimensional UMAP projection says little about what a model trained on the full embedding can learn; no model is trained on magnetism.  

**CLAIM8** `CLAIM` `intermediate` `demonstrated` Discussion, para. 1  
The information can probably be compressed into a much smaller feature vector.  
Evidence: none given  
Modality: descriptive  
**Verdict: ✓ YES**. Follows directly from the PCA counts.  

**CLAIM9** `CLAIM` `main conclusion` `demonstrated` Discussion, para. 3-4  
Proximity in the embedding space correlates with comparable physical properties, so the embedding can find functional analogues of known materials without any calculation.  
Evidence: none given  
Modality: generalization  
⚠ overgeneralization (medium): A general correlation is stated from two hand-picked cases; the paper's own hBN-graphite pair (close neighbours with very different electronic properties) is a counterexample that is not discussed as such.  
**Verdict: ◔ WEAK**. Two illustrative cases, no systematic test of how well distance predicts property similarity.  

**CLAIM10** `CLAIM` `intermediate` `proposed` Discussion, para. 5  
The uniqueness measure highlights compounds with few similar alternatives that may merit attention in experiments.  
Evidence: none given  
Modality: conceptual  
**Verdict: ◐ PARTIAL**. A definition with two examples; its usefulness for experiments is argued, not shown.  

**CON1** `CLAIM` `intermediate` `demonstrated` Discussion, final paragraph  
The fingerprint can be used to create structure or property maps that span families of materials or the entire material space.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM1**  
→ restates **CLAIM6** *(annotator)*  
**Verdict: ◐ PARTIAL**. Restates the map results, which hold for structure and metallicity but not for magnetism.  

**CON2** `CLAIM` `intermediate` `demonstrated` Discussion, final paragraph  
The human-generated fingerprint can compete with machine-learned opaque representations as input to machine learning models.  
Evidence: none given  
Modality: comparative  
→ restates **CLAIM3** *(annotator)*  
**Verdict: ✓ YES**. "Can compete" is exactly what Table 2 shows; more cautious than the abstract.  

## Limitations (stated by authors)

**LIM1** `LIMITATION`  Discussion, final paragraph; Introduction, para. 8  
The similarity data lack information for rare gases and some actinides, and ICSD bias may create spurious correlations.  
Evidence: none given  
Kind: data  
→ qualifies **CLAIM1**  

**LIM2** `LIMITATION`  Results, Similarity of chemical elements; Figs. 4-5 text  
The shape of the two-dimensional maps depends on the UMAP parameters, and two dimensions may distort distances.  
Evidence: none given  
Kind: method  
→ qualifies **CLAIM6**  
