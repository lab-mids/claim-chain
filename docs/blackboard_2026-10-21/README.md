# Blackboard discussion, OSI hackathon, 21 Oct 2026

Digitized from the 4 photos in this folder (`board_1.jpg` to `board_4.jpg`). Handwriting I couldn't read with confidence is marked **[?]**. The arrows on board 4 are my reading of the drawing; see the notes there.

---

## Board 1: Topic brainstorm and team (`board_1.jpg`)

Four topic columns:

| Extraction | Agentic | Hypothesis testing / Validation | Coding |
|---|---|---|---|
| from papers to computational workflows (reproduction) | | Figures in conversation → less text | Automation |
| | | Deep Wiki | Analysis |
| | | *towards:* Agentic Review System | |

**Issues** (under Extraction):
- No schema
- Missing information

**Team:** Sepideh, Keymir [?], Markus, Soroush, Jan, Akmal [?]

---

## Board 2 (lower) and board 3 (upper): Problem framing (`board_2.jpg`, `board_3.jpg`)

**Motivation:** Review is the limiting factor (bottleneck) of scientific discovery / validation / progress.
- Exponential growth in math, but not in MSE.
- LLMs accelerate research. **Bottleneck: review.**

**Problem:** There is no format for logical chains of arguments in a single paper, with uncertainty and correlation/causation.

**Target:** Develop a format for logical validation.

**Unit:** Paper: text, tables, figures, SI.

**Target / objective:** Are the statements/conclusions valid?
- *Valid* = does the presented data support the statements?
- Causation vs. correlation.
- Output: **YES / NO**

**Format** of logical chains of arguments, using "evidence".

**Side notes:**
- Retracted papers: *inconclusive* (as a test set? see below)
- Ontology (bracketed off to the side, i.e. parked)
- "Benchmark…" on the adjacent board (cut off in the photo)

---

## Board 4: Statement types, relations and outputs (`board_4.jpg`)

**Statement types (list in the middle):**
- Claim
- Reference / Background
- Limitation: inconsistency
- Observation
- Assumption: a general claim accepted in the community → open questions
- Gap
- Hypothesis

**Relations drawn as arrows (my interpretation):**
- **Yellow arrows** run from a shared arc into Claim, Reference/Background, Observation, Assumption and Hypothesis. This reads as "these types support or feed into one another".
- A bracket links **Gap → Hypothesis**: a gap motivates a hypothesis.
- A yellow arc on the right links **Reference/Background ↔ Limitation/inconsistency**: a limitation can be an inconsistency with the background literature.
- **"Qualitative support"** (white arrows, left) points to Reference/Background and Observation: support can be qualitative.
- **"Affected (qualitative) uncertainty" ⊛** (white arrow, left) points to Assumption. Uncertainty is attached to links, at least qualitatively.
- Two **⊛-marked arrows** on the right point back up toward the list from "general claim accepted in the community". The same ⊛ symbol as the uncertainty note suggests that community assumptions carry uncertainty and open questions.

**Headline:** **Logic score!** (boxed)

**Outputs (numbered):**
1. Logic
2. Limitations
3. Missing evidence

Input for these: **paper + LLM background knowledge**

---

## How this compared to the schema at the time (v0.1)

All rows marked as differences were folded into schema v0.2.

| Board | Schema v0.1 | Difference (now resolved in v0.2) |
|---|---|---|
| Claim, Observation, Assumption, Gap, Limitation, Reference/Background | CLAIM, OBSERVATION, ASSUMPTION, GAP, LIMITATION, BACKGROUND | match |
| Hypothesis | (THESIS, QUESTION) | **add HYPOTHESIS** or rename THESIS |
| Assumption = "general claim accepted in community" | ASSUMPTION = "premise taken without test" | definitions differ; may need both kinds |
| Limitation includes inconsistency | separate concern INTERNAL_INCONSISTENCY | decide where inconsistency lives |
| Qualitative support / uncertainty on links | evidence kind per statement; no uncertainty on relations | **add strength/uncertainty to Relation** |
| Correlation vs. causation | not modelled | **add claim modality** (correlational / causal) |
| Valid: YES / NO, logic score | concerns only, no score | **add a verdict + score** per claim and per paper |
| Outputs: logic, limitations, missing evidence | relations + LIMITATION + concerns | "missing evidence" fits the existing concerns (MISSING_QUANTIFICATION, UNTESTED_ASSERTION) |
| Ontology (parked) | removed | consistent |
