# Ideas: Soroush

*First version written from Markus's notes of the team discussion (21 Oct 2026). Soroush, please correct and add details.*

## Approach: quantify the supporting evidence

Rate how strongly each piece of evidence supports the claim it is attached to: **strong**, **intermediate** or **weak**.

## How it maps to the format

- Each relation has a `support_strength` (STRONG, INTERMEDIATE, WEAK).
- It sits next to `support_basis` (qualitative, quantitative, logical) and `uncertainty` (low, medium, high) from the blackboard discussion.

## What I tried

## Open questions

- `support_strength` and `uncertainty` overlap. Keep both, merge them, or derive one from the other?
- What are the criteria for strong, intermediate and weak? For example, quantitative with statistics is strong, visual is intermediate, argument only is weak.
- How should strength propagate into the logic score? For example, a claim is only as strong as its strongest or weakest support.
