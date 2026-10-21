# Ideas: Sepideh

*First version written from Markus's notes of the team discussion (21 Oct 2026). Sepideh, please correct and add details.*

## Approach: divide and conquer

Analyse the individual parts of a paper separately before assessing the whole-paper logic:

1. **Introduction first.** Extract the background, the gap and the hypothesis, so the hypothesis is set up properly before anything else is judged.
2. **Then each further part** (methods, results, discussion, conclusion, SI): extract its statements and check them locally.
3. **Then the whole paper:** link the parts and assess whether the conclusions follow from the hypothesis and the results.

## How it maps to the format

- Each statement has a `paper_part` (INTRODUCTION, THEORY, METHODS, RESULTS, DISCUSSION, CONCLUSION, SUPPLEMENTARY, ABSTRACT), so extraction can run part by part and be merged.
- `render.py` lists the statements per part in the report.

## What I tried

## Open questions

- Should each part get its own sub-score before the whole-paper score?
- How should the hypothesis extracted from the introduction be compared with what the conclusion actually claims (drift between promise and delivery)?
