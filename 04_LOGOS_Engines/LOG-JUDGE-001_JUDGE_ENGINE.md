---
doc_id: LOG-JUDGE-001
title: LOGOS Judge Engine (Design Jury) v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
engine_blueprint: CTO Decision #003
last_reviewed: 2026-07-17
related:
  - LOG-CREATE-001 Create Engine (upstream — provides Concept Families)
  - LOG-CC-001 Creative Council (the 9 minds — evaluation engine)
  - All Philosophy Series LICs (evaluation dimensions)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-JUDGE-001 — Judge Engine (Design Jury)

> *The Judge Engine is LogoMind's quality gate. It evaluates every Concept Family across ten dimensions, explains its scoring with reasoning, and refuses to pass concepts that don't meet the bar. It is the engine that protects against "good enough."*

---

## 1. Mission

Evaluate Concept Families (and, later, sketch concepts) across the ten Philosophy dimensions, produce a defensible score for each, explain the reasoning, and recommend which concepts survive scrutiny and which require refinement or rejection.

The Judge Engine does not improve concepts — that is the designer's job. It *evaluates* them, providing the rigorous second opinion that prevents weak work from proceeding.

---

## 2. Purpose in the Pipeline

```
LOGOS Create  →  LOGOS Judge  →  Strategic Sketch Brief (SSB)
(Concept         (evaluation)     (final creative report
 Families)                        to the designer)
                    ▲
                    │
              THE JUDGE ENGINE
              evaluates each family
              across 10 dimensions
              only survivors reach
              the SSB
```

The Judge Engine sits between Create and the SSB output, ensuring that only concepts that pass rigorous evaluation reach the designer's report.

---

## 3. The Two Evaluation Components

The Judge Engine combines two distinct evaluation systems:

### Component A: The Creative Council (LOG-CC-001)
The nine thinking models — each asks its driving question of the concept:
1. Meaning & Semiotics — What does this communicate?
2. Simplicity & Clarity — Can this be reduced?
3. Differentiation — Will this stand apart?
4. Context & Application — Will this work where it must live?
5. Memorability — Will it be recalled?
6. Identity Systems — Does this hold as a system?
7. Emotional Resonance — What will people feel?
8. Longevity — Will this last?
9. Strategic Boldness — Is this appropriately courageous?

### Component B: The Design Jury Scoring
Ten-dimension quantitative scoring, each dimension grounded in a Philosophy LIC:

| Dimension | Source LIC | Question |
|-----------|-----------|----------|
| Meaning | RS-LIC-PH-001 | Does it express the brand's meaning? |
| Simplicity | RS-LIC-PH-003 | Has it been reduced appropriately? |
| Clarity | RS-LIC-PH-004 | Is it clear to a cold viewer? |
| Originality | RS-LIC-PH-005 | Is it combinatorial and distinctive? |
| Memorability | RS-LIC-PH-006 | Will it be recalled after encounter? |
| Authenticity | RS-LIC-PH-007 | Is it authentic to the brand? |
| Timelessness | RS-LIC-PH-008 | Will it age well? |
| Relevance | RS-LIC-PH-009 | Is it relevant to the audience/category? |
| Consistency | RS-LIC-PH-010 | Will it cohere across touchpoints? |
| Brand Fit | RS-LIC-BS-001 | Does it serve the positioning? |

Together: the Council provides *qualitative judgment*; the Jury provides *quantitative scoring*. Both are required.

---

## 4. Inputs

### Required Data
- Concept Families (from Create Engine) — full structures with reasoning trails
- Brand DNA (from Strategy Engine) — the strategic foundation concepts are evaluated against
- Insight Report (from Insight Engine) — competitive context, clichés, trend appropriateness

### Knowledge Sources
- **All 10 Philosophy Series LICs** — provide the evaluation dimensions and their operational tests
- **RS-LIC-BS-001 Brand Positioning** — provides the Brand Fit dimension
- **Creative Council (LOG-CC-001)** — the nine-mind qualitative evaluation

---

## 5. Reasoning Steps

```
Step 1: PREPARE EVALUATION CONTEXT
   → Load Brand DNA — this is what concepts are evaluated AGAINST
   → Load Insight Report — competitive context for differentiation scoring
   → Confirm evaluation dimensions (10) and their tests

Step 2: RUN THE CREATIVE COUNCIL (qualitative)
   → For each Concept Family, run all 9 minds:
     Each mind asks its driving question and provides:
     ├── Assessment (1-2 paragraphs of qualitative judgment)
     ├── Concerns (what worries this mind?)
     └── Strengths (what does this mind endorse?)
   → Synthesise the 9 assessments into a Council Verdict

Step 3: RUN THE DESIGN JURY SCORING (quantitative)
   → For each Concept Family, score all 10 dimensions (0-10):
     For each dimension:
     ├── Apply the LIC's operational tests (e.g., Reduction Sequence
     │   for Simplicity, Clarity Audit for Clarity, Originality Tests
     │   for Originality)
     ├── Score based on test outcomes
     └── Write justification (WHY this score, citing the tests)
   → Calculate weighted total

Step 4: DIMENSION-BY-DIMENSION REASONING
   → For any dimension scoring < 7, provide:
     ├── Specific weakness identified
     ├── How it could be improved
     └── Whether improvement is feasible within this family
   → For any dimension scoring 9+, note what specifically earns the high score

Step 5: CALCULATE COMPOSITE SCORE
   → Weighting (reflecting strategic priority):
     Brand Fit:        15%  (highest — without fit, nothing else matters)
     Meaning:          12%
     Clarity:          10%
     Memorability:     10%
     Authenticity:     10%
     Originality:       8%
     Simplicity:        8%
     Timelessness:      8%
     Relevance:         8%
     Consistency:       8%  (evaluated once system is developed)
   → Composite = weighted average

Step 6: CLASSIFY OUTCOME
   → Based on composite score and minimum dimension scores:
     ├── 8.5+ composite, no dimension < 7 → RECOMMENDED (pass to SSB)
     ├── 7.0-8.4 composite, no dimension < 6 → DEVELOP WITH REFINEMENT
     ├── < 7.0 composite OR any dimension < 6 → REJECT OR RECONCEIVE
     └── Borderline cases → human designer judgment required

Step 7: COMPARE FAMILIES
   → Rank surviving families
   → Identify the strongest 1-3 for prominent SSB inclusion
   → Note: the designer always makes the final choice

Step 8: PREPARE JUDGE REPORT
   → Package all evaluations for the SSB Composer:
     ├── Per-family: Council Verdict + Jury Scores + reasoning
     ├── Ranking
     ├── Refinement recommendations for borderline families
     └── Honest flags where the engine is uncertain
```

---

## 6. Decision Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **DR-1** | Any dimension scores < 5 | Auto-reject regardless of composite — a critical failure |
| **DR-2** | Brand Fit scores < 7 | Reject — without fit, the concept doesn't serve the strategy |
| **DR-3** | Originality scores < 6 AND Insight flags as cliché | Reject — concept is undifferentiated |
| **DR-4** | Council unanimous concern across multiple minds | Flag prominently; recommend rejection even if scores pass |
| **DR-5** | Composite 7.0-8.4 with clear refinement path | Mark DEVELOP WITH REFINEMENT; specify what to improve |
| **DR-6** | Engine uncertainty high (low-confidence evaluation) | Flag honestly; recommend human judgment |

---

## 7. Confidence Calculation

Each score carries a confidence level (per LM-STD-003):

| Confidence | Meaning |
|-----------|---------|
| 🟢 C5 | Strong evaluation — multiple tests pass/fail clearly |
| 🔵 C4 | Generally reliable — tests support the score with minor ambiguity |
| 🟠 C3 | Context-dependent — score depends on execution details not yet known |
| 🟣 C2 | Emerging — evaluation based on limited information |
| ⚪ C1 | Exploratory — engine is guessing; flag for human review |

Low-confidence scores are *never silently asserted*. The Judge Engine explicitly notes when it is uncertain — preserving intellectual honesty (FD-004).

---

## 8. Outputs

### Primary Output: Judge Report

```yaml
judge_report:
  project: <project name>

  family_A:
    creative_council_verdict:
      meaning_mind: <assessment, concerns, strengths>
      simplicity_mind: <...>
      differentiation_mind: <...>
      context_mind: <...>
      memorability_mind: <...>
      systems_mind: <...>
      emotion_mind: <...>
      longevity_mind: <...>
      boldness_mind: <...>
      synthesised_verdict: <overall Council judgment>

    jury_scores:
      meaning: { score: 8.5, confidence: C4, justification: "..." }
      simplicity: { score: 9.0, confidence: C5, justification: "..." }
      clarity: { score: 7.5, confidence: C3, justification: "..." }
      originality: { score: 8.0, confidence: C4, justification: "..." }
      memorability: { score: 7.0, confidence: C3, justification: "..." }
      authenticity: { score: 9.0, confidence: C4, justification: "..." }
      timelessness: { score: 8.5, confidence: C3, justification: "..." }
      relevance: { score: 8.0, confidence: C4, justification: "..." }
      consistency: { score: 7.5, confidence: C2, justification: "..." }
      brand_fit: { score: 9.5, confidence: C5, justification: "..." }
      composite: 8.3
      classification: DEVELOP WITH REFINEMENT
      refinement_recommendations:
        - "Strengthen memorability — current silhouette is not distinctive enough"
        - "Improve clarity at small scale — test at favicon size"

  family_B: { ... }

  ranking:
    recommended: [family_A, family_C]
    develop_with_refinement: [family_B]
    rejected: [family_D]

  honest_flags:
    - "Engine confidence low on family_C's timelessness — human review recommended"

metadata:
  source: <Concept Families + Brand DNA + Insight Report>
  timestamp: <ISO>
```

### Secondary Outputs
- **Refinement Recommendations** — specific improvements for borderline concepts
- **Rejection Reasons** — why rejected concepts failed (educational for future Create cycles)
- **Uncertainty Flags** — where the engine recommends human judgment

---

## 9. The "Concept DNA" Score

Every evaluated concept receives a structured fingerprint (the Creative Genome from LOGOS Architecture):

```yaml
concept_id: C-024
family: A
emotion: Trust
archetype: Sage
primary_symbol: Bridge
secondary_symbol: Horizon
shape_language: Circular Geometry
typography_personality: Modern Humanist
complexity: Low
originality: High
risk: Medium
timelessness: 9.4/10
strategic_confidence: 94%
jury_composite: 8.3
```

This enables objective comparison across concepts — the designer can compare fingerprints, not just descriptions.

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Reasoning Provided** | Does every score have explicit justification? | Yes — no scores without reasoning |
| **Tests Applied** | Were the operational tests from each LIC actually applied? | Yes — not just asserted scores |
| **Confidence Honest** | Are low-confidence evaluations flagged? | Yes — never silently asserted |
| **Council/Jury Agreement** | Do Council qualitative concerns align with Jury scores? | Yes — or disagreement is explained |
| **Brand Fit Priority** | Is Brand Fit weighted appropriately? | Yes — highest weight |
| **No Auto-Pass** | Has every concept actually been scrutinised? | Yes — no rubber-stamp approvals |

---

## 11. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Score Without Reasoning** | Numbers without justification | Reasoning Provided check; reject scores without reasoning |
| **Rubber Stamp** | All concepts pass without scrutiny | No Auto-Pass check; enforce rejection thresholds |
| **Council/Jury Conflict** | Council concerns ignored by Jury scores | Council/Jury Agreement check; reconcile or explain |
| **Confidence Inflation** | Low-confidence evaluations presented as certain | Confidence Honest check; flag all C1-C2 evaluations |
| **Brand Fit Ignored** | Concepts scored highly despite poor brand fit | Brand Fit Priority; highest weight; auto-reject if < 7 |
| **Skipping Tests** | Scores assigned without applying the operational tests | Tests Applied check; reasoning must cite the test |

---

## 12. Learning Opportunities

- **Scoring calibration** — how do engine scores correlate with real-world outcomes? (Validate and recalibrate)
- **Dimension interaction patterns** — which dimensions tend to correlate? Trade off?
- **Common failure patterns** — which weaknesses recur most across concepts?
- **Refinement effectiveness** — which refinement recommendations actually improve scores?

---

## 13. Future Versions

| Version | Enhancement |
|--------|-------------|
| v1.1 | Sketch evaluation — extend Judge to evaluate designer's actual sketches (uploaded) |
| v1.2 | Comparative jury — evaluate multiple concepts side-by-side with relative scoring |
| v1.3 | Historical calibration — compare scores against known successful/failed identities |
| v2.0 | Crowd validation — integrate real designer evaluations to calibrate scoring |

---

## Relationship to Other Engines

| Engine | Relationship |
|--------|-------------|
| **LOGOS Create** (upstream) | Provides the Concept Families to evaluate |
| **LOGOS Strategy** (parallel) | Provides Brand DNA — the standard concepts are evaluated against |
| **LOGOS Insight** (parallel) | Provides competitive context for differentiation scoring |
| **Creative Council** (LOG-CC-001) | Component A of the Judge Engine — the qualitative evaluation |
| **SSB Composer** (downstream) | Consumes the Judge Report — only survivors reach the SSB |

---

## The Intellectual Honesty Principle

The Judge Engine embodies LogoMind's commitment to intellectual honesty (FD-004):

- It never pretends certainty it doesn't have.
- It flags uncertainty explicitly.
- It explains its reasoning — every score is defensible.
- It recommends human judgment where the engine is uncertain.
- It refuses to pass concepts that don't meet the bar — protecting against "good enough."

A Judge Engine that rubber-stamps is worse than no Judge Engine — it provides false confidence. The discipline of honest evaluation is the entire value.
