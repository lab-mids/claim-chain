# claim-chain report: Characterization of Microstructure and Mechanical Properties of Cast Materials using Advanced Techniques

Bharat Singh, C Praveen Kumar, Ravi Kalra, Koushal Dhamija, Zahraa N. Salman, Manish Kumar (2023), doi:10.1051/e3sconf/202343001111. Generated; do not edit by hand.

## 1. Logic

**Overall: ? INCONCLUSIVE** · **Logic score: 0.32** · weighted: 0.30 · proof obligations discharged: 0.00 (of 9)  
Score method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting). Weighted: as the logic score, but MAIN_CONCLUSION weighs 3, COUNTER_CLAIM 0 and every other claim or hypothesis 1 (draft weighting).  
Verdicts: 1 YES, 2 PARTIAL, 2 WEAK, 12 INCONCLUSIVE, 1 NO.

The paper reports one set of round-number microstructure and property values for three sand-cast alloys (A356, gray cast iron, SS316). Their phase descriptions match the known microstructures, and Table 1 does show a wide spread of properties. The headline claims do not hold. The 'strong correlations' rest on three different base metals with no reported statistics. Phase distribution and defects are never quantified. No casting-parameter value or per-condition result appears anywhere, so the process-microstructure-property conclusions and the optimization payoff are asserted, not shown. The paper also misprints the Hall-Petch equation, calls 5 % ductility 'high', reports a corrosion figure with no method, and cites references that do not match the studies attributed to them.

**Score from derived verdicts: 0.31**, 2 claim(s) where the derived verdict differs from the annotator's. Method: verdicts derived from the links: an incoming CONTRADICTS gives NO; otherwise the strongest support link decides (STRONG YES, INTERMEDIATE PARTIAL, WEAK WEAK, none INCONCLUSIVE); UNDERCUTS, QUALIFIES or an alternative explanation caps at PARTIAL; CONDITIONALLY_SUPPORTS counts as WEAK at most; an essential link caps the claim at its own strength and at the derived verdict of the claim it comes from. Links without a strength count as INTERMEDIATE. Claims without links keep the annotator's verdict.  

| Statement | Role | Modality | Authors say | Verdict | Derived | Rationale |
|---|---|---|---|---|---|---|
| **CLAIM16** The study of a variety of industrially relevant cast alloys provides a comprehensive understanding of their behaviour under different casting conditions and reveals a strong correlation between grain size, phase distribution and defect morphology on one side and hardness, yield strength and ductility on the other. | main conclusion | generalization | demonstrated | ? INCONCLUSIVE | same | No result is reported per casting condition and phase distribution and defect morphology are never quantified; only the grain-size ranking against hardness and yield over three different alloys exists, which does not decide the claim as worded. |
| **CLAIM1** The XRD patterns confirm the phases observed by SEM in the three cast materials. | intermediate | comparative | demonstrated | ◐ PARTIAL | same | The reported XRD phases match the matrix phases and carbides named from SEM, but graphite in gray cast iron is not confirmed and no pattern is shown, so confirmation rests on text alone. |
| **CLAIM2** Statistical analysis of the data reveals strong correlations between the microstructural features and the mechanical properties of the cast materials. | main conclusion | correlational | demonstrated | ◔ WEAK | **? INCONCLUSIVE** | Only grain size is quantified, and over three different alloy systems its ranking inversely matches hardness and yield (OBS6); no statistics are reported, phase distribution and defects are never quantified, and UTS and ductility do not follow grain size. |
| **CLAIM3** Grain size correlates inversely with hardness and yield strength in the cast materials studied. | quantitative support | correlational | demonstrated | ◔ WEAK | **? INCONCLUSIVE** | Table 1 shows the inverse ranking exactly (OBS6), but over only three different alloys with no replicates, and one 'grain size' is a colony size, so the correlation is thin and uncontrolled. |
| **CLAIM4** The inverse dependence of hardness and yield strength on grain size in the cast materials is consistent with Hall-Petch grain-boundary strengthening. | mechanistic interpretation | causal | proposed | ? INCONCLUSIVE | same | No within-material grain-size variation is shown, so the data cannot decide whether grain boundaries cause the trend; the cross-alloy comparison gives inconsistent and implausibly large implied Hall-Petch slopes. |
| **CLAIM5** Phase distribution significantly influences hardness and ultimate tensile strength of the cast materials. | intermediate | causal | demonstrated | ? INCONCLUSIVE | same | The paper reports no quantity describing phase distribution, so no data relate it to hardness or UTS. |
| **CLAIM6** Defect morphology affects the ductility of the cast materials. | intermediate | causal | demonstrated | ? INCONCLUSIVE | same | Defect morphology is mentioned as an SEM capability but never measured, so nothing in the paper links it to the ductility values. |
| **CLAIM7** Pouring temperature and cooling rate affect grain size, phase distribution and defect morphology of the cast materials, which in turn influence their mechanical properties. | main conclusion | causal | demonstrated | ? INCONCLUSIVE | same | The paper presents no data at all on casting parameters, so the claimed process-microstructure-property chain is asserted rather than shown. |
| **CLAIM8** The results give a comprehensive understanding of the microstructure and mechanical properties of the cast materials and their dependence on casting parameters, and offer insights for optimizing the casting process and tailoring properties. | main conclusion | generalization | demonstrated | ? INCONCLUSIVE | same | Without any casting-parameter data or process-property relation in the paper, the optimization payoff cannot be judged. |
| **CLAIM9** SEM, XRD and EBSD reveal for each material the phases and grain structures typically associated with it (dendrites and secondary phases in Aluminium Alloy 356, pearlite and graphite flakes in gray cast iron, austenite and carbides in Stainless Steel 316). | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | The reported phase descriptions match the textbook microstructures, but no micrograph, map or pattern is tied to the results (Fig. 1 judged from its caption only) and XRD does not show graphite. |
| **CLAIM10** The austenitic matrix and carbide precipitates of Stainless Steel 316 reflect its high-temperature stability and corrosion resistance. | intermediate | causal | demonstrated | ? INCONCLUSIVE | same | No corrosion or high-temperature test is described; Fig. 4 has no method and is judged from its caption only, and grain-boundary Cr23C6 is usually linked to reduced, not improved, corrosion resistance. |
| **CLAIM18** Nanoindentation and tensile testing show a wide range of mechanical properties across the three cast materials. | intermediate | descriptive | demonstrated | ✓ YES | same | Table 1 spans hardness 80-200 HV, modulus 70-210 GPa, UTS 310-500 MPa and ductility 1-30 %, which is a wide range for three different base metals. |
| **CLAIM11** Aluminium Alloy 356 combines relatively low hardness and yield strength with high ductility, which suits it to lightweight parts needing good formability. | intermediate | comparative | demonstrated | ✗ NO | same | The low hardness and yield part holds, but the paper's own Table 1 gives A356 only 5 % ductility against 30 % for SS316, so 'high ductility' and the formability argument built on it are contradicted. |
| **CLAIM12** The property profiles make Aluminium Alloy 356 suitable for automotive parts, gray cast iron ideal for engine blocks needing high strength and vibration damping, and Stainless Steel 316 versatile for chemical-processing equipment needing strength, ductility and corrosion resistance. | intermediate | generalization | demonstrated | ? INCONCLUSIVE | same | These are handbook application statements; the properties they rest on (damping, corrosion, formability) are not measured in the paper. |
| **CLAIM13** Secondary phases raise hardness and UTS through load transfer and dislocation pinning, and defects lower ductility by acting as stress concentrators and fracture initiation sites. | mechanistic interpretation | causal | proposed | ? INCONCLUSIVE | same | Textbook mechanisms are named but nothing in the paper (no fractography, TEM or defect statistics) tests them for these samples. |
| **CLAIM14** The study demonstrates the power of advanced characterization techniques in revealing the intricate relationships between microstructure, mechanical properties and processing parameters in cast materials. | main conclusion | comparative | demonstrated | ? INCONCLUSIVE | same | Without a baseline using conventional methods and with no processing data, the paper cannot show what the advanced techniques add or that processing relationships were revealed. |
| **CLAIM15** The research successfully elucidated the intricate relationships between microstructural features and mechanical properties of Aluminium Alloy 356, gray cast iron and Stainless Steel 316 and their dependence on casting parameters, and the strong correlations found underscore the pivotal role of microstructure. | intermediate | causal | demonstrated | ? INCONCLUSIVE | same | Restates CLAIM2 and CLAIM7; the microstructure-property part rests only on a three-alloy ranking and the casting-parameter part on no data. |
| **CLAIM17** The research reaffirms that the properties of a material are determined by its structure and that the structure can be controlled by processing. | intermediate | generalization | demonstrated | ? INCONCLUSIVE | same | The structure-property step is only a cross-alloy ranking, and the processing-structure step has no data in the paper. |

**Support links tested on the five criteria** (directness, sufficiency, controls, alternatives, scope match; ✓ met, ◐ partly, ✗ not met, – not applicable):

| Link | Criteria | Strength | Note |
|---|---|---|---|
| OBS2 → CLAIM1 (essential) | ✓◐––◐ | intermediate | Phases listed in text only, no pattern; graphite not confirmed. |
| OBS1 → CLAIM9 (essential) | ✓◐––◐ | intermediate | Descriptions only; micrographs not tied to results. |
| OBS6 → CLAIM3 (essential) | ✓✗✗◐◐ | unsupported (annotator: weak) | Exact inverse ranking but n = 3 with no replicates; each point a different base metal; one 'grain size' is a colony size. |
| CLAIM3 → CLAIM2 (essential) | ◐✗✗✗◐ | unsupported (annotator: weak) | Only grain size of the three named features is quantified; three alloys; alloy chemistry not controlled. |
| CLAIM3 → CLAIM4 (essential) | ✗✗✗✗✗ | unsupported | Hall-Petch concerns grain size within one material; the evidence compares three base metals. |
| OBS1 → CLAIM5 | ✗✗✗✗✗ | unsupported | Qualitative phase names only; no phase distribution metric related to properties. |
| OBS1 → CLAIM6 | ✗✗✗✗✗ | unsupported | No defect measurement reported. |
| DATA1 → CLAIM7 (essential) | ✗✗✗✗✗ | unsupported | Parameters said to be varied but no values or per-condition results given. |
| CLAIM7 → CLAIM8 (essential) | ◐✗✗✗✗ | unsupported | Optimization insight would follow only from parameter-property data, which are absent. |
| CLAIM2 → CLAIM16 (essential) | ◐✗✗✗◐ | unsupported (annotator: weak) | Three alloys; no per-condition data. |
| OBS8 → CLAIM10 | ◐✗✗✗✗ | unsupported | Figure with no method; caption only. |
| DATA2 → CLAIM18 (essential) | ✓✓––✓ | strong | Differences of factors 3-30 between materials far exceed any plausible scatter. |
| OBS5 → CLAIM11 | ✓◐––✗ | unsupported | Supports low hardness and yield but not 'high ductility'. |
| OBS5 → CLAIM12 | ✗◐–◐✗ | unsupported (annotator: weak) | Strength and ductility only; damping, corrosion, formability unmeasured. |
| OBS1 → CLAIM13 | ✗✗✗✗✗ | unsupported | No fractography, TEM or quantified phases/defects. |
| CLAIM2 → CLAIM14 (essential) | ✗✗✗◐✗ | unsupported (annotator: weak) | No comparison with conventional techniques; relationship rests on averages obtainable by optical metallography. |

**Golden thread** (each aim from the introduction to the end of the paper):

| Aim | Gap | Method | Result | Claim (verdict) | Outcome |
|---|---|---|---|---|---|
| **AIM1** The paper characterizes the microstructure and mechanical properties of a variety of industrially relevant cast materials with SEM, XRD, EBSD, nanoindentation and tensile testing. | GAP1 | DATA1, DATA2 | - | - | METHOD ONLY |
| **AIM2** The paper correlates microstructural features with mechanical properties to gain insight into the behaviour of cast materials under different casting conditions. | - | METH6 | - | CLAIM2 (◔), CLAIM15 (?) | DELIVERED |
| **AIM3** The paper shows the influence of casting parameters on microstructure and properties and so offers guidelines for optimizing casting processes (promised payoff). | GAP2 | - | - | CLAIM7 (?), CLAIM8 (?) | DELIVERED |
| **AIM4** The paper underscores the importance of integrated microstructural and mechanical characterization for understanding and predicting the performance of cast materials (promised payoff). | GAP1 | - | - | CLAIM14 (?) | NOT RESTATED |

Outcomes: DELIVERED, NOT RESTATED (delivered but absent from the conclusion and abstract), METHOD ONLY (carried out but no result shown), DROPPED (nothing delivers it).

**Presented as demonstrated, but the verdict is weak, inconclusive or no:** CLAIM16 (INCONCLUSIVE), CLAIM2 (WEAK), CLAIM3 (WEAK), CLAIM5 (INCONCLUSIVE), CLAIM6 (INCONCLUSIVE), CLAIM7 (INCONCLUSIVE), CLAIM8 (INCONCLUSIVE), CLAIM10 (INCONCLUSIVE), CLAIM11 (NO), CLAIM12 (INCONCLUSIVE), CLAIM14 (INCONCLUSIVE), CLAIM15 (INCONCLUSIVE), CLAIM17 (INCONCLUSIVE).

**Recomputed checks:**

- **OBS6** grain size ranking inverse to hardness and yield rankings ✓ satisfied (recomputed)
- **OBS6** yield strength exactly linear in grain size (equal slopes) ✓ satisfied (recomputed)
- **OBS6** UTS does not follow the grain-size ranking ✓ satisfied (recomputed)
- **OBS6** ductility does not follow the grain-size ranking ✓ satisfied (recomputed)
- **OBS7** k from Al 356 and gray iron (MPa m^1/2) = 2.414 MPa m^1/2 (recomputed)
- **OBS7** k from Al 356 and SS316 (MPa m^1/2) = 3.232 MPa m^1/2 (recomputed)
- **OBS7** k from SS316 and gray iron (MPa m^1/2) = 1.927 MPa m^1/2 (recomputed)
- **CLAIM11** A356 ductility relative to SS316 = 0.167 (recomputed)
- **CLAIM11** A356 has the highest ductility of the three ✗ not satisfied (recomputed)

**Statements per paper part:**

| Part | Statements |
|---|---|
| abstract | CLAIM16 |
| introduction | BG1, BG2, GAP1, BG3, GAP2, AIM1, AIM2, AIM3, AIM4 |
| methods | DATA1, METH1, METH2, METH3, METH4, METH5, METH6 |
| results | OBS1, OBS2, CLAIM1, OBS3, OBS4, OBS5, DATA2, OBS6, OBS7, DEF1, CLAIM2, CLAIM3, CLAIM4, CLAIM5, CLAIM6, CLAIM7, CLAIM8 |
| discussion | CLAIM9, OBS8, CLAIM10, CLAIM18, CLAIM11, CLAIM12, CLAIM13, CLAIM14, OUT1 |
| conclusion | CLAIM15, CLAIM17, OUT2 |

Causal claims (check against correlational evidence): CLAIM4, CLAIM5, CLAIM6, CLAIM7, CLAIM10, CLAIM13, CLAIM15.

## 2. Limitations

- No casting-parameter data or per-condition results, although casting-parameter influence is a main conclusion (DATA1, DATA2, CLAIM7, CLAIM8, CLAIM15).
- Correlations rest on n = 3 different base metals with no replicates or reported regression/ANOVA/PCA output, so microstructure is confounded with alloy chemistry (METH6, OBS6, CLAIM2, CLAIM3).
- Hall-Petch consistency is asserted across alloys with a misprinted equation and implausible implied slopes (DEF1, OBS7, CLAIM4).
- Phase distribution, defect morphology and corrosion are never measured, yet conclusions are drawn about them (CLAIM5, CLAIM6, CLAIM10, CLAIM13, OBS8).
- Internal inconsistencies, namely 'high ductility' for 5 % elongation, colony size tabulated as grain size, HV units from Oliver-Pharr nanoindentation, and figure and reference numbering that do not match the text (CLAIM11, OBS3, METH4, BG3).

**Stated by the authors:**


**Assumptions the argument rests on:**


**Inference rules that are empirical, unstated, argued only by the authors, or weak:**

- **OBS6→CLAIM3**: A monotonic inverse ranking of property against grain size over the samples indicates an inverse correlation. (unstated)
- **CLAIM3→CLAIM2**: Correlation across samples of different alloys indicates a microstructure-property relationship. (unstated)

**Flagged by the annotator:**

- **CLAIM16** overclaim (high): Three alloys, each reported with a single set of values, are called a variety giving comprehensive understanding under different casting conditions; no condition-resolved data are shown.
- **CLAIM16** overclaim (high): Ductility is listed among the correlated properties, but in Table 1 ductility does not track grain size (r = 0.13) and phase distribution and defects are never quantified.
- **GAP1** untested assertion (medium): The gap is asserted without citation, and the paper never compares its advanced techniques with conventional ones, so the gap is not shown to be closed.
- **BG3** internal inconsistency (high): The reference list does not match the studies attributed to it: ref. 4 (cited for a hybrid Al 7075 composite) is on Pr3+-doped phosphate glasses, ref. 5 (Al 2024 with boron and graphite) on solar MPPT, ref. 13 (TiN/Al-7Si composite) on fenugreek seed toxicity, ref. 1 (Mg-Gd-Y-Zn-Al) on ECAP of Al6061.
- **BG3** reproducibility (medium): References 15-33 are never cited in the text.
- **DATA1** reproducibility (critical): No pouring temperatures, cooling rates, number of casting conditions, mould details or specimen counts are given, although the casting-parameter claims rest on them.
- **DATA1** reproducibility (high): Chemical compositions, melt treatment (e.g. modification, inoculation) and heat treatment state of the alloys are not reported.
- **DATA1** internal inconsistency (low): The methods say 'Figure 1 represents the casting process', but Fig. 1 is 'Microstructure Images' in the literature review and the casting flowchart is Fig. 2.
- **METH1** reproducibility (medium): Etchants, instrument, voltage and the number of fields imaged are not given; no EDS result is reported anywhere.
- **METH2** reproducibility (medium): No quantitative phase method (e.g. Rietveld) is described and no phase fractions or lattice parameters are reported, although 'quantitative phase information' is promised.
- **METH3** reproducibility (medium): Step size, map area, misorientation threshold for grain boundaries and the grain-size definition are not given.
- **METH4** reproducibility (high): Load, number of indents, indent locations (which phase) and the Poisson ratios used to convert Er to E are not reported.
- **METH4** internal inconsistency (medium): Eq. (2) gives hardness as load per contact area (GPa), yet results are reported in Vickers units (HV) without a stated conversion.
- **METH5** reproducibility (high): Specimen geometry, number of specimens, strain rate, yield definition (0.2 % offset) and ductility measure (elongation or reduction of area) are not given.
- **METH6** missing quantification (critical): No regression coefficient, ANOVA table, p-value or PCA loading is reported anywhere in the paper; with one row per material (three points) such analyses cannot be meaningful.
- **METH6** reproducibility (medium): Software, variables entered and sample sizes for the statistics are not named.
- **OBS1** reproducibility (high): The results cite no micrograph, and the only microstructure figure (Fig. 1) appears in the literature review, described as microstructures under different conditions with no labels in the text.
- **OBS2** reproducibility (medium): No pattern, peak list or phase fraction is shown.
- **OBS2** internal inconsistency (medium): Graphite, seen by SEM in gray cast iron, is not reported in its XRD, so XRD does not confirm all SEM phases; an 'Al-Si eutectic phase' is not a single crystalline phase with its own peaks (Si peaks would be expected).
- **OBS3** internal inconsistency (high): For gray cast iron the text reports pearlite colony size, but Table 1 lists it in the 'Grain Size' column and the Hall-Petch comparison treats it as grain size.
- **OBS3** missing quantification (medium): Single round averages without distribution, standard deviation or number of grains; no EBSD map is shown.
- **OBS4** missing quantification (high): Nanoindentation of multiphase cast materials gives phase-dependent local values, yet one round number per material is reported without scatter or indent count.
- **OBS4** unaddressed counterevidence (medium): A modulus of 210 GPa for flake-graphite gray cast iron is at the level of steel; bulk gray iron is usually far lower because of the graphite flakes, so the value is either a matrix value or implausible, and the paper does not say which (annotator background).
- **OBS5** missing quantification (high): No error bars, repeats or specimen counts; all values are round numbers and no value is given per casting condition.
- **OBS5** unaddressed counterevidence (low): A distinct 350 MPa yield strength for flake gray iron and 250 MPa for sand-cast A356 of unstated temper are high for these materials; the paper does not discuss them (annotator background).
- **DEF1** internal inconsistency (medium): The printed equation is wrong: the Hall-Petch relation is sigma_y = sigma_0 + k d^-1/2; the printed form puts k under the root in the denominator and is dimensionally inconsistent with k being a stress times sqrt(length).
- **CLAIM2** missing quantification (critical): 'Strong' is not backed by any reported coefficient, significance or replicate; n = 3 materials.
- **CLAIM2** confounded comparison (critical): Each data point is a different base metal (Al, cast iron, austenitic steel), so microstructure and alloy chemistry change together and the correlation cannot be attributed to microstructure.
- **CLAIM3** confounded comparison (high): The three points are three base metals; the gray-iron value is a pearlite colony size, not a grain size.
- **CLAIM3** missing quantification (medium): With n = 3, a perfect inverse ranking arises by chance with probability 1/6; no significance is given.
- **CLAIM4** causal overreach (high): Hall-Petch describes grain-size strengthening within one material; across Al, cast iron and steel the yield differences mainly reflect different base metals, friction stresses and strengthening phases (graphite, pearlite, carbides).
- **CLAIM4** arithmetic (medium): The implied Hall-Petch slopes (1.9-3.2 MPa m^1/2, OBS7) differ between pairs and are far above typical constants for these alloys; the equation is also misprinted (DEF1).
- **CLAIM5** untested assertion (high): Phase distribution is never quantified (no phase fractions, spacing or morphology metric), so 'significantly' has no data or test behind it.
- **CLAIM6** untested assertion (high): No porosity, inclusion or graphite-flake measurement is reported; ductility differences (1-30 %) are equally explained by the different base metals.
- **CLAIM7** untested assertion (critical): No pouring temperature, cooling rate or per-condition result appears anywhere; Table 1 has one row per material.
- **CLAIM8** overclaim (high): No guideline, process window or parameter-property relation is given, so the promised optimization insight is not delivered.
- **OBS8** reproducibility (high): Corrosion data appear in a figure with no method, medium, metric or sample description.
- **CLAIM10** untested assertion (medium): Neither high-temperature stability nor corrosion is measured by a described method.
- **CLAIM11** internal inconsistency (high): Table 1 gives A356 a ductility of 5 %, one sixth of SS316 (30 %); calling it high ductility and inferring good formability contradicts the paper's own table.
- **CLAIM12** untested assertion (medium): Damping, weight-specific properties, formability and corrosion are not measured.
- **CLAIM12** internal inconsistency (low): Gray cast iron is credited with high strength, but its UTS (400 MPa) is below that of SS316 (500 MPa) in Table 1.
- **CLAIM13** causal overreach (medium): Mechanisms are invoked without fractography, dislocation imaging or any quantified phase or defect data.
- **CLAIM14** overclaim (high): No comparison with conventional techniques is made; the only quantified microstructural feature (average grain size) is obtainable by optical metallography, and EDS, XRD quantification and local nanoindentation mapping produce no reported result.
- **CLAIM15** overclaim (high): The conclusion states the casting-parameter dependence as elucidated, although no casting-parameter data are reported, and states no limitation.

**Local checks per part** (issues found; failed derived checks count as arithmetic):

| Part | Completeness | Arithmetic | Consistency | Argument | High or critical |
|---|---|---|---|---|---|
| abstract | 0 | 0 | 0 | 2 | 2 |
| introduction | 1 | 0 | 1 | 1 | 1 |
| methods | 9 | 0 | 2 | 0 | 5 |
| results | 7 | 1 | 5 | 7 | 12 |
| discussion | 1 | 0 | 2 | 4 | 3 |
| conclusion | 0 | 0 | 0 | 1 | 1 |

## 3. Missing evidence

- Pouring temperature and cooling rate for each casting, with grain size, porosity, phase fractions and properties per condition
- Replicate tensile and hardness tests with scatter
- Within-alloy grain-size series to test Hall-Petch behaviour
- Reported regression coefficients, ANOVA tables and PCA loadings
- Quantified porosity and secondary-phase fractions, and fractography
- Described corrosion test method behind Fig. 4
- Comparison with conventional characterization to show what the advanced techniques add

**Open proof obligations:**

- **CLAIM16** (open, critical): Report microstructure and properties for each casting condition, not only one row per material. Needs: grain size, porosity fraction, phase fractions, hardness, yield strength, elongation per casting condition [um, %, HV, MPa, %] via EBSD, image analysis, XRD Rietveld, tensile tests.
- **CLAIM16** (open, high): Quantify the correlation (coefficient and significance) with replicates.
- **CLAIM2** (open, critical): Show the correlation within one alloy over varied microstructures, so that alloy chemistry is held constant. Needs: yield strength and hardness versus grain size within each alloy [MPa, HV, um] via tensile and hardness tests on castings with different cooling rates.
- **CLAIM2** (open, high): Report the statistical analyses the methods announce.
- **CLAIM2** (open, high): Quantify phase distribution and defect morphology. Needs: porosity fraction, secondary-phase fraction and spacing [%, um] via SEM image analysis and XRD Rietveld.
- **CLAIM7** (open, critical): Report the casting conditions and the microstructure obtained under each. Needs: pouring temperature, cooling rate, grain size, porosity [degC, K/s, um, %] via thermocouple-instrumented sand casting with EBSD and image analysis.
- **CLAIM7** (open, critical): Report properties for each condition with replicates. Needs: hardness, yield strength, elongation per condition [HV, MPa, %] via ASTM E8 tensile tests (n >= 3) and hardness.
- **CLAIM14** (open, high): Show a relation that only the advanced techniques could reveal.
- **CLAIM14** (open, critical): Show processing-parameter relationships with data.

**Per statement:**

- **CLAIM16**: Table of grain size, porosity and phase fractions with properties for each pouring temperature and cooling rate of each alloy
- **CLAIM1**: Indexed XRD patterns for each alloy including graphite and Si reflections
- **CLAIM2**: Within-alloy variation of grain size, porosity and phase fractions with properties over several casting conditions and replicates
- **CLAIM2**: Reported regression coefficients, ANOVA tables and PCA loadings
- **CLAIM3**: Grain-size series within each alloy with replicate hardness and tensile tests
- **CLAIM4**: Yield strength versus d^-1/2 for at least four grain sizes of one alloy
- **CLAIM5**: Secondary-phase fraction and spacing per sample with hardness and UTS
- **CLAIM6**: Porosity fraction and pore size per specimen with fractography and elongation
- **CLAIM7**: Grain size, porosity and properties of each alloy at several pouring temperatures and cooling rates
- **CLAIM8**: A process map relating pouring temperature and cooling rate to target properties for each alloy
- **CLAIM10**: Polarization or intergranular corrosion tests of the as-cast SS316 with carbide quantification
- **CLAIM14**: Side-by-side optical metallography and macro-hardness on the same samples showing what the advanced techniques add
- **CLAIM14**: Phase-resolved nanoindentation maps linked to EBSD
