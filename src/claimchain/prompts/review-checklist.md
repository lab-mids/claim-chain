# Review checklist for claim-chain annotation

Use the general checks for every paper, then the section for its type. Each item gives the `concern_type` to record when it fires. The examples come from the ten test papers in `test_papers/` and show what a hit looks like.

## General checks (every paper)

**Internal consistency**
- [ ] Plug fitted or reported parameters into the paper's own equations. *Dielectrics paper: W_m = 18-29 meV ≈ kT, so the paper's CBH formula s = 1 - 6kT/W_m gives negative s, while measured s is 0-1.* → `INTERNAL_INCONSISTENCY`; add a CONTRADICTS relation into the claim.
- [ ] Check tabulated values for physical sense: epsilon_inf > epsilon_s, activation energies of several eV for a process whose rate changes 10x over 40 K, an RMSE in "bar", a probe that is smaller than the cascade it should resolve.
- [ ] Compare counts and settings between abstract, text, figures and methods: 76 vs 78 samples, 1-inch vs 4-inch wafer, training-set sizes, software versions, analysis dose, "tensile" vs "compressive". → `INTERNAL_INCONSISTENCY`
- [ ] Check equation and reference numbering (wrong cross-references, empty or duplicate references). → `REPRODUCIBILITY` or `INTERNAL_INCONSISTENCY`
- [ ] Derived quantity vs its input: if P ∝ eps_r and eps_r rises monotonically, a P optimum at an intermediate composition is impossible. → claim gets `"NO"`.

**Claim strength**
- [ ] Abstract/highlights vs results: "we demonstrate", "confirm", "predictive", "optimal", "reproduces the grain size distribution" (not shown), "dopant-free" (only checked before processing). → `OVERCLAIM`
- [ ] Does the paper's own limitation or discussion undercut the headline? *Annealing paper: the text states the martensitic transformation is faster than the quench, which undercuts "kinetic stabilization" in the abstract.* Record it as UNDERCUTS/CONTRADICTS with `asserted_by: AUTHORS`.
- [ ] Generalizations ("material-independent", "any EBSD dataset", "other MXenes", "heterophase interfaces") from 1-3 cases. → `OVERGENERALIZATION`, verdict usually INCONCLUSIVE.
- [ ] A precondition the authors state themselves but never test ("provided one can prove the ranking is invariant…"). → ASSUMPTION with `UNTESTED_ASSERTION`.

**Causation**
- [ ] Mechanism inferred from a trend, from visual similarity, or from a calculation that only shows consistency. → `CAUSAL_OVERREACH`, `claim_modality: CAUSAL`.
- [ ] Identify the obvious alternative cause and look for the control that excludes it: pulsed current vs composition, nanosize vs quench rate, external N source vs internal impurity, pressed-pellet interfaces vs dopant. Missing control → ALTERNATIVE_EXPLANATION_FOR relation + `missing_evidence`.
- [ ] Two variables changed together (energy and sample thickness; Y content and Te content; metric and segmentation). → `CONFOUNDED_COMPARISON`
- [ ] Explanations invoked side by side that contradict each other ("sluggish diffusion" vs "fast partitioning" at the same temperature). → `UNACKNOWLEDGED_CONFLICT`

**Evidence quantity**
- [ ] n per condition, repeats, error bars, number of micrographs or fields of view. Record `scope.sample_count`. → `MISSING_QUANTIFICATION`
- [ ] Differences ranked or claimed without an uncertainty (SAW drops of 0.39-0.47 % ranked with no noise level).
- [ ] Agreement metrics without a baseline (C2 RMS 0.098: what would a random microstructure give?). → `MISSING_QUANTIFICATION`
- [ ] Validation that cannot fail (disagreement re-read as "higher sensitivity"; a hypothesized feature defined as undetectable). → `UNFALSIFIABLE_VALIDATION`
- [ ] Data shown in the paper that contradict a claim but are not discussed (the {100}/{110} GB gets stronger with SGMDs). → `UNADDRESSED_COUNTEREVIDENCE`
- [ ] Ad hoc constants, weights or selection limits (equal-weight sums called "objective", halved eigenstrains, spline order at the edge of the tested range). → `AD_HOC_PARAMETER`

## Experimental papers

- [ ] Is the phase/structure actually identified? Single diffraction peak, no Raman, amorphous state never checked by XRD/DSC.
- [ ] Are properties measured after processing or only before (stoichiometry, grain size, phase fraction)?
- [ ] Sample form vs claim: pressed powder pellets (interfaces), thin films vs bulk, one flake per condition.
- [ ] The application claimed (PCM, thermal management, RF antennas) vs the properties actually measured.
- [ ] Probe-induced artifacts: beam damage, contamination, heating, preferential sputtering in XPS, EDS interaction volume.
- [ ] Is the reference used for comparison obtained under the same conditions?

## Computational papers (DFT, MD, phase field, CALPHAD)

- [ ] Stability: phonons only for the pristine host? A short AIMD run as the only check for the doped or loaded structure? Positive formation energy waved through by analogy?
- [ ] Method adequacy: DFT+U / spin polarization for 3d dopants; one interatomic potential validated on one motif; a database not built for the system.
- [ ] Selection criteria that inflate results: averaged multilayer adsorption energy vs bulk cohesive energy (instead of differential); a dopant chosen by binding strength alone.
- [ ] Kinetics: barriers measured from the initial state, ignoring deep traps; energy span not given.
- [ ] Structure search: a single 0 K relaxation taken as the ground state. If the paper finds one metastable artefact, ask whether the other structures were checked.
- [ ] "Inputs only from first principles" while some parameters are chosen (eigenstrains, nucleus size, interface concentrations).
- [ ] Sensitivity analysis on intermediate quantities only (nucleation rate), not on the predicted outcome (microstructure), or over ranges narrower than the input uncertainty.
- [ ] Validation against one experimental image or one literature value; consequences (kinetics, cracking) argued without being computed.
- [ ] Comparison tables mixing functionals, criteria and capacity definitions from different papers.

## High-throughput / screening papers

- [ ] Proxy validity: is the fast measurement calibrated against the property of interest in this material class?
- [ ] Repeatability of the proxy and its noise compared with the spread across samples.
- [ ] Film-to-bulk transfer or ranking invariance: assumed or tested?
- [ ] Ranking: are weights and normalization stated, and does the winner win on the property in the headline?
- [ ] Speed-up claims: is the baseline measured, and does it deliver the same information?

## Method / software papers

- [ ] Benchmarked against an established code on many cases, plus at least one measured dataset?
- [ ] Speed claims qualified by workload and hardware (GPU slower for small cases?).
- [ ] Held-out validation (omitted patterns, cycles, reflections, temperatures) rather than in-sample fit only.
- [ ] Does the paper separate stability/variance reduction from accuracy (smoothness imposed by a model ≠ smaller uncertainty)?
- [ ] A careful paper with all of the above deserves `"YES"` verdicts; do not invent concerns.

## Agentic AI / LLM-workflow papers

- [ ] Baseline: is the agentic workflow compared with a scripted or manual workflow (time, errors, effort)?
- [ ] Attribution: which decisions did agents make vs researchers? Researcher-initiated steps credited to "dynamic replanning"?
- [ ] Failures visible in the paper (screening missed candidates the researcher added).
- [ ] Reproducibility: proprietary model versions, regenerated code, repeat runs.
- [ ] Separate the physics claims (assess like a computational paper) from the claims about the AI framework (usually INCONCLUSIVE without a baseline).

## Questions per part (Sepideh's question spine)

Ask these of every paper, part by part. An unanswered question is where the argument is weakest; "not reported" items become REPRODUCIBILITY concerns.

- **Introduction:** Why does the field matter? What is the specific problem? What controls it? Why believe it matters in this system? How can it be studied, and why this method? What is still missing (coverage and method gaps)? What does the paper do, one aim per gap? Why does it matter (payoff)?
- **Methods:** Which theory, code and settings? How is the system or sample built? How is the quantity computed or measured? Which equation defines the result? Is it converged and validated on a known case? How is the variable of interest controlled? Could a reader reproduce it from the text alone?
- **Results:** Does the method reproduce known values, including earlier values the introduction names? What is the main split or trend? What are the extremes, with numbers? How does the result depend on the controlled variable? Which aims do the results deliver?
- **Discussion:** Which results need explaining? What hypothesis could explain them? Does it fit the data, and which cases break it? What mechanism links cause and effect, and for how many cases is it shown? What alternative explanations exist?
- **Conclusions:** Is every aim delivered and restated? Does any claim grow more certain than in the discussion? Are limitations and next steps stated? Does the end return to the opening problem?
