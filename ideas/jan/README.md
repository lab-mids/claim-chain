# Ideas: Jan

*First version written from Markus's notes of the team discussion (21 Oct 2026). Jan, please correct and add details.*

## Approach: open proof obligations (reviewer's view)

Treat the paper like a case under investigation. Every claim creates **proof obligations**: what has to be shown for the claim to hold. Then gather the evidence the paper presents and check which obligations it discharges. Whatever stays open is what a reviewer would ask for.

## How it maps to the format

- Each claim's `assessment` can list `proof_obligations`. Each obligation has:
  - a text
  - a status: OPEN, PARTIALLY_DISCHARGED or DISCHARGED
  - the statement ids that discharge it (`discharged_by`)
- The report lists all open obligations. They are the most specific form of "missing evidence".

## What I tried

## Open questions

- Should a verdict be derived from obligations, e.g. all discharged = YES, some = PARTIAL, none = NO?
- Who generates the obligations? A fixed checklist per claim type, e.g. a causal claim requires a control or mechanism, or free-form from an LLM?
