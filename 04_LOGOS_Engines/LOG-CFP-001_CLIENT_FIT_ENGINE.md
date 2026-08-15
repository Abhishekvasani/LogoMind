---
doc_id: LOG-CFP-001
title: LOGOS Client Fit — Client Preference Predictor v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
last_reviewed: 2026-08-14
related:
  - LOG-JUDGE-001 Judge Engine (upstream — evaluates design excellence; Client Fit deliberately diverges)
  - LOG-CREATE-001 Create Engine (upstream — provides Concept Families)
  - LOG-CBD-001 Contest Brief Decoder (upstream — provides decoded contest signals)
  - LOG-CP-001 Concept Prompt Engine (downstream — prompts steered by the persona)
  - RS-LIC-PSY-VOLUME Client Psychology (decision-maker types)
  - RS-LIC-CON-VOLUME Contest Dynamics (revealed-preference interpretation)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-CFP-001 — Client Fit (Client Preference Predictor)

> *The Judge scores design excellence. Client Fit answers a different question entirely: which direction will THIS client love? It builds a model of the specific decision-maker, predicts how strongly each Concept Family resonates with that persona, and ranks them — honestly, as an inference with a stated confidence, never as a measurement of the client's brain.*

---

## 1. Mission

Predict client appeal, not design quality. A family can score high with the jury and still be the wrong bet for a conservative decision-maker — and the predictor says so explicitly, with the reasoning visible.

## 2. Purpose in the Pipeline

Sits between Judge and Concept Prompt. Its persona is the steering signal for every downstream concept prompt (the rank-1 family gets extra emphasis), and its refine loop keeps the prediction current as the contest unfolds.

## 3. The Signature Principle: Preference Is Modelled, Not Measured

The HONESTY BOUND is structural: this is reasoning-based preference prediction via LLM persona-simulation. It is NOT a neural or brain-response measurement, and nothing may claim to be. Every prediction carries explicit confidence; the report's `caveat` states plainly how much signal the inputs provide.

## 4. Inputs

### Required Data
- Concept Families (from Create) — the candidates being ranked

### Optional Data (highest signal first)
- Contest feedback (revealed preferences: liked/disliked/comment + trait) — overrides brief inference
- Contest brief (decoded via LOG-CBD-001) — pre-committed taste
- Client brief, Discovery summary, Brand DNA, Insight report — context
- Judge report — for divergence-awareness, NOT as the ranking

### Knowledge Sources
- RS-LIC-CL-VOLUME (colour psychology — decoding "blue" → trust)
- RS-LIC-SY-VOLUME (symbol meanings — decoding "a shield" → security)
- RS-LIC-BS-005 (twelve-archetype vocabulary for the persona's `archetype`)
- RS-LIC-PSY-VOLUME (decision-maker types carry aesthetic-lean/boldness-tolerance priors — evidence overrides)
- RS-LIC-CON-VOLUME (rating/elimination/silence interpretation in the refine loop)

## 5. Reasoning Steps

1. **Build the persona** (`ClientPersona`): one-line characterisation, archetype, taste signals, decoded intents (stated → intent), aesthetic lean, boldness tolerance, must-haves/avoids.
2. **Score each family** for resonance with THAT persona (`FamilyAppeal`): client_appeal_score 0–100, rank, predicted response in the client's emotional vocabulary, appeal drivers (persona-relative), appeal risks.
3. **Recommend + explain**: rank-1 family, 2–3 sentence reasoning (why it is the safest bet to win), honest caveat, confidence.
4. **Refine (Stage 4 loop)**: append contest signals to the accumulated feedback; re-run with that feedback weighted highest. Signals compound — they are never overwritten.

## 6. Decision Rules

- **Divergence is information**: where the persona's taste contradicts the Judge's excellence scores, say so — that is the product.
- **Types are priors, never verdicts**: PSY decision-maker types inform the prior; the brief's own evidence always overrides (RS-LIC-PSY-VOLUME framework).
- **Aggregate before acting**: one contest signal is noise; three aligned signals are a direction (RS-LIC-CON-VOLUME).
- **Never regress**: re-running prediction never moves the project backwards past its current stage.

## 7. Confidence Calculation

Persona and per-family confidence follow LM-STD-003 (C1–C5), driven by input richness: contest feedback > decoded contest brief > detailed client brief > thin brief. The report-level `caveat` must state the bound honestly (e.g. "brief-only; refine with contest feedback").

## 8. Outputs

### Primary Output: AppealReport
- `persona: ClientPersona` — the modelled decision-maker
- `family_appeal: [FamilyAppeal]` — one per family, ranked by predicted appeal
- `recommended_family` + `reasoning` — the decision screen
- `caveat` + `confidence` — the honesty bound

### Secondary Outputs
- Persona persisted on the project (`client_persona`) and threaded into Concept Prompt steering
- Decision-log entries (recommendation + refinements)

## 9. What This Engine Is Not

- Not a Judge replacement — it deliberately diverges from design excellence
- Not a neuroscience claim — the honesty bound is non-negotiable
- Not a decision maker — the designer remains sovereign (FD-005)

## 10. Quality Checks

- Every family provided has exactly one appeal entry; ranks are deterministic from scores
- Drivers/risks are persona-relative (not generic design commentary)
- Persona fields populated from evidence, not stereotype defaults

## 11. Failure Cases

- Brief-only prediction on a thin brief → low confidence, honest caveat (by design)
- Contradictory contest signals → treat as an undecided holder, weight recency
- Persona drift across re-runs → normaliser repairs shape; rank consistency enforced

## 12. Learning Opportunities

Refine-loop signal → persona-trait correlations; which archetype types change their minds under contest feedback.

## 13. Future Versions

- Persona versioning across refinements (visible drift history)
- Per-signal weighting (downgrades vs eliminations)
- Multi-stakeholder personas (the Relayer's hidden decision-maker)

## Relationship to Other Engines

Judge (excellence) → **Client Fit (appeal)** → Concept Prompt (steered execution). Contest Brief Decoder feeds it; the SSB ultimately benefits from a client-aligned direction.

## The "Why?" Loop

Why this family? Because the modelled decision-maker — built from their brief, sharpened by their revealed preferences — maps onto its meaning and lean, and the reasoning is visible to check.
