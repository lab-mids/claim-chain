# Argument chain: Lattice genome: representation and analysis of heterogeneous crystalline microstructures

Jiayang Wang, Mathieu Calvat, J.C. Stinville, Marat I. Latypov (2026), arxiv:2606.09611v1. Generated from the claim-chain YAML (schema 0.3.0); do not edit by hand.

**Logic score: 0.46** (2 YES, 7 PARTIAL, 4 INCONCLUSIVE, 1 NO). Method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, INCONCLUSIVE=0.25, NO=0 (draft weighting).

## Motivation

**BG1** `BACKGROUND` Sec. 1  
The Materials Genome Initiative assumes materials have an underlying code dictating behaviour, but what a materials gene looks like in practice remains unclear.  
Evidence: citation [1, 2]  

**BG2** `BACKGROUND` Sec. 1  
A generalized materials gene should be a vector that is compact, unique, experimentally accessible, and has a distance metric reflecting structural similarity.  
Evidence: citation [3]  
→ motivates **GAP1**  

**BG3** `BACKGROUND` Sec. 1  
Atomic pair distribution functions meet the gene criteria for uniform materials but lack spatial information at the mesoscale.  
Evidence: citation [3]  
→ motivates **GAP1**  

**BG4** `BACKGROUND` Sec. 1  
In structural alloys, spatial heterogeneity of phases, orientations and defects governs macroscale properties.  
Evidence: citation [4, 5]  
→ motivates **GAP1**  

**GAP1** `GAP` Sec. 1  
No notion of materials genes exists for spatially heterogeneous materials at the mesoscale.  
Evidence: argument: No literature survey given.  
→ motivates **HYP1**  

**BG5** `BACKGROUND` Sec. 1  
EBSD maps Kikuchi patterns over large areas at the mesoscale with high automation and speed.  
Evidence: citation [6, 7]  
→ supports **HYP1**  

**BG6** `BACKGROUND` Sec. 1  
Conventional EBSD reduces Kikuchi patterns to individual lossy descriptors (phase, orientation, rotation, strain, dislocation densities); combining them does not recover all pattern information.  
Evidence: citation [8, 9, 10, 11, 12, 13, 14, 15]  
→ motivates **HYP1**  

**BG7** `BACKGROUND` Sec. 1  
Prior PCA, matrix-factorization and deep-learning approaches to Kikuchi patterns compress them or extract known features, but do not give a holistic compact encoding.  
Evidence: citation [16-25]  
→ motivates **HYP1**  

**BG8** `BACKGROUND` Sec. 1  
A VAE trained on Kikuchi patterns compresses each pattern into a latent vector from which the pattern can be reconstructed to a predefined accuracy.  
Evidence: citation [26, 27, 28, 15]  
→ supports **HYP1**  
→ supports **CLAIM1a** [logical, intermediate, medium uncertainty]  
→ supports **CLAIM1b** [logical, strong, low uncertainty]  
→ supports **CLAIM1c** [logical, weak, high uncertainty]  
→ supports **CLAIM1d** [logical, weak, high uncertainty]  

**BG9** `BACKGROUND` Sec. 1  
Spatial maps of VAE latent features of Kikuchi patterns reveal microstructural heterogeneities with sensitivity exceeding conventional EBSD analysis.  
Evidence: citation [15]  
Scope: IN718, Waspaloy; Same data source as this paper.  
→ supports **HYP1**  

**HYP1** `HYPOTHESIS` Sec. 1  
VAE latent representations of Kikuchi patterns satisfy the criteria for a generalized materials gene, which extends the materials genome to heterogeneous crystalline materials, and they support standard microstructure analysis.  
Modality: conceptual  
**Verdict: ◐ PARTIAL**. The tools work comparably to conventional EBSD on three maps, but the gene criteria are argued, not shown, and the distance criterion is contradicted by LIM2 and LIM3.  
Missing: Quantitative test of the gene criteria (see CLAIM1a-d)  
Missing: Independent ground truth for the finer features  
Obligation (partially discharged): Show that each of the four gene criteria holds with data ← CLAIM1a, CLAIM1b  
Obligation (partially discharged): Show that the lattice genome supports standard EBSD analyses ← CLAIM3, CLAIM4, CLAIM6, CLAIM7  

## Concept

**DEF1** `DEFINITION` Sec. 2  
A lattice gene is the latent encoding z_i in R^d of a single Kikuchi pattern.  
→ depends on **HYP1**  

**DEF2** `DEFINITION` Sec. 2  
A lattice genome is the spatially resolved collection of lattice genes, Z in R^(HxWxd), over a statistically representative area or volume of a material in a given state.  
→ depends on **DEF1**  
→ supports **CLAIM2**  
→ motivates **Q1**  
⚠ untested assertion: Statistical representativeness of the maps used is never assessed.  

**Q1** `QUESTION` Sec. 2  
Can the lattice genome support visualization, segmentation and heterogeneity quantification as done in conventional EBSD workflows?  

## Methods and data

**METH1** `METHOD` Sec. 3, 4  
Kikuchi patterns are encoded with the pretrained VAE encoder of Calvat et al.; one of 128 latent dimensions is dropped because it mainly captures measurement geometry, giving d = 127.  
Evidence: none: Geometry-tracking of the dropped dimension stated but not shown.  
→ supports **LIM3** *(annotator)*  

**METH2** `METHOD` Sec. 3, 4.1  
Latent component maps are built by PCA of all lattice genes of one map and mapping PC1-3 to RGB; optionally each latent dimension is first rescaled so its 1st and 99th percentiles map to 0 and 1.  
Evidence: none given  

**METH3** `METHOD` Sec. 3  
Neighbouring pixels are merged into one domain if both the latent angle A and the latent Euclidean distance D are below thresholds A* and D*, scanning row by row over right and down neighbours; domains under 6 pixels are dismissed.  
Evidence: argument (Eq. 1a, 1b)  
→ analog of **GrainSegmentation**  
⚠ reproducibility: Label-conflict resolution during the row scan not specified.  

**ASM1** `ASSUMPTION` Sec. 3  
Absolute latent-space thresholds do not transfer between microstructures, so A* and D* are set to the p-th percentile of each map's own A and D distributions.  
Evidence: data_qualitative (Fig. S1/8)  
Basis: author choice. Open question: Does a fixed percentile assume a fixed fraction of boundary pixel pairs in every map?  

**ASM2** `ASSUMPTION` Sec. 3 *(hedged)*  
The elbow of the within-cluster sum of squares vs. number-of-clusters curve corresponds to the optimal microstructure segmentation.  
Evidence: argument: "We expect the elbow region corresponds to an optimal segmentation."  
Basis: community accepted. Open question: Does the WCSS elbow coincide with physically meaningful boundaries, or only with a statistical knee?  
→ supports **CLAIM5** [logical, weak, high uncertainty]  
⚠ untested assertion: Elbow is a heuristic without physical meaning; not validated against a ground truth.  

**ASM3** `ASSUMPTION` Sec. 4.2  
Grain maps from 5 degree misorientation thresholding are an adequate reference for judging a microstructure segmentation.  
Evidence: citation [29]  
Basis: community accepted. Open question: Which of the extra latent domains are real boundaries the 5 degree reference misses, and which are artifacts?  

**ASM4** `ASSUMPTION` Sec. 4.3  
KAM and GOS are accepted measures of local and grain-level microstructural heterogeneity, so agreement with them indicates a meaningful heterogeneity metric.  
Evidence: citation [6, 35]  
Basis: community accepted. Open question: If KLVS differs from KAM, which one is closer to the true defect content?  

**METH4** `METHOD` Sec. 3, Suppl.  
The percentile p is scanned from 95 to 60 in steps of 1 and the search stops when three consecutive relative WCSS reductions fall below 10 % of the mean of the first eight; p* is the middle of that window.  
Evidence: none: The 60-95 range is from "preliminary tests" not shown.  
→ depends on **ASM1**  
→ depends on **ASM2**  
⚠ ad hoc parameter: Range 60-95, 8-step baseline, 10 % and 3-step window are not justified.  

**METH5** `METHOD` Sec. 4.3  
Kernel latent vector spread (KLVS) of a pixel is the mean latent angle between its lattice gene and those of its nearest neighbours.  
Evidence: argument (Eq. 3)  
→ analog of **KAM**  
⚠ internal inconsistency: Text says "average cosine angle", the equation uses the arccos angle; Sec. 5 cites Eq. 6 (which is D-KLVS) for KLVS.  

**METH6** `METHOD` Sec. 4.3  
Latent vector spread (LVS) of a domain is the mean latent angle between each pixel's lattice gene and the domain centroid.  
Evidence: argument (Eq. 4)  
→ analog of **GOS**  
⚠ internal inconsistency: Fig. 7 caption says 'lattice vector spread'.  

**DATA1** `DATA` Sec. 4  
Three EBSD maps with raw Kikuchi patterns are analysed, all from Calvat et al. - wrought fully recrystallized IN718 (RX), partially recrystallized Waspaloy (W), and as-built DED IN718 (AM).  
Evidence: none given  
Scope: IN718, Waspaloy; n = 3; Single encoder; whether it was trained on these maps is not stated.  

## Observations

**OBS1** `OBSERVATION` Sec. 4.1  
In the three maps, the first three principal components of the lattice genes explain 25-37 % of the variance, and about 20 components are needed to explain nearly 100 %.  
Evidence: data_quantitative (Fig. 2c)  
Scope: n = 3  
→ qualifies **CLAIM3**  
→ supports **CLAIM1a** [quantitative, intermediate, medium uncertainty] *(annotator)*  

**OBS2** `OBSERVATION` Sec. 4.1  
Latent component maps capture the grain-scale heterogeneity seen in IPF orientation maps in all three microstructure states.  
Evidence: data_qualitative (Fig. 2a,b)  
Scope: n = 3  
→ supports **CLAIM3** [qualitative, intermediate, medium uncertainty]  

**OBS3** `OBSERVATION` Sec. 4.1 *(hedged)*  
Latent component maps show features faint or absent in IPF maps - preparation deformation and an extra grain (RX), smooth intragranular gradients likely from orientation variation (W), and substructure likely from dislocation cells (AM).  
Evidence: data_qualitative (Fig. 2d A-D)  
Modality: causal  
→ supports **CLAIM3** [qualitative, weak, high uncertainty]  
⚠ untested assertion: Physical interpretation not checked by an independent technique.  

**OBS4** `OBSERVATION` Sec. 4.1  
Pre-PCA per-dimension scaling reveals an annealing twin and intragranular gradients missed by unscaled latent component maps and otherwise visible only in single-dimension maps.  
Evidence: data_qualitative (Fig. 3)  
→ supports **CLAIM3** [qualitative, intermediate, medium uncertainty]  

**OBS5** `OBSERVATION` Sec. 4.1  
In a 2D PCA projection, lattice genes form visible clusters, most clearly for the RX microstructure.  
Evidence: data_qualitative (Fig. 4)  
→ motivates **METH3**  

**OBS6** `OBSERVATION` Sec. 4.2  
The early-stopping search selects percentile thresholds p76 (RX), p80 (W) and p73 (AM).  
Evidence: data_quantitative (Sec. 4.2, Fig. S2/9)  
→ depends on **METH4**  
→ supports **CLAIM5** [quantitative, intermediate, medium uncertainty]  

**OBS7** `OBSERVATION` Sec. 4.2  
Latent domain boundaries largely coincide with grain boundaries from 5 degree misorientation thresholding, most closely for RX and W.  
Evidence: data_qualitative (Fig. 5a)  
→ supports **CLAIM4** [qualitative, intermediate, medium uncertainty]  
⚠ missing quantification: No boundary overlap metric given.  

**OBS8** `OBSERVATION` Sec. 4.2  
Latent segmentation yields more domains than misorientation segmentation yields grains in all three microstructures.  
Evidence: data_quantitative (Fig. 5a)  
→ supports **CLAIM4** [quantitative, weak, high uncertainty]  

**OBS9** `OBSERVATION` Sec. 4.2  
Latent segmentation misses some grain boundaries - those of small grains in AM and W, those near poorly indexed regions in RX, and a few regular grain boundaries.  
Evidence: data_qualitative (Fig. 5a)  
→ undercuts **CLAIM4** *(annotator)*  

**OBS10** `OBSERVATION` Sec. 4.2  
Area distributions of latent domains and misorientation grains closely match for RX and W but not for AM.  
Evidence: data_qualitative (Fig. 5b): No statistical test.  
→ supports **CLAIM4** [qualitative, intermediate, medium uncertainty]  

**OBS11** `OBSERVATION` Sec. 4.3  
KLVS and KAM maps show the same qualitative trends - high values at boundaries in RX, elevated values throughout W, and patches in AM.  
Evidence: data_qualitative (Fig. 6)  
→ supports **CLAIM6** [qualitative, intermediate, medium uncertainty]  

**OBS12** `OBSERVATION` Sec. 4.3  
High-KAM artifacts from poorly indexed grains (RX) and a polishing scratch (W) are absent or weaker in KLVS maps.  
Evidence: data_qualitative (Fig. 6)  
→ supports **CLAIM6** [qualitative, intermediate, medium uncertainty]  

**OBS13** `OBSERVATION` Sec. 4.3  
KLVS resolves intragranular substructure in large AM grains that is not visible in KAM.  
Evidence: data_qualitative (Fig. 6b)  
→ supports **CLAIM6** [qualitative, weak, high uncertainty]  

**OBS14** `OBSERVATION` Sec. 4.3  
KLVS values span 0-120 degrees whereas KAM spans 0-8 degrees, so absolute values are not comparable.  
Evidence: data_quantitative (Fig. 6 colour bars)  

**OBS15** `OBSERVATION` Suppl.  
Distance-based KLVS maps are similar to angle-based KLVS maps.  
Evidence: data_qualitative (Fig. S3/10)  
→ supports **CLAIM8** [qualitative, strong, low uncertainty]  

**OBS16** `OBSERVATION` Sec. 4.3  
LVS maps show the same trends as GOS maps - low in RX, high in W, intermediate in AM.  
Evidence: data_qualitative (Fig. 7a,b)  
→ supports **CLAIM7** [qualitative, intermediate, medium uncertainty]  

**OBS17** `OBSERVATION` Sec. 4.3  
Area-weighted LVS and GOS distributions differ, most strongly for AM; for RX and W they show similar but shifted peaks.  
Evidence: data_qualitative (Fig. 7c)  
→ qualifies **CLAIM7**  

## Claims

**CLAIM1a** `CLAIM` Sec. 2  
The VAE latent vector of a Kikuchi pattern is a compact, low-dimensional representation of the pattern.  
Evidence: argument  
Modality: descriptive  
→ supports **HYP1** [logical, intermediate, medium uncertainty]  
⚠ missing quantification: Pattern size vs. latent size (128) never stated. Fig. 2c (~20 PCs explain ~100 %) could support compactness but is not used for it.  
**Verdict: ◐ PARTIAL**. Fig. 2c (about 20 PCs explain nearly all variance) supports compactness, but the paper does not use it that way and gives no size ratio.  
Missing: Compression ratio of pattern pixels to latent dimensions  
Missing: Intrinsic dimensionality vs. reconstruction error  

**CLAIM1b** `CLAIM` Sec. 2  
With a pretrained encoder, the latent vector is obtained from a measured pattern by a single forward pass, so it is experimentally accessible.  
Evidence: argument  
Modality: descriptive  
→ supports **HYP1** [logical, strong, low uncertainty]  
**Verdict: ✓ YES**. True by construction: a pretrained encoder maps a measured pattern in one forward pass.  

**CLAIM1c** `CLAIM` Sec. 2  
Distance between latent vectors of Kikuchi patterns reflects the physical similarity of the probed lattice (crystallography, orientation, defects), and the continuous latent space avoids discontinuities of space-group classification.  
Evidence: argument  
Modality: correlational  
→ supports **HYP1** [logical, weak, high uncertainty]  
⚠ untested assertion: Never tested, e.g. latent distance vs. misorientation or vs. dislocation density.  
⚠ unacknowledged conflict: Undercut by LIM2 and LIM3 (no symmetry reduction; measurement conditions encoded).  
**Verdict: ✗ NO**. No data tests it, and the paper's own limitations (no symmetry reduction; measurement conditions encoded) contradict it.  
Missing: Latent distance vs. misorientation (symmetry-reduced) for the same pixel pairs  
Missing: Latent distance vs. GND density  
Missing: Same sample measured with two detector geometries  
Obligation (open): Show that latent distance increases with misorientation, after symmetry reduction  
Obligation (open): Show that latent distance is insensitive to detector geometry and noise  

**CLAIM1d** `CLAIM` Sec. 2  
Because the Kikuchi pattern can be reconstructed from it, the latent vector encodes lattice parameter, orientation, strain and defect density, and maps near-uniquely to the local lattice state within reconstruction error.  
Evidence: argument; citation [15]  
Modality: conceptual  
→ supports **HYP1** [logical, weak, high uncertainty]  
⚠ untested assertion: Reconstruction shows code determines the pattern, not that the pattern uniquely determines the lattice state. Reconstruction error not reported.  
**Verdict: ? INCONCLUSIVE**. Rests on an inference from reconstruction; reconstruction error is not reported and the pattern-to-lattice-state uniqueness is not shown.  
Missing: Reconstruction error statistics  
Missing: Recovery of orientation, strain and dislocation density from decoded patterns  

**CLAIM2** `CLAIM` Sec. 2  
The lattice genome extends the materials genome concept to heterogeneous crystalline materials at the mesoscale.  
Evidence: argument: Analogy with biological genome; decoder as "ribosome".  
Modality: conceptual  
→ answers **GAP1**  
→ supports **OUT5**  
**Verdict: ? INCONCLUSIVE**. Framing claim by analogy; no data can decide it.  

**CLAIM3** `CLAIM` Sec. 4.1, 6  
PCA-based latent component maps are an analog of orientation maps that reveal finer microstructural heterogeneity than IPF maps.  
Evidence: none given  
Modality: comparative  
Scope: IN718, Waspaloy; n = 3  
→ answers **Q1**  
**Verdict: ◐ PARTIAL**. Agreement with IPF maps is shown visually; 'finer heterogeneity' is interpreted as likely physics without an independent check.  
Missing: Independent characterization (e.g. HR-EBSD, ECCI) of the extra features  

**CLAIM4** `CLAIM` Sec. 4.2, 6  
Segmentation by latent angle and distance thresholds produces domain maps consistent with misorientation grain maps while being more sensitive.  
Evidence: none given  
Modality: comparative  
Scope: IN718, Waspaloy; n = 3  
→ answers **Q1**  
→ depends on **ASM3** [medium uncertainty] *(annotator)*  
⚠ unfalsifiable validation: Agreement is counted as validation, extra domains as higher sensitivity; no independent ground truth.  
⚠ unaddressed counterevidence: Missed grain boundaries (OBS9) not weighed against the claim.  
**Verdict: ◐ PARTIAL**. Boundary agreement is shown visually and counts are given; 'more sensitive' is not distinguished from artifacts or pattern overlap (LIM4), and missed boundaries are not weighed.  
Missing: Boundary precision/recall against a reference  
Missing: Ground truth for the extra domain boundaries  
Obligation (partially discharged): Show that domain boundaries coincide with grain boundaries, quantitatively ← OBS7, OBS8, OBS10  
Obligation (open): Show that extra domain boundaries are real microstructural features, not artifacts or pattern overlap  
Obligation (open): Explain the missed grain boundaries  

**CLAIM5** `CLAIM` Sec. 5, Suppl.  
A single percentile parameter with automatic elbow detection produces suitable segmentations across microstructures with very different statistics, without case-by-case calibration.  
Evidence: none given  
Modality: generalization  
Scope: n = 3  
⚠ overgeneralization: Supplement says it 'readily generalizes to any EBSD dataset' from n = 3.  
**Verdict: ◐ PARTIAL**. The procedure ran on three FCC Ni datasets; suitability rests on the elbow assumption and generality beyond n = 3 is not tested.  
Missing: Sensitivity of the result to the early-stopping constants  
Missing: Tests on other crystal structures and instruments  

**CLAIM6** `CLAIM` Sec. 4.3, 6  
KLVS reproduces KAM trends with better contrast for real features and fewer artifacts, because it operates on the encoded pattern rather than on indexed orientations.  
Evidence: argument: Mechanism.  
Modality: causal  
→ answers **Q1**  
→ depends on **ASM4** [low uncertainty] *(annotator)*  
⚠ missing quantification: Contrast judged by eye; no contrast or SNR metric.  
⚠ causal overreach: Mechanism ('because it operates on the encoded pattern') inferred from visual comparison only.  
**Verdict: ◐ PARTIAL**. Trend agreement with KAM is visible; better contrast and fewer artifacts are judged by eye, and the mechanism is argued, not tested.  
Missing: Contrast-to-noise metric for KLVS vs. KAM  
Missing: Controlled test with artificially perturbed patterns  
Obligation (discharged): Show that KLVS reproduces KAM trends ← OBS11  
Obligation (open): Quantify the contrast gain over KAM  
Obligation (open): Test that artifact robustness comes from operating on encoded patterns  

**CLAIM7** `CLAIM` Sec. 4.3, 6  
LVS is a high-dimensional analog of GOS that recovers qualitatively similar trends of grain-level heterogeneity.  
Evidence: none given  
Modality: comparative  
→ answers **Q1**  
→ depends on **ASM4** [low uncertainty] *(annotator)*  
⚠ confounded comparison: LVS is computed on latent domains, GOS on grains, so metric and segmentation differences are mixed.  
⚠ overclaim: Conclusion attributes "better contrast" to the spreads; only shown (by eye) for KLVS.  
**Verdict: ◐ PARTIAL**. Qualitative trends match GOS, but the distributions differ and the comparison mixes metric and segmentation.  
Missing: LVS computed on the conventional grains  

**CLAIM8** `CLAIM` Sec. 4.3  
Angle and Euclidean distance in the latent space are consistent descriptors of local microstructural variation.  
Evidence: none given  
Modality: correlational  
**Verdict: ✓ YES**. Fig. S3 shows similar maps for both metrics; the claim is modest.  

**CLAIM9** `CLAIM` Sec. 5, 6  
Lattice-genome analysis needs no pattern indexing and is therefore applicable to patterns that are hard to index, such as heavily deformed or multiphase regions.  
Evidence: argument; citation [10]  
Modality: generalization  
→ supports **OUT5**  
⚠ overgeneralization: Not demonstrated; all three maps are single-phase and indexable.  
**Verdict: ? INCONCLUSIVE**. Plausible from the method, but no hard-to-index or multiphase data is analysed.  
Missing: Analysis of heavily deformed or multiphase regions where indexing fails  

**CLAIM10** `CLAIM` Sec. 5  
One encoded lattice genome can serve many downstream tasks without reprocessing raw patterns.  
Evidence: argument  
Modality: conceptual  
→ supports **OUT5**  
**Verdict: ? INCONCLUSIVE**. Argued from the design; no downstream task is demonstrated.  

## Limitations (stated by authors)

**LIM1** `LIMITATION` Sec. 5  
Latent component map colours are dataset-dependent because PCA is fitted per map, unlike the universal IPF colour scheme.  
Evidence: none given  
Kind: scope  
→ qualifies **CLAIM3**  

**LIM2** `LIMITATION` Sec. 5  
Crystal symmetry is encoded only implicitly in lattice genes; latent angles are not symmetry-reduced, so KLVS and LVS are systematically larger than KAM and GOS and do not match them quantitatively.  
Evidence: argument  
Kind: method  
→ alternative explanation for **OBS14**  
→ alternative explanation for **OBS17**  
→ undercuts **CLAIM1c** *(annotator, background knowledge)*  

**LIM3** `LIMITATION` Sec. 5  
Lattice genes also encode measurement conditions (detector geometry, pattern centre, background, noise), complicating comparisons across datasets.  
Evidence: citation [36]  
Kind: data  
→ undercuts **CLAIM6** *(annotator)*  
→ undercuts **CLAIM1c** *(annotator)*  
→ undercuts **CLAIM1d** *(annotator)*  

**LIM4** `LIMITATION` Sec. 5  
Where the interaction volume spans several lattices, e.g. at grain or twin boundaries, the lattice gene encodes a superposition, which is harder to interpret but makes the encoding sensitive to overlaps.  
Evidence: citation [37, 38, 39, 15]  
Modality: causal  
Kind: interpretation  
→ alternative explanation for **OBS8**  

## Outlook

**OUT1** `OUTLOOK` Sec. 5  
Rotation-invariant or conditional, disentangling encoders could make symmetry explicit and separate physical quantities in the latent space.  
Evidence: citation [40, 41, 42]  
→ answers **LIM2**  

**OUT2** `OUTLOOK` Sec. 5 *(hedged)*  
Training on large, diverse diffraction datasets can yield a unique, instrument-invariant encoding with a universal distance metric.  
Evidence: none  
→ answers **LIM3**  

**OUT3** `OUTLOOK` Sec. 5, 6  
The lattice-genome analysis tools are encoder-agnostic and will remain applicable as encoder architectures evolve.  
Evidence: argument  

**OUT4** `OUTLOOK` Sec. 5  
Lattice genomes can be extended to chord-length and n-point statistics, multiphase materials, EDS coupling and machine-learning property prediction.  
Evidence: citation [43-49]  
→ supports **OUT5**  

**OUT5** `OUTLOOK` Sec. 5 *(hedged)*  
The lattice genome may offer a practical realization of the Materials Genome Initiative vision for heterogeneous crystalline materials at the mesoscale.  
Evidence: none given  
