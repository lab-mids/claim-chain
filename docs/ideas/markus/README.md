# Ideas: Markus

First manual and semi-formal analyses, made while shaping the approach. They use the example paper Wang et al. 2026, "Lattice genome", arXiv:2606.09611 (encoded in `examples/wang2026_lattice_genome/`).

## Approach

1. Read the paper and write down its argument as typed statements (background, gap, hypothesis, assumption, method, observation, claim, limitation, outlook).
2. Tag every statement with the kind of evidence the paper gives: citation, argument, data judged by eye, numbers, or none.
3. Link statements with typed relations: supports, undercuts, qualifies, alternative explanation, and others.
4. Mark where the evidence is weaker than the wording, and where the paper's own limitations undercut earlier claims.
5. Encode all of this in the schema and generate the readable views and the score from it.

## Files

| File | What it is |
|---|---|
| `logical_flow_Wang2026_lattice_genome.md` | First-pass critique: claims, argument chain, gaps and leaps. |
| `argument_chain_Wang2026_lattice_genome.md` | Hand-written human-readable argument chain with evidence per step, before the schema existed. |
| `argument_map_Wang2026.png` / `.svg` | Argument map rendered from the Mermaid in the chain file. |
| `slides/lattice_genome_logic.tex` | 11-slide Beamer deck on the logic, evidence and limitations of the example paper (metropolis theme). |

The slides use figures cropped from the paper. They are not in git (see `.gitignore`); place `fig2.png`, `fig5.png` and `fig6.png` in `slides/figs/` to compile.

## Open questions

- How should the logic score weigh central claims against peripheral ones?
- Should the critique (concerns, verdicts) live in a separate layer from the encoded paper?
