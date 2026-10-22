# Data used by the notebooks

The notebooks do not keep their own copies of the encodings. They read them from the repository:

| Notebook | Encoding |
|---|---|
| `00-getting-started.ipynb` | built inline, plus `examples/zhang2013_mg_sfe/zhang2013_mg_sfe.yaml` |
| `01-peer-review.ipynb` | `examples/zhuang2017_d019_mgal/zhuang2017_d019_mgal_claimchain.yaml` |
| `02-research-opportunities.ipynb` | `test_papers/yaml/*.yaml` (ten arXiv preprints) |

## Why the encodings are cached

Encoding a paper is an LLM call that takes minutes and costs money. The encodings are therefore committed as YAML, and the book only reads them. Building the book needs no API key and no PDF.

## Regenerating an encoding

```bash
pip install -e .
export ANTHROPIC_API_KEY=...
claimchain paper.pdf -o paper.yaml
python scripts/render.py paper.yaml generated/
```

The PDFs are not in the repository (they are not ours to redistribute); `test_papers/fetch_papers.sh` downloads the ten test papers from arXiv.

## Sources

- Zhuang, Chen and Carter (2017): D0<sub>19</sub>-ordered Mg<sub>3</sub>Al, encoded by hand and converted to the current schema with LLM assistance.
- Ten preprints from the cond-mat.mtrl-sci new submissions of 21 October 2026 (`test_papers/references.bib`), encoded by an LLM (Claude) from the PDFs of their first versions.
