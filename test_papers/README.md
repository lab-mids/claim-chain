# Test papers

Ten recent submissions from arXiv **cond-mat.mtrl-sci** (new-submissions listing of 21 Oct 2026). They were picked to cover the range of materials science papers claim-chain should handle: experimental, computational, method and AI-tool papers.

> **The PDFs are not in this repository.** Each user has to fetch them individually after cloning:
>
> ```bash
> cd test_papers && ./fetch_papers.sh
> ```
>
> This downloads the papers from arXiv into `pdf/` (gitignored, since arXiv licenses vary per paper) and the official BibTeX into `bib/`.

| # | arXiv | Title | Authors | Type | BibTeX key |
|---|---|---|---|---|---|
| 1 | [2610.26996](https://arxiv.org/abs/2610.26996) | Tailoring Dielectric Relaxation and Charge Transport in Amorphous Ge-Te-Se Phase-Change Materials through Yttrium Incorporation | Surbhi Agarwal et al. | experimental, phase-change materials | `agarwal2026tailoringdielectricrelaxationcharge` |
| 2 | [2610.27240](https://arxiv.org/abs/2610.27240) | Nanoscale chemical engineering of Ti3C2Tx MXene multilayers through in situ electron beam irradiation in a TEM | Ayoub Benmoumen et al. | experimental, in situ TEM, 2D materials | `benmoumen2026nanoscalechemicalengineeringti3c2tx` |
| 3 | [2610.27355](https://arxiv.org/abs/2610.27355) | Reaction-induced Localized Annealing for On-chip Materials Discovery | Nensi Toncich et al. | experimental, combinatorial thin films | `toncich2026reactioninducedlocalizedannealingonchip` |
| 4 | [2610.27460](https://arxiv.org/abs/2610.27460) | Nanocrystalline cubic boron arsenide growth on GaAs(100) by gas source molecular beam epitaxy | Matthew A. Delmont et al. | experimental, thin-film growth | `delmont2026nanocrystallinecubicboronarsenide` |
| 5 | [2610.27825](https://arxiv.org/abs/2610.27825) | Early-stage local melting during solid-state sintering of a Cu-Ni-Ti-Zr-Hf alloy: A combined thermodynamic and kinetic analysis | Andrea Skolakova et al. | experimental + thermodynamics, metallurgy | `skolakova2026earlystagelocalmeltingsolidstate` |
| 6 | [2610.28152](https://arxiv.org/abs/2610.28152) | Enhancement of Li and Na Storage in Janus HfSSe Monolayers by Co-Induced Electron-Deficient Chalcogen Sites: A First-Principles Study | Md. Muktadir Hasan et al. | computational (DFT), battery materials | `hasan2026enhancementlinastorage` |
| 7 | [2610.28232](https://arxiv.org/abs/2610.28232) | High-throughput Down-selection of Fusion Candidate Materials | Elena Botica-Artalejo et al. | high-throughput screening, nuclear materials | `boticaartalejo2026highthroughputdownselectionfusioncandidate` |
| 8 | [2610.28493](https://arxiv.org/abs/2610.28493) | Multiscale Modeling of Zr Corrosion: Predicting Microstructures of Oxide Films | K. Starkey et al. | computational, multiscale modelling, corrosion | `starkey2026multiscalemodelingzrcorrosion` |
| 9 | [2610.28564](https://arxiv.org/abs/2610.28564) | Differentiable powder X-ray diffraction enables analysis of evolving structures | Xiangyu Yin et al. | method, characterization + ML | `yin2026differentiablepowderxraydiffraction` |
| 10 | [2610.28629](https://arxiv.org/abs/2610.28629) | GBClaw: An agentic AI framework for atomistic grain boundary research and mechanistic discovery | Yazhuo Liu et al. | computational, agentic AI for atomistics | `liu2026gbclawagenticaiframework` |

## Files

- `arxiv_ids.txt`: the ten ids, one per line.
- `references.bib`: combined official arXiv BibTeX for all ten papers.
- `bib/`: one official arXiv BibTeX file per paper.
- `fetch_papers.sh`: downloads the PDFs to `pdf/` and the BibTeX to `bib/`, then rebuilds `references.bib`. Already-downloaded files are skipped.
- `pdf/`: the papers. PDFs are gitignored because arXiv licenses vary per paper; everyone runs `./fetch_papers.sh` locally.

## Selection criteria

- New submissions, not cross-lists or replacements.
- Clearly in materials science. Some border on physics or ML.
- A mix of paper types, because the logic differs:
  - experimental: 2610.26996, 27240, 27355, 27460, 27825
  - computational: 2610.28152, 28493
  - high-throughput screening: 2610.28232
  - characterization method: 2610.28564
  - agentic AI framework: 2610.28629
