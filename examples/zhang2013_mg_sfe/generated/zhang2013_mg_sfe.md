# Argument chain: First-principles study of stacking fault energies in Mg-based binary alloys

J. Zhang, Y. Dou, G. Liu, Z. Guo (2013), doi:10.1016/j.commatsci.2013.07.012. Generated from the claim-chain YAML (schema 0.6.0); do not edit by hand.

**Logic score: 0.55** (3 YES, 4 PARTIAL, 3 WEAK, 2 INCONCLUSIVE, 0 NO), weighted by claim role: 0.54. Method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting).

## Motivation

**BG1** `BACKGROUND`  Sec. 1, para. 1  
Magnesium alloys are the lightest structural metals, but wrought magnesium products such as sheets and extrusions are still rare.  
Evidence: none given  
→ motivates **BG2**  

**BG2** `BACKGROUND`  Sec. 1, para. 1  
Hcp magnesium has only two independent basal slip systems while compatible polycrystal deformation needs five, so non-basal slip and twinning must be activated to make magnesium formable.  
Evidence: citation [1, 2]  
→ motivates **AIM6**  

**BG3** `BACKGROUND`  Sec. 1, para. 2  
Stacking fault energy governs the deformation behaviour of metals, and solute atoms change it by disturbing the local charge density and strain field.  
Evidence: citation [3, 4, 5]  
→ motivates **BG4**  
→ motivates **AIM5**  

**BG4** `BACKGROUND`  Sec. 1, para. 3  
Studies of Mg-Y, Mg-Zn-Y and Mg-Li or Mg-Al link solute-induced changes of the I1 stacking fault energy to the active deformation modes and to ductility.  
Evidence: citation [6, 7, 8]  
→ motivates **GAP1**  
→ supports **CLAIM7** [logical, weak]  

**BG5** `BACKGROUND`  Sec. 1, para. 4  
Measured stacking fault energies of magnesium scatter between 50 and 280 mJ/m2, whereas DFT values for pure magnesium lie between 8 and 21 mJ/m2.  
Evidence: citation [9, 10, 11, 16, 17, 18, 19]  
→ motivates **GAP2**  

**GAP1** `GAP`  Sec. 1, para. 5  
The I1 stacking fault energy has been computed for only eight solutes in magnesium (Al, Dy, Gd, Li, Nd, Pr, Tb, Y).  
Evidence: citation [7, 8, 21]  
→ motivates **AIM1**  

**GAP2** `GAP`  Sec. 1, para. 5  
Earlier DFT calculations of the I1 fault used vacuum layers whose free surfaces may interact with the fault, and rarely tested convergence with supercell size.  
Evidence: none given  
→ motivates **AIM2**  
→ motivates **AIM3**  

**GAP3** `GAP`  Sec. 1 (implicit)  
Earlier calculations of solute effects on the I1 fault used a single solute concentration.  
Evidence: none given  
→ motivates **AIM4** *(annotator)*  

**AIM1** `AIM`  Sec. 1, para. 6  
The paper computes the I1 stacking fault energy of 52 binary Mg-X systems.  
Evidence: none given  

**AIM2** `AIM`  Sec. 1, para. 6  
The paper uses a periodic supercell with two fault interfaces, so that no vacuum layer and no free surface is needed.  
Evidence: none given  

**AIM3** `AIM`  Sec. 1, para. 6  
The paper tests the convergence of the stacking fault energy with supercell size.  
Evidence: none given  

**AIM4** `AIM`  Sec. 1, para. 6  
The paper computes each solute at two concentrations on the fault plane, 11 and 25 at.%.  
Evidence: none given  

**AIM5** `AIM`  Sec. 1, para. 6  
The paper explains the trends of the stacking fault energy with simple physical features of the solute atoms.  
Evidence: none given  

**AIM6** `AIM`  Sec. 1, para. 6  
The stacking fault energies form a first-principles database meant to guide the design of formable magnesium alloys.  
Evidence: none given  

## Methods and data

**METH1** `METHOD`  Sec. 2, para. 1  
Energies are computed with VASP using PAW potentials and the PBE functional, relaxing atoms with Methfessel-Paxton smearing until forces are below 0.01 eV/A and taking final energies with the tetrahedron method.  
Evidence: none given  
⚠ reproducibility (medium): The plane-wave cutoff energy is not reported.  
⚠ reproducibility (high): It is not stated whether calculations are spin-polarized, although Fe, Co, Ni, Mn and Cr are among the solutes.  
⚠ reproducibility (medium): The magnesium lattice constants used and whether cell shape or only atomic positions were relaxed are not given.  

**METH2** `METHOD`  Sec. 2, para. 2-3, Fig. 1, Eq. (1)  
The I1 fault is built by switching the stacking from AB to CB halfway along c in a periodic supercell, which then contains two fault interfaces, and the stacking fault energy is (E - E0) / 2A.  
Evidence: none given  
→ delivers **AIM2**  
→ delivers **AIM3**  

**METH3** `METHOD`  Sec. 2, para. 4, Fig. 2  
One magnesium atom in the faulted layer of a 2x2x10 or a 3x3x10 supercell is replaced by a solute, giving 25 or 11 at.% on the fault plane, which the paper states as 2.5 and 1.1 at.% overall.  
Evidence: data_quantitative (Sec. 2 and Sec. 5)  
Check: one solute in 80 atoms = 1.25 at.% (recomputed)  
Check: one solute in 180 atoms = 0.56 at.% (recomputed)  
Check: stated overall concentrations equal one solute per cell ✗ not satisfied (recomputed)  
→ delivers **AIM1**  
→ delivers **AIM4**  
⚠ arithmetic (medium): One solute in 80 or 180 atoms gives 1.25 and 0.56 at.%, not the stated 2.5 and 1.1 at.%.  

## Observations

**OBS1** `OBSERVATION`  Sec. 3.1, Table 1, Fig. 3  
The pure-magnesium stacking fault energy stops changing once the supercell has at least 10 unit cells along c, at 17.9-21.4 mJ/m2, within the published DFT range, and the 2x2x10 and 3x3x10 cells give 21.0 and 21.4 mJ/m2.  
Evidence: data_quantitative (Table 1, Fig. 3)  
Scope: n = 15; 15 supercells from 1x1 to 3x3 in-plane and 4-12 unit cells along c  
→ delivers **AIM2**  
→ supports **CLAIM1** [quantitative, strong]  
→ supports **CLAIM8** [quantitative, strong]  

**OBS2** `OBSERVATION`  Sec. 3.2, Table 2  
Eighteen of the 52 solutes raise the I1 stacking fault energy, cobalt most with 34.8 and 54.1 mJ/m2 at 11 and 25 at.%.  
Evidence: none given  
→ delivers **AIM1**  
→ supports **CLAIM2** [quantitative, intermediate]  
→ supports **CLAIM9** [quantitative, intermediate]  
⚠ internal inconsistency (low): Sec. 3.2 lists Ta among both the raising and the lowering solutes; Table 2 (21.7 and 24.6 mJ/m2) shows that it raises the SFE.  

**OBS3** `OBSERVATION`  Sec. 3.2, Table 2  
Most solutes lower the I1 stacking fault energy, including every rare earth; cesium lowers it most, to -33.3 mJ/m2 at 25 at.%, and nine solutes give a negative value.  
Evidence: none given  
→ supports **CLAIM2** [quantitative, intermediate]  
→ supports **CLAIM9** [quantitative, intermediate]  
⚠ untested assertion (low): The paper suggests the faulted structure may be stable for the nine negative-SFE solutes but does not test it.  

**OBS4** `OBSERVATION`  Sec. 3.2, Table 2  
Differences below about 1 mJ/m2 from pure magnesium, e.g. Mo 21.6 and Rh 21.3 against 21.0 mJ/m2, are counted as increases of the stacking fault energy.  
Evidence: none given  
→ qualifies **CLAIM2** *(annotator)*  
⚠ missing quantification (medium): No numerical uncertainty is given, although the pure-Mg value varies by more than 1 mJ/m2 across converged cells.  

**OBS5** `OBSERVATION`  Sec. 4.1, Fig. 4  
At 11 at.%, almost every solute that lowers the stacking fault energy has a lower first ionization energy than magnesium, but ten solutes (Ag, Cr, Li, Mn, Mo, Nb, Ni, Rh, Ru, V) have a lower ionization energy and still raise it.  
Evidence: none given  
→ supports **CLAIM3** [qualitative, intermediate]  
→ supports **CLAIM4** [qualitative, weak]  
→ supports **CLAIM10** [qualitative, intermediate]  

**OBS6** `OBSERVATION`  Sec. 4.1, Fig. 5  
Virtually every solute that raises the stacking fault energy is smaller than magnesium (160 pm), including all ten exceptions to the ionization-energy trend (124-152 pm).  
Evidence: none given  
→ supports **CLAIM3** [qualitative, intermediate]  
→ supports **CLAIM5** [qualitative, weak]  
→ supports **CLAIM10** [qualitative, intermediate]  

**OBS7** `OBSERVATION`  Sec. 4.1, Fig. 6  
Charge-density plots show cobalt gathering electrons and cesium pushing them away near the faulted plane.  
Evidence: none given  
Scope: n = 2; Co and Cs only  
→ supports **CLAIM4** [qualitative, weak]  

**OBS8** `OBSERVATION`  Sec. 2, para. 2  
After relaxation the interplanar distance in the fcc-like zone at the fault is 5.178 A, slightly larger than the 5.165 A of the perfect lattice.  
Evidence: none given  
→ supports **CLAIM5** [quantitative, weak]  

**OBS9** `OBSERVATION`  Sec. 4.2, Fig. 7  
For most solutes the change of the stacking fault energy grows from 11 to 25 at.% (Ga 19.0 to 3.3 mJ/m2), but for 23 solutes it moves back toward pure magnesium (Er 5.6 to 10.2 mJ/m2), including all rare earths except La, Ce, Pr, Nd and Yb.  
Evidence: none given  
→ delivers **AIM4**  
→ motivates **CLAIM6**  
→ supports **CLAIM11** [quantitative, strong]  

**OBS10** `OBSERVATION`  Sec. 4.2 (annotator)  
In the 2x2x10 cell each solute is about 6.4 A, two lattice spacings, from its own periodic image.  
Evidence: none given  
→ alternative explanation for **CLAIM6** *(annotator, background knowledge)*  

## Claims

**CLAIM1** `CLAIM` `methodological` `demonstrated` Sec. 3.1  
The two-fault supercell gives converged stacking fault energies that agree with published DFT values, and the two cells used for alloys give nearly the same pure-magnesium value.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM3**  
→ supports **CLAIM2** [logical, strong]  
**Verdict: ✓ YES**. A 15-cell convergence series and agreement with the literature range support it directly.  

**CLAIM2** `CLAIM` `main conclusion` `demonstrated` Sec. 3.2, Table 2  
Table 2 is a first-principles database of the I1 stacking fault energy for 52 solutes at two concentrations, which divides the solutes into raisers and lowerers.  
Evidence: none given  
Modality: descriptive  
→ delivers **AIM1**  
⚠ missing quantification (high): The introduction names eight solutes with earlier I1 values but the results never compare against them; this is the most direct test of the new setup.  
**Verdict: ◐ PARTIAL**. The values are computed and tabulated for all 52 solutes, but small differences carry no uncertainty and the setup is never compared with the eight earlier I1 values.  
Obligation (open, high): Compare the new values with the earlier I1 values for Al, Dy, Gd, Li, Nd, Pr, Tb and Y.  
&nbsp;&nbsp;&nbsp;needs: I1 SFE for the eight previously computed solutes [mJ/m2] via same supercell setup  
Obligation (open, medium): Give a numerical uncertainty and treat changes inside it as no effect.  

**CLAIM3** `CLAIM` `main conclusion` `demonstrated` Sec. 4.1, final paragraph  
Solutes with a low first ionization energy and a large atomic radius lower the I1 stacking fault energy of magnesium, and solutes with a high ionization energy and a small radius raise it.  
Evidence: none given  
Modality: correlational  
→ delivers **AIM5**  
→ supports **CLAIM7** [logical, weak]  
⚠ missing quantification (high): The rule is read from two scatter plots; no fit and no count of how many of the 52 solutes it predicts correctly is given.  
⚠ missing quantification (medium): The two factors are called competing but the paper does not say which dominates when they disagree.  
**Verdict: ◐ PARTIAL**. Both correlations are visible and the radius accounts for the ten ionization-energy exceptions, but the combined rule is never tested quantitatively.  

**CLAIM4** `CLAIM` `mechanistic interpretation` `proposed` Sec. 4.1, para. 5-6  
A solute with a high ionization energy forms a local potential well that gathers charge near the fault, so forming the fault needs more charge redistribution and the stacking fault energy rises.  
Evidence: none given  
Modality: causal  
⚠ causal overreach (medium): The mechanism rests on charge-density pictures for two solutes and no quantitative charge analysis.  
**Verdict: ◔ WEAK**. Shown by plots for the two extreme solutes only; no charge transfer is computed for the others.  

**CLAIM5** `CLAIM` `mechanistic interpretation` `proposed` Sec. 4.1, para. 7  
Large solutes lower the stacking fault energy because they expand the lattice locally, which favours the wider fcc-like zone at the fault.  
Evidence: none given  
Modality: causal  
**Verdict: ◔ WEAK**. Argued from a 0.013 A difference in interplanar distance and the size correlation; the local strain around solutes is not computed.  

**CLAIM6** `CLAIM` `mechanistic interpretation` `speculative` Sec. 4.2, final paragraph  
The reversal at 25 at.% arises because electrons tunnel between neighbouring solutes above about 20 at.%, which weakens the local potential wells and hills; the authors say this needs further verification.  
Evidence: citation [33]  
Modality: causal  
→ supports **CLAIM12** [logical, weak]  
**Verdict: ? INCONCLUSIVE**. Proposed from a cited concept and not tested; direct solute-image interaction in the small cell is an untested alternative.  

**CLAIM7** `CLAIM` `intermediate` `proposed` Sec. 3.2, 4.2  
The SFE rule and the rare-earth trend give a screening rule for magnesium alloy design, and Yb and Bi additions or a rare-earth optimum are worth testing experimentally.  
Evidence: none given  
Modality: generalization  
→ delivers **AIM6**  
→ motivates **OUT1**  
**Verdict: ◔ WEAK**. Follows from the correlation, but the link from a lower I1 energy to ductility rests on the cited studies and no alloy is tested.  

**CLAIM8** `CLAIM` `intermediate` `demonstrated` Sec. 5, sentences 1-3  
Convergence of the supercells was tested strictly and is satisfactory for the 2x2x10 cell.  
Evidence: none given  
Modality: descriptive  
→ restates **CLAIM1** *(annotator)*  
**Verdict: ✓ YES**. Restates the convergence result of Sec. 3.1.  

**CLAIM9** `CLAIM` `intermediate` `demonstrated` Sec. 5, sentences 4-5  
Cobalt and cesium bracket the range of stacking fault energies; eighteen solutes raise it and most, including every rare earth, lower it.  
Evidence: none given  
Modality: descriptive  
→ restates **CLAIM2** *(annotator)*  
**Verdict: ◐ PARTIAL**. Restates Table 2, here with Ta correctly among the raisers; small changes still carry no uncertainty.  

**CLAIM10** `CLAIM` `intermediate` `demonstrated` Sec. 5, sentence 6  
Solutes with lower ionization energy and larger radius decrease the stacking fault energy, and those with higher ionization energy and smaller radius increase it.  
Evidence: none given  
Modality: correlational  
→ restates **CLAIM3** *(annotator)*  
**Verdict: ◐ PARTIAL**. Same rule as in the discussion, with the same lack of a quantitative test.  

**CLAIM11** `CLAIM` `intermediate` `demonstrated` Sec. 5, sentences 7-9  
The effect of a solute usually grows with concentration, but most rare earths change the stacking fault energy non-monotonically.  
Evidence: none given  
Modality: descriptive  
→ restates **OBS9** *(annotator)*  
**Verdict: ✓ YES**. Restates the concentration results of Sec. 4.2 and Fig. 7.  

**CLAIM12** `CLAIM` `intermediate` `demonstrated` Sec. 5, final sentence  
The abnormal concentration dependence of the stacking fault energy is correlated with quantum tunnelling.  
Evidence: none given  
Modality: causal  
→ restates **CLAIM6** *(annotator)*  
⚠ overclaim (high): The discussion calls the tunnelling explanation preliminary; the conclusion states it without that caveat.  
**Verdict: ? INCONCLUSIVE**. Restates an untested explanation with more certainty than the discussion gives it.  

## Limitations (stated by authors)

**LIM1** `LIMITATION`  Sec. 4.2  
The tunnelling explanation of the concentration reversal is preliminary and needs further verification.  
Evidence: none given  
Kind: interpretation  
→ qualifies **CLAIM6**  

## Outlook

**OUT1** `OUTLOOK`  Sec. 4.2  
Yb and Bi may raise the stacking-fault density, and rare-earth content should be optimised rather than maximised.  
Evidence: none given  
