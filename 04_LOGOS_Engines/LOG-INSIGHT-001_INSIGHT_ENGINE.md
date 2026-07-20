---
doc_id: LOG-INSIGHT-001
title: LOGOS Insight Engine (Research + Trend Intelligence) v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
engine_blueprint: CTO Decision #003
last_reviewed: 2026-07-17
related:
  - LOG-STRAT-001 Strategy Engine (upstream)
  - LOG-CREATE-001 Create Engine (downstream — consumes cliché awareness)
  - RS-LIC-PH-008 Timelessness (knowledge source for trend classification)
  - RS-LIC-PH-009 Relevance (knowledge source for context-aware recommendations)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-INSIGHT-001 — Insight Engine (Research + Trend Intelligence)

> *The Insight Engine is LogoMind's eyes on the world. It knows the category, the competitors, the clichés, and the trends — and it applies that knowledge contextually, never universally. Its job is to make sure every creative direction is informed by reality, not assumption.*

---

## 1. Mission

Provide the Strategy and Create engines with **industry intelligence, competitor awareness, cliché detection, and context-aware trend recommendations** — so every strategic and creative decision is grounded in the actual category dynamics rather than assumption.

---

## 2. Purpose in the Pipeline

```
LOGOS Strategy  →  LOGOS Insight  →  LOGOS Create
(Brand DNA)         (category context)  (Concept Families)
                       ▲
                       │
              THE INSIGHT ENGINE
              knows the category:
              competitors, clichés,
              opportunities, trends
```

The Insight Engine sits between Strategy and Create, providing the contextual intelligence that prevents LogoMind from generating concepts in a vacuum. Without it, the Create Engine might propose symbols that are overused in the category, miss competitive visual language, or apply trends inappropriately.

---

## 3. The Core Principle: Context-Aware, Not Universal

> Trends are never universal advice. A law firm may need timelessness; a fintech startup might benefit from contemporary feel; a heritage brand may want to avoid trends entirely.

The Insight Engine never says "this trend is good." It says "this trend is [appropriate / inappropriate / context-dependent] for THIS brand, in THIS category, for THIS audience, given THIS positioning."

---

## 4. Inputs

### Required Data
- Brand DNA (from Strategy Engine) — especially positioning, audience, archetype
- Industry / category
- Geographic / cultural market

### Optional Data
- Competitor names (from Discovery)
- Existing visual references the client provided
- Historical context (rebrand vs. new brand)

### Knowledge Sources
- **RS-LIC-PH-008 Timelessness** — provides the Trend Taxonomy (Timeless / Emerging / Short-lived / Overused)
- **RS-LIC-PH-009 Relevance** — provides the Three-Axis Audit and Relevance Dial
- **LMKC Industry Intelligence** (future volume) — per-category symbol conventions, clichés, opportunities
- **LMKC Trend Intelligence** (future layer) — emerging directions, classification, context-applicability

---

## 5. Reasoning Steps

```
Step 1: INDUSTRY ANALYSIS
   → Identify the category's visual conventions (what does the
     category "look like"?)
   → Map common symbols, palettes, typographic conventions
   → Identify category clichés (overused, exhausted symbols)
   → Identify category opportunities (underused directions,
     white space)

Step 2: COMPETITOR MAPPING
   → For each identified competitor, capture:
     ├── Positioning (where they claim to sit)
     ├── Visual language (forms, palette, type)
     ├── Strengths and weaknesses of their identity
     └── Differentiation opportunities (where is the gap?)
   → Build a competitive visual map showing where the brand can
     differentiate visually

Step 3: CLICHÉ DETECTION
   → List symbols/elements that are overused in this category
   → For each cliché, note:
     ├── Why it became a cliché (what meaning it originally carried)
     ├── Whether it can be refreshed through combination or abstraction
     └── Alternative symbols carrying the same meaning
   → Output the Cliché Avoidance Report (consumed by Create Engine)

Step 4: OPPORTUNITY IDENTIFICATION
   → Where is the category's white space?
   → What meanings are underserved by existing competitors?
   → What audience concerns are not addressed by existing visual language?
   → What adjacent categories offer borrowable conventions?

Step 5: TREND INTELLIGENCE (context-aware)
   → Identify current trends relevant to the category
   → Classify each trend using the Trend Taxonomy (RS-LIC-PH-008 §4):
     ├── Timeless Principle (always consider)
     ├── Emerging Direction (consider if brand fit is high)
     ├── Short-lived Trend (use cautiously; flag as dating risk)
     └── Overused Trend (usually avoid)
   → Apply context: is this trend appropriate for THIS brand?
     ├── Heritage brand → mostly avoid trends; favour timelessness
     ├── Innovative brand → engage Emerging trends strategically
     ├── Challenger brand → may use trends to signal newness
     └── Established brand → selective engagement

Step 6: TREND vs. TIMELESS METER
   → For this specific project, recommend a balance:
     "Timeless ◄━━━━━━●━━━━━━► Trend-forward
                    Recommended Position"
   → Examples by brand type:
     ├── Government/institutional: 95% timeless / 5% contemporary
     ├── Luxury heritage: 90% timeless / 10% contemporary
     ├── Established tech: 70% timeless / 30% contemporary
     ├── Fashion startup: 40% timeless / 60% trend-aware
     └── Youth culture: 20% timeless / 80% trend-forward (but
         strategic, not reflexive)

Step 7: CULTURAL & REGIONAL CONSIDERATIONS
   → Identify symbol meanings in the target market(s)
   → Flag symbols with negative connotations in specific cultures
   → Identify symbols with positive, underexplored connotations
   → Adjust recommendations for international vs. regional brands

Step 8: SYNTHESISE INSIGHT REPORT
   → Combine all findings into a single Insight Report
   → Ensure every recommendation is context-aware (never universal)
   → Flag confidence levels — where is the engine guessing vs. knowing?
```

---

## 6. Decision Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **DR-1** | A competitor uses the exact symbol the Create Engine is considering | Flag for differentiation; recommend alternative or abstraction |
| **DR-2** | A symbol is identified as a category cliché | Add to Cliché Avoidance Report; do not include in Concept Families unless refreshed |
| **DR-3** | A symbol has negative cultural connotation in target market | Flag with high priority; recommend alternative |
| **DR-4** | A trend's classification depends on context | Apply the Trend Taxonomy contextually; never universal advice |
| **DR-5** | Insufficient category data | Flag confidence as low; recommend additional research or proceed with caveats |

---

## 7. Confidence Calculation

| Insight Element | Confidence Inputs |
|-----------------|-------------------|
| Category conventions | How well-documented is this category? |
| Competitor mapping | How many competitors were identified? How current? |
| Cliché detection | Cross-referenced across multiple sources? |
| Trend classification | Stable classification vs. emerging/judgment call? |
| Cultural considerations | Single-market vs. cross-cultural verification? |

Low-confidence insights are *flagged* — never silently asserted. The downstream engines know which insights are well-supported and which are provisional.

---

## 8. Outputs

### Primary Output: Insight Report

```yaml
insight_report:
  project: <project name>
  category: <industry>

  industry_analysis:
    visual_conventions: <what the category looks like>
    common_symbols: <with frequency/ubiquity notes>
    common_palettes: <with emotional associations>
    typographic_conventions: <serif/sans, weights, treatments>

  competitor_map:
    competitor_1:
      positioning: <where they claim to sit>
      visual_language: <forms, palette, type>
      strengths: <what works>
      weaknesses: <what doesn't>
      differentiation_opportunity: <where the gap is>
    competitor_2: { ... }

  cliche_avoidance:
    - symbol: <overused symbol>
      why_cliche: <why it's exhausted>
      original_meaning: <what it once carried>
      refresh_possible: <yes/no, via combination or abstraction>
      alternatives: <symbols carrying the same meaning>

  opportunities:
    white_space: <underused directions>
    underserved_meanings: <meanings competitors neglect>
    adjacent_category_borrowings: <potentially relevant conventions>

  trend_intelligence:
    current_relevant_trends:
      - trend: <name>
        classification: <Timeless / Emerging / Short-lived / Overused>
        context_assessment: <appropriate for this brand? why?>
    trend_vs_timeless_recommendation:
      timeless_percentage: <%>
      contemporary_percentage: <%>
      reasoning: <why this balance for this brand>

  cultural_considerations:
    flagged_symbols: <symbols with market-specific connotations>
    regional_adjustments: <if multi-market>

  confidence_summary:
    overall: <C-level>
    high_confidence: <elements>
    low_confidence: <elements needing verification>
```

### Secondary Outputs
- **Cliché Avoidance Report** (also consumed directly by Create Engine)
- **Competitive Visual Map** (visual representation of category positioning)
- **Trend Recommendation Brief** (for the SSB)

---

## 9. The Trend Intelligence Advisor (Sub-Engine)

A specialised component within the Insight Engine, focused exclusively on trend judgment:

### How It Thinks

Instead of saying: *"Glassmorphism is popular."*

It reasons:
```
Industry: FinTech
Brand Position: Innovative
Audience: 18-30
Trend: Glassmorphism (translucent layering)
Classification: Emerging (3-5 year horizon)
Context Assessment:
  - Brand fit: HIGH (innovative positioning aligns)
  - Audience fit: HIGH (younger, design-aware)
  - Longevity: MEDIUM (may date within a decade)
Recommendation: Consider, with awareness of dating risk. Pair
with timeless structural elements to hedge longevity concern.
```

Compare to:
```
Industry: Luxury Watches
Trend: Glassmorphism
Context Assessment:
  - Brand fit: LOW (luxury favours materiality, not translucence)
  - Audience fit: LOW (luxury audience favours heritage cues)
Recommendation: Avoid. Trend conflicts with brand position.
```

Same trend; opposite recommendations — because context differs.

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Context Test** | Is every trend recommendation context-aware? | Yes — never universal advice |
| **Cliché Coverage** | Have category clichés been identified? | Yes — Cliché Avoidance Report complete |
| **Competitor Currency** | Is competitor information current? | Within 12 months, or flagged |
| **Cultural Verification** | Have cultural considerations been checked for target markets? | Yes — especially for international brands |
| **Confidence Honesty** | Are low-confidence insights flagged? | Yes — never silently asserted |
| **Differentiation Mapping** | Has competitive visual white space been identified? | Yes — where can the brand differentiate? |

---

## 11. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Universal Trend Advice** | Trends recommended without context | Context Test; Trend Taxonomy applied per-brand |
| **Cliché Compliance** | Engine misses category clichés; Create Engine uses them | Cliché Detection step mandatory; cross-reference multiple sources |
| **Stale Competitor Data** | Competitor mapping is outdated | Currency check; flag if > 12 months old |
| **Cultural Blindness** | Engine ignores regional/cultural connotations | Cultural Considerations step; especially for international brands |
| **Confidence Inflation** | Engine asserts low-confidence insights as fact | Confidence Honesty check; flag all provisional findings |
| **Category Misidentification** | Engine analyses wrong category | Verify category against Brand DNA; confirm with Discovery output |

---

## 12. Learning Opportunities

- **Category cliché accumulation** — building a comprehensive cliché library across industries (feeds LMKC)
- **Trend classification accuracy** — how well do Timeless/Emerging/Short-lived classifications hold over time?
- **Cultural symbol maps** — comprehensive cross-cultural symbol meaning database
- **Differentiation pattern discovery** — which white spaces recur across categories?

---

## 13. Future Versions

| Version | Enhancement |
|--------|-------------|
| v1.1 | Real-time trend data integration (currently relies on LMKC + judgment) |
| v1.2 | Cultural adaptation engine — automatic cross-market verification |
| v1.3 | Competitor monitoring — track visual identity changes over time |
| v2.0 | Predictive trend classification — machine learning on trend ageing patterns |

---

## Relationship to Other Engines

| Engine | Relationship |
|--------|-------------|
| **LOGOS Strategy** (upstream) | Provides Brand DNA; Insight focuses research on the right positioning/audience |
| **LOGOS Create** (downstream) | Consumes Cliché Avoidance Report and Opportunities; avoids exhausted symbols |
| **LOGOS Judge** (parallel) | Insight context informs Judge's distinctiveness scoring |
| **LKG / LMKC** (knowledge) | Insight both consumes and contributes to category intelligence |

---

## The Future-Proof Check

A sub-routine of the Insight Engine, applied to every Concept Family before Judge evaluation:

- Will this logo still feel appropriate in 10 years?
- Is this concept tied too closely to today's aesthetics?
- Could a small modernisation be enough instead of a complete redesign?
- Is the identity flexible enough for digital, print, motion, and small-screen applications?

The goal: encourage longevity without ignoring modern expectations. Not anti-trend; context-aware.
