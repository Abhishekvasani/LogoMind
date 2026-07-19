---
doc_id: LOG-CC-001
title: The Creative Council — Nine Thinking Models
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
last_reviewed: 2026-07-14
---

# The Creative Council (LOGOS Thinking Engine)

> LOGOS does not reason as a single mind. It reasons as a **council of nine specialised thinking models** — each asking a distinct question. Together, they simulate the deliberation of an experienced creative team.

---

## Purpose

A senior creative director doesn't think in one mode. They shift between meaning, simplicity, differentiation, context, memory, and more — often within seconds. The Creative Council makes this explicit and auditable.

---

## The Nine Minds

| # | Mind | Driving Question |
|---|------|------------------|
| 1 | **Meaning & Semiotics** | What does this actually communicate? |
| 2 | **Simplicity & Clarity** | Can this be reduced without losing meaning? |
| 3 | **Differentiation** | Will this stand apart, or blend in? |
| 4 | **Context & Application** | Will this work where it must live? |
| 5 | **Memorability** | Will someone recall this after one glance? |
| 6 | **Identity Systems** | Does this hold together as a system? |
| 7 | **Emotional Resonance** | What will people feel? |
| 8 | **Longevity** | Will this still be right in 10 years? |
| 9 | **Strategic Boldness** | Is this appropriately courageous? |

---

## How the Council Works

For any concept or recommendation, each mind independently evaluates and contributes its perspective. The outputs are then synthesised into a single, reasoned recommendation.

```
Concept or Brief
       │
       ▼
┌──────────────────────────────────────┐
│            Creative Council          │
│                                      │
│  Meaning → Simplicity → Diff →       │
│  Context → Memory → Systems →        │
│  Emotion → Longevity → Boldness      │
│                                      │
│         (each asks its question)      │
└──────────────────────────────────────┘
       │
       ▼
Synthesised Recommendation
(with reasoning from each mind)
```

---

## Design Review Flow Example

A designer proposes: *"Combine a compass with the letter N."*

| Mind | Contribution |
|------|-------------|
| **Meaning** | Compass = guidance/direction. Aligned with navigation brands. |
| **Simplicity** | Two elements is manageable; watch for forced integration. |
| **Differentiation** | Compass is moderately used; the N-integration may distinguish it. |
| **Context** | Must work at favicon size — test legibility of the N. |
| **Memorability** | Depends on execution; the fusion is the memorable moment. |
| **Systems** | Does this extend to sub-brands or lock to one mark? |
| **Emotion** | Direction = confidence. Good for advisory/consulting. |
| **Longevity** | Compass is timeless geometry. Strong. |
| **Boldness** | Moderate — familiar elements, depends on fusion quality. |

**Synthesis:** The concept is strategically sound but execution-dependent. The fusion of N + compass is the differentiator; if forced, it fails. Test at 16px before proceeding.

---

## Why Nine (Not More, Not Fewer)

- **Fewer than nine** misses a critical professional perspective.
- **More than nine** dilutes focus and creates noise.

The number is frozen (CTO Decision #013: *Perfect the core before expanding*). New minds are added only after repeated production evidence justifies it.

---

## Relationship to Other Engines

- The Creative Council is the **thinking core** of LOGOS.
- It is consulted by **LOGOS Judge** (evaluation) and **LOGOS Create** (concept generation).
- Its nine perspectives map to the evaluation dimensions in the **Decision Studio** (RS-LIC Section 6).
- The Council's reasoning is expressed in **LRL** (LogoMind Reasoning Language).
