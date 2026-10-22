# SciLogic

**SciLogic reduces a research publication to its logical argument structure.**

A paper becomes a set of typed statements (background, assumptions, methods, observations, claims, limitations, outlook) and typed relations between them (supports, qualifies, undercuts, ...). Every claim gets a verdict: does the data presented in the paper support it? Where the paper gives numbers, the encoding records them and the checks can be recomputed.

The reference implementation is [claim-chain](https://github.com/lab-mids/claim-chain). It converts a PDF into an encoding with an LLM (`claimchain paper.pdf`) and renders the encoding into reports, argument maps and a logic score (`scripts/render.py`).

Read the [SciLogic paper (PDF)](scilogic_paper.pdf).

## Who this is for

- **Peer reviewers** who need to reconstruct and check the argument of a paper.
- **Researchers** looking for open questions in a field that match their expertise.
- **Teams writing proposals** from their own body of work.

## What the examples show

- [Getting started](00-getting-started.ipynb): load an encoding, inspect statements and relations, compute the logic score.
- [Peer review](01-peer-review.ipynb): the argument of Zhuang, Chen and Carter (2017), with its verdicts, recomputed checks and open proof obligations.
- [Research opportunities](02-research-opportunities.ipynb): collect the open items of ten recent arXiv preprints and trace five derived studies back to them.

All examples run on encodings stored in the repository, so the notebooks make no LLM calls and build reproducibly.
