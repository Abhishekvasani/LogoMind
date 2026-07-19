---
doc_id: LOG-PIPE-001
title: LOGOS Pipeline & Remaining Engines
version: 1.0
status: Approved (summary) — Individual engines at varying draft levels
governance_level: L2 — Engine Specifications
last_reviewed: 2026-07-14
---

# LOGOS Pipeline — Engine Summary

> Full specifications exist for LOGOS Discover, the Creative Council, and LRL. The remaining engines are specified here at the architecture level and require full detailing before implementation.

---

## The Full Pipeline

```
Client Brief
     │
     ▼
┌─────────────────────────────────────┐
│  1. LOGOS Discover                  │  ← See LOG-DISC-001 (full spec)
│     Understand the client           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  2. LOGOS Strategy                  │  ← Brand DNA Engine
│     Create Brand DNA                │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  3. LOGOS Insight                   │  ← Research Engine
│     Industry, psychology, semiotics │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  4. LOGOS Create                    │  ← Creative Engine
│     Generate creative territories   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  5. LOGOS Judge                     │  ← Creative Council + Design Jury
│     Evaluate concepts               │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  6. Strategic Sketch Brief (SSB)    │  ← THE PRIMARY OUTPUT
│     The designer's creative report  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  7. LOGOS Coach                     │  ← Sketch Coach
│     Help designers sketch           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  8. LOGOS Present                   │  ← Presentation Builder
│     Build presentations             │
└─────────────────────────────────────┘
```

---

## Engine 2: LOGOS Strategy (Brand DNA Engine)

**Status:** Architecture defined; full spec pending.

| | |
|---|---|
| **Mission** | Create a complete Brand DNA profile from discovery output. |
| **Inputs** | Discovery Summary, Brand Confidence Score |
| **Outputs** | Brand DNA: Core Values, Personality, Archetype, Voice, Promise, Emotional Goal, Positioning, Differentiators |
| **Knowledge Sources** | LMKC — Brand Archetypes, Brand Psychology |

The **LogoMind Brand DNA Framework** has six strands: Purpose, Audience, Personality, Emotion, Differentiation, Promise.

---

## Engine 3: LOGOS Insight (Research Engine)

**Status:** Architecture defined; full spec pending.

| | |
|---|---|
| **Mission** | Apply branding knowledge to the specific project context. |
| **Inputs** | Brand DNA, Industry |
| **Outputs** | Industry Intelligence (common symbols, overused symbols, opportunities, visual expectations, trend recommendation) |

Includes the **Trend Intelligence Advisor** — classifies trends as Timeless / Emerging / Short-lived / Overused, with a **Trend vs. Timeless Meter** recommendation per project.

---

## Engine 4: LOGOS Create (Creative Engine)

**Status:** Architecture defined; full spec pending.

| | |
|---|---|
| **Mission** | Generate creative territories, not isolated ideas. |
| **Inputs** | Brand DNA, Industry Intelligence, Symbol Library |
| **Outputs** | Concept Families (strategic directions), each with symbols, metaphors, and visual language |

### Concept Families (Signature Feature)

Instead of flat lists of ideas, LOGOS generates **strategic territories**:

```
Family A — Trust:     Bridge, Anchor, Keystone, Pillar
Family B — Precision: Compass, Grid, Hexagon, Orbit
Family C — Growth:    Seed, Spiral, Tree Rings, Sunrise
```

The designer chooses a *direction*, not just an *idea*.

### Symbol Intelligence

For each symbol, LOGOS provides: meaning, why it fits, originality rating, abstraction level, risk level, possible combinations.

---

## Engine 5: LOGOS Judge (Creative Council + Design Jury)

**Status:** Creative Council fully specified (LOG-CC-001). Design Jury scoring framework defined.

**The Design Jury scores concepts across:**

| Dimension | Question |
|-----------|----------|
| Originality | Is it distinct from competitors? |
| Memorability | Will it be recalled after one glance? |
| Simplicity | Can it be reduced further? |
| Timelessness | Will it still work in 20 years? |
| Scalability | Does it work at 16px and on a billboard? |
| Brand Fit | Does it serve the brand strategy? |
| Production Readiness | Does it work in monochrome, embroidery, reverse? |
| Storytelling | Does it communicate a narrative? |

Only concepts that pass the Creative Council's nine minds and score above threshold proceed to the SSB.

---

## The Flagship Output: Strategic Sketch Brief (SSB)

**Status:** Full structure defined (CTO Decision #012; FD-014).

> LogoMind's primary output is **not a logo concept.** It is a **Strategic Sketch Brief** — a complete creative strategy that gives the designer everything needed to sketch confidently.

### SSB Structure (7 Sections)

1. **Project Essence** — one-paragraph synthesis.
2. **Brand DNA Snapshot** — the six strands.
3. **Creative North Star** — the single sentence the logo must embody.
4. **Creative Territories** — 3–5 strategic directions, each with symbols and rationale.
5. **Opportunities & Warnings** — what to explore; what to avoid (clichés).
6. **Creative Council Advice** — the nine minds' guidance, in a table.
7. **Sketch Mission** — 5–10 specific sketch directions, each with: core idea, why it works, potential pitfalls.

---

## Engine 7: LOGOS Coach (Sketch Coach)

**Status:** Concept defined; full spec pending.

Guides the designer's sketching — not by drawing for them, but by suggesting *where to start, what geometric relationships to test, where to introduce negative space, what proportions to explore, what to avoid.*

> "Begin with a circle-based grid. Explore three variations where the negative space forms the initial 'A'. Keep line weights consistent and test the icon in monochrome before introducing color."

---

## Engine 8: LOGOS Present (Presentation Builder)

**Status:** Concept defined; full spec pending.

Assembles the client presentation from project data: story, symbolism, typography rationale, colour rationale, construction logic, scalability notes, future-proofing, trend relevance.

> **Clients buy the reasoning as much as the design.**

---

## Parked / Future Engines

- **Reflection Engine** — captures designer learnings from real projects; feeds LMKC (with human approval).
- **Inspiration Engine** — analyses uploaded logos for *why* they appeal (without copying).
- **Design Mentor** — conversational mentor that asks questions instead of giving answers.
- **Creative Memory** — *rejected* in favour of project-specific memory + knowledge base (FD: "Remember knowledge, not preferences").
