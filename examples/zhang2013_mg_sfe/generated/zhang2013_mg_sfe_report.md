# claim-chain report: First-principles study of stacking fault energies in Mg-based binary alloys

J. Zhang, Y. Dou, G. Liu, Z. Guo (2013), doi:10.1016/j.commatsci.2013.07.012. Generated; do not edit by hand.

## 1. Logic

**Overall: ◐ PARTIAL** · **Logic score: 0.55** · weighted: 0.54 · proof obligations discharged: 0.00 (of 2)  
Score method: mean over CLAIM and HYPOTHESIS statements of YES=1, PARTIAL=0.5, WEAK=0.375, INCONCLUSIVE=0.25, NO=0 (draft weighting). Weighted: as the logic score, but MAIN_CONCLUSION weighs 3, COUNTER_CLAIM 0 and every other claim or hypothesis 1 (draft weighting).  
Verdicts: 3 YES, 4 PARTIAL, 3 WEAK, 2 INCONCLUSIVE, 0 NO.

The computational core holds: the two-fault supercell converges, agrees with published values, and delivers I1 stacking fault energies for 52 solutes at two concentrations, which closes the coverage and method gaps named in the introduction. The ionization-energy and radius rule is a visible correlation but is never tested quantitatively, and the mechanisms rest on pictures for two solutes. The tunnelling explanation is called preliminary in the discussion and stated plainly in the conclusion. The no-vacuum design and the alloy-design payoff promised in the introduction are not restated at the end, and the conclusion states no limitations.

**Score from derived verdicts: 0.55**, 0 claim(s) where the derived verdict differs from the annotator's. Method: verdicts derived from the links: an incoming CONTRADICTS gives NO; otherwise the strongest support link decides (STRONG YES, INTERMEDIATE PARTIAL, WEAK WEAK, none INCONCLUSIVE); UNDERCUTS, QUALIFIES or an alternative explanation caps at PARTIAL; CONDITIONALLY_SUPPORTS counts as WEAK at most; an essential link caps the claim at its own strength and at the derived verdict of the claim it comes from. Links without a strength count as INTERMEDIATE. Claims without links keep the annotator's verdict.  

| Statement | Role | Modality | Authors say | Verdict | Derived | Rationale |
|---|---|---|---|---|---|---|
| **CLAIM1** The two-fault supercell gives converged stacking fault energies that agree with published DFT values, and the two cells used for alloys give nearly the same pure-magnesium value. | methodological | descriptive | demonstrated | ✓ YES | same | A 15-cell convergence series and agreement with the literature range support it directly. |
| **CLAIM2** Table 2 is a first-principles database of the I1 stacking fault energy for 52 solutes at two concentrations, which divides the solutes into raisers and lowerers. | main conclusion | descriptive | demonstrated | ◐ PARTIAL | same | The values are computed and tabulated for all 52 solutes, but small differences carry no uncertainty and the setup is never compared with the eight earlier I1 values. |
| **CLAIM3** Solutes with a low first ionization energy and a large atomic radius lower the I1 stacking fault energy of magnesium, and solutes with a high ionization energy and a small radius raise it. | main conclusion | correlational | demonstrated | ◐ PARTIAL | same | Both correlations are visible and the radius accounts for the ten ionization-energy exceptions, but the combined rule is never tested quantitatively. |
| **CLAIM4** A solute with a high ionization energy forms a local potential well that gathers charge near the fault, so forming the fault needs more charge redistribution and the stacking fault energy rises. | mechanistic interpretation | causal | proposed | ◔ WEAK | same | Shown by plots for the two extreme solutes only; no charge transfer is computed for the others. |
| **CLAIM5** Large solutes lower the stacking fault energy because they expand the lattice locally, which favours the wider fcc-like zone at the fault. | mechanistic interpretation | causal | proposed | ◔ WEAK | same | Argued from a 0.013 A difference in interplanar distance and the size correlation; the local strain around solutes is not computed. |
| **CLAIM6** The reversal at 25 at.% arises because electrons tunnel between neighbouring solutes above about 20 at.%, which weakens the local potential wells and hills; the authors say this needs further verification. | mechanistic interpretation | causal | speculative | ? INCONCLUSIVE | same | Proposed from a cited concept and not tested; direct solute-image interaction in the small cell is an untested alternative. |
| **CLAIM7** The SFE rule and the rare-earth trend give a screening rule for magnesium alloy design, and Yb and Bi additions or a rare-earth optimum are worth testing experimentally. | intermediate | generalization | proposed | ◔ WEAK | same | Follows from the correlation, but the link from a lower I1 energy to ductility rests on the cited studies and no alloy is tested. |
| **CLAIM8** Convergence of the supercells was tested strictly and is satisfactory for the 2x2x10 cell. | intermediate | descriptive | demonstrated | ✓ YES | same | Restates the convergence result of Sec. 3.1. |
| **CLAIM9** Cobalt and cesium bracket the range of stacking fault energies; eighteen solutes raise it and most, including every rare earth, lower it. | intermediate | descriptive | demonstrated | ◐ PARTIAL | same | Restates Table 2, here with Ta correctly among the raisers; small changes still carry no uncertainty. |
| **CLAIM10** Solutes with lower ionization energy and larger radius decrease the stacking fault energy, and those with higher ionization energy and smaller radius increase it. | intermediate | correlational | demonstrated | ◐ PARTIAL | same | Same rule as in the discussion, with the same lack of a quantitative test. |
| **CLAIM11** The effect of a solute usually grows with concentration, but most rare earths change the stacking fault energy non-monotonically. | intermediate | descriptive | demonstrated | ✓ YES | same | Restates the concentration results of Sec. 4.2 and Fig. 7. |
| **CLAIM12** The abnormal concentration dependence of the stacking fault energy is correlated with quantum tunnelling. | intermediate | causal | demonstrated | ? INCONCLUSIVE | same | Restates an untested explanation with more certainty than the discussion gives it. |

**Support links tested on the five criteria** (directness, sufficiency, controls, alternatives, scope match; ✓ met, ◐ partly, ✗ not met, – not applicable):

| Link | Criteria | Strength | Note |
|---|---|---|---|
| OBS1 → CLAIM1 (essential) | ✓✓✓–✓ | strong | 15 cells, benchmarked against published values. |
| OBS2 → CLAIM2 | ✓◐◐–✓ | intermediate | No uncertainty on small changes; no comparison with earlier I1 values. |
| OBS5 → CLAIM3 | ◐◐–✓✓ | intermediate | Free-atom ionization energy as a proxy; trend read by eye, ten exceptions. |
| OBS6 → CLAIM3 | ◐◐–✓✓ | intermediate | Free-atom radius as a proxy for local strain; no count of violations. |

**Golden thread** (each aim from the introduction to the end of the paper):

| Aim | Gap | Method | Result | Claim (verdict) | Outcome |
|---|---|---|---|---|---|
| **AIM1** The paper computes the I1 stacking fault energy of 52 binary Mg-X systems. | GAP1 | METH3 | OBS2 | CLAIM2 (◐) | DELIVERED |
| **AIM2** The paper uses a periodic supercell with two fault interfaces, so that no vacuum layer and no free surface is needed. | GAP2 | METH2 | OBS1 | - | NOT RESTATED |
| **AIM3** The paper tests the convergence of the stacking fault energy with supercell size. | GAP2 | METH2 | - | CLAIM1 (✓) | DELIVERED |
| **AIM4** The paper computes each solute at two concentrations on the fault plane, 11 and 25 at.%. | GAP3 | METH3 | OBS9 | - | DELIVERED |
| **AIM5** The paper explains the trends of the stacking fault energy with simple physical features of the solute atoms. | - | - | - | CLAIM3 (◐) | DELIVERED |
| **AIM6** The stacking fault energies form a first-principles database meant to guide the design of formable magnesium alloys. | - | - | - | CLAIM7 (◔) | NOT RESTATED |

Outcomes: DELIVERED, NOT RESTATED (delivered but absent from the conclusion and abstract), METHOD ONLY (carried out but no result shown), DROPPED (nothing delivers it).

**Certainty drift between restatements:**

- STRENGTHENED: **CLAIM6** (speculative, discussion) → **CLAIM12** (demonstrated, conclusion)

**Presented as demonstrated, but the verdict is weak, inconclusive or no:** CLAIM12 (INCONCLUSIVE).

**Recomputed checks:**

- **METH3** one solute in 80 atoms = 1.25 at.% (recomputed)
- **METH3** one solute in 180 atoms = 0.56 at.% (recomputed)
- **METH3** stated overall concentrations equal one solute per cell ✗ not satisfied (recomputed)

**Statements per paper part:**

| Part | Statements |
|---|---|
| introduction | BG1, BG2, BG3, BG4, BG5, GAP1, GAP2, GAP3, AIM1, AIM2, AIM3, AIM4, AIM5, AIM6 |
| methods | METH1, METH2, METH3, OBS8 |
| results | OBS1, CLAIM1, OBS2, OBS3, OBS4, CLAIM2 |
| discussion | OBS5, OBS6, OBS7, CLAIM3, CLAIM4, CLAIM5, OBS9, OBS10, CLAIM6, LIM1, CLAIM7, OUT1 |
| conclusion | CLAIM8, CLAIM9, CLAIM10, CLAIM11, CLAIM12 |

Causal claims (check against correlational evidence): CLAIM4, CLAIM5, CLAIM6, CLAIM12.

## 2. Limitations

- Small SFE changes carry no uncertainty and the setup is not compared with the eight earlier I1 values (CLAIM2, OBS4).
- The combined rule is a correlation without a count of correct predictions or a weighting of the two factors (CLAIM3).
- Mechanisms rest on two charge-density plots and a 0.013 A spacing difference (CLAIM4, CLAIM5).
- The tunnelling explanation is untested and gains certainty in the conclusion (CLAIM6, CLAIM12).
- Cutoff energy, spin treatment and lattice parameters are not reported, and the stated overall concentrations do not follow from the described cells (METH1, METH3).

**Stated by the authors:**

- **LIM1** (interpretation): The tunnelling explanation of the concentration reversal is preliminary and needs further verification.

**Assumptions the argument rests on:**


**Flagged by the annotator:**

- **METH1** reproducibility (medium): The plane-wave cutoff energy is not reported.
- **METH1** reproducibility (high): It is not stated whether calculations are spin-polarized, although Fe, Co, Ni, Mn and Cr are among the solutes.
- **METH1** reproducibility (medium): The magnesium lattice constants used and whether cell shape or only atomic positions were relaxed are not given.
- **METH3** arithmetic (medium): One solute in 80 or 180 atoms gives 1.25 and 0.56 at.%, not the stated 2.5 and 1.1 at.%.
- **OBS2** internal inconsistency (low): Sec. 3.2 lists Ta among both the raising and the lowering solutes; Table 2 (21.7 and 24.6 mJ/m2) shows that it raises the SFE.
- **OBS3** untested assertion (low): The paper suggests the faulted structure may be stable for the nine negative-SFE solutes but does not test it.
- **OBS4** missing quantification (medium): No numerical uncertainty is given, although the pure-Mg value varies by more than 1 mJ/m2 across converged cells.
- **CLAIM2** missing quantification (high): The introduction names eight solutes with earlier I1 values but the results never compare against them; this is the most direct test of the new setup.
- **CLAIM3** missing quantification (high): The rule is read from two scatter plots; no fit and no count of how many of the 52 solutes it predicts correctly is given.
- **CLAIM3** missing quantification (medium): The two factors are called competing but the paper does not say which dominates when they disagree.
- **CLAIM4** causal overreach (medium): The mechanism rests on charge-density pictures for two solutes and no quantitative charge analysis.
- **CLAIM12** overclaim (high): The discussion calls the tunnelling explanation preliminary; the conclusion states it without that caveat.

**Local checks per part** (issues found; failed derived checks count as arithmetic):

| Part | Completeness | Arithmetic | Consistency | Argument | High or critical |
|---|---|---|---|---|---|
| methods | 3 | 1 | 0 | 0 | 1 |
| results | 2 | 0 | 1 | 1 | 1 |
| discussion | 2 | 0 | 0 | 1 | 1 |
| conclusion | 0 | 0 | 0 | 1 | 1 |

## 3. Missing evidence

- Comparison with earlier I1 values for Al, Dy, Gd, Li, Nd, Pr, Tb and Y
- Count of solutes the ionization-energy and radius rule predicts correctly
- Charge transfer computed for every solute, not only Co and Cs
- Larger in-plane cells at 25 at.% to separate tunnelling from solute-image interaction

**Open proof obligations:**

- **CLAIM2** (open, high): Compare the new values with the earlier I1 values for Al, Dy, Gd, Li, Nd, Pr, Tb and Y. Needs: I1 SFE for the eight previously computed solutes [mJ/m2] via same supercell setup.
- **CLAIM2** (open, medium): Give a numerical uncertainty and treat changes inside it as no effect.

**Per statement:**

