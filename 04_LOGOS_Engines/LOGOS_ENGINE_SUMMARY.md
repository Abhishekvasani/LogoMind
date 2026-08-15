---
doc_id: LOG-PIPE-001
title: LOGOS Pipeline & Engine Summary
version: 2.0
status: Approved (summary) — all pipeline engines fully specified and implemented
governance_level: L2 — Engine Specifications
last_reviewed: 2026-08-14
---

# LOGOS Pipeline — Engine Summary

> All pipeline engines have full Approved specifications and running implementations. This summary tracks the pipeline shape at a glance; each engine's authoritative definition lives in its own LOG-XXX-001 spec.

---

## The Full Pipeline

```
Client Brief (+ optional Contest Brief, decoded by LOG-CBD-001)
     │
     ▼
┌─────────────────────────────────────┐
│  1. LOGOS Discover                  │  ← LOG-DISC-001 (full spec)
│     Understand the client           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  2. LOGOS Strategy                  │  ← LOG-STRAT-001
│     Create Brand DNA                │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  3. LOGOS Insight                   │  ← LOG-INSIGHT-001
│     Industry, psychology, semiotics │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  4. LOGOS Create                    │  ← LOG-CREATE-001
│     Generate creative territories   │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  5. LOGOS Judge                     │  ← LOG-JUDGE-001 + LOG-CC-001
│     Evaluate concepts               │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  6. LOGOS Client Fit                │  ← LOG-CFP-001
│     Predict client appeal           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  7. LOGOS Concept Prompt            │  ← LOG-CP-001
│     Executable concepts + wireframes│
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  8. Strategic Sketch Brief (SSB)    │  ← THE PRIMARY OUTPUT
│     The designer's creative report  │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│  9. LOGOS Coach                     │  ← LOG-COACH-001
│     Help designers sketch           │
└─────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────┐
│ 10. LOGOS Present                   │  ← LOG-PRESENT-001
│     Build presentations             │
└─────────────────────────────────────┘
```

Input tooling alongside the pipeline: **LOG-CBD-001 Contest Brief Decoder** (freelancer-style brief → structured ContestBrief, feeding Client Fit and enriching the brief for Discovery/Strategy).

**Knowledge grounding:** every LLM engine except the Contest Decoder (extraction-pure by design) and Discovery injects curated extracts from the 24-volume LIC corpus at prompt-build time (`backend/app/services/lic_knowledge.py`; `/health` reports the state).

---

## Engine 2: LOGOS Strategy (Brand DNA Engine)

**Status:** Fully specified (LOG-STRAT-001) and implemented. Injects the five Brand Strategy frameworks (RS-LIC-BS-001…005).

| | |
|---|---|
| **Mission** | Create a complete Brand DNA profile from discovery output. |
| **Inputs** | Discovery Summary, Brand Confidence Score |
| **Outputs** | Brand DNA: Purpose, Positioning, Differentiation, Audience Configuration, Personality, Archetype, Emotional Goal, flagged contradictions |

The **LogoMind Brand DNA Framework** has six strands: Purpose, Audience, Personality, Emotion, Differentiation, Promise.

---

## Engine 3: LOGOS Insight (Research Engine)

**Status:** Fully specified (LOG-INSIGHT-001) and implemented. Injects the Trend Taxonomy (PH-008), Relevance Dial (PH-009), Symbol volume, and Industry Intelligence.

| | |
|---|---|
| **Mission** | Apply branding knowledge to the specific project context. |
| **Inputs** | Brand DNA, Industry |
| **Outputs** | Industry Intelligence (conventions, cliché avoidance, opportunities, visual expectations, trend recommendation) |

Includes the **Trend Intelligence Advisor** — classifies trends as Timeless / Emerging / Short-lived / Overused, with a **Trend vs Timeless Meter** recommendation per project.

---

## Engine 4: LOGOS Create (Creative Engine)

**Status:** Fully specified (LOG-CREATE-001) and implemented. Injects the Symbol (33 entries), Color (18 + WCAG), Typography, Identity, and Industry volumes + PH-005 + style anchors.

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

---

## Engine 5: LOGOS Judge (Creative Council + Design Jury)

**Status:** Fully specified (LOG-JUDGE-001 + LOG-CC-001) and implemented. Injects PH-005/003/004/006/008 (five scored dimensions grounded) + the Trademark volume for legal-risk signalling.

**The Design Jury scores concepts across:** originality, memorability, simplicity, clarity, timelessness, authenticity, relevance, consistency, brand fit — with a 0–10 composite, classification (recommended / develop / reject), and a Concept DNA fingerprint.

Only concepts that pass the Creative Council's nine minds and score above threshold proceed.

---

## Engine 6: LOGOS Client Fit (Client Preference Predictor)

**Status:** Fully specified (LOG-CFP-001) and implemented.

Models the specific decision-maker (persona: archetype, aesthetic lean, boldness tolerance, decoded intents) and ranks each Concept Family by predicted resonance with THAT persona — deliberately diverging from the Judge's excellence scores. A refine loop folds in revealed contest preferences (ratings, eliminations, comments). Grounded by the Color/Symbol volumes, the twelve archetypes, Client Psychology (decision-maker types), and Contest Dynamics.

---

## Engine 7: LOGOS Concept Prompt (Concept Prompt Engine)

**Status:** Fully specified (LOG-CP-001, FD-015) and implemented.

Turns an evaluated family into an **executable concept**: four prompt variants (minimal / detailed / typographic-led / symbolic), five per-model adaptations (Midjourney, Ideogram, Stable Diffusion, Recraft, general), a composition wireframe SPEC (deterministic, rendered as a drafting plate), rationale, and clichés avoided. Generates no images; makes no creative decision. Grounded by PH-005, the Identity volume (grids, logo types, optical correction), and Production standards.

---

## The Flagship Output: Strategic Sketch Brief (SSB)

**Status:** Fully specified (CTO Decision #012; FD-014) and implemented.

> LogoMind's primary output is **not a logo concept.** It is a **Strategic Sketch Brief** — a complete creative strategy that gives the designer everything needed to sketch confidently.

### SSB Structure

1. **Project Essence** — one-paragraph synthesis.
2. **Brand DNA Snapshot** — the six strands.
3. **Creative North Star** — the single sentence the logo must embody.
4. **Selected Territory** — the chosen strategic direction with visual language and symbols.
5. **Opportunities & Warnings** — what to explore; what to avoid (clichés).
6. **Creative Council Advice** — the nine minds' guidance.
7. **Sketch Missions** — specific sketch directions, each with: core idea, why it works, potential pitfalls.

---

## Engine 9: LOGOS Coach (Sketch Coach)

**Status:** Fully specified (LOG-COACH-001) and implemented. Injects Simplicity + Clarity audits and the Production standards (favicon, embroidery, monochrome constraints).

Guides the designer's sketching — not by drawing for them, but by suggesting *where to start, what geometric relationships to test, where to introduce negative space, what proportions to explore, what to avoid.*

> "Begin with a circle-based grid. Explore three variations where the negative space forms the initial 'A'. Keep line weights consistent and test the icon in monochrome before introducing color."

---

## Engine 10: LOGOS Present (Presentation Builder)

**Status:** Fully specified (LOG-PRESENT-001) and implemented. Injects Client Psychology — the Objection Taxonomy grounds its objection-handling output; the Rationale Narrative shapes its reasoning sections.

Assembles the client presentation from project data: story, symbolism, typography rationale, colour rationale, construction logic, scalability notes, future-proofing, trend relevance.

> **Clients buy the reasoning as much as the design.**

---

## Input Tooling: Contest Brief Decoder

**Status:** Fully specified (LOG-CBD-001) and implemented.

Normalises a pasted freelancer-style contest brief into a structured ContestBrief — extraction ONLY, inventing nothing. The decoded preferred/avoided colours are the holder's only pre-committed taste; the brief enriches the project and feeds Client Fit. Deliberately knowledge-free beyond contest-dynamics context (creativity is a defect in extraction).

---

## Parked / Future Engines

- **Reflection Engine** — captures designer learnings from real projects; feeds LMKC (with human approval).
- **Inspiration Engine** — analyses uploaded logos for *why* they appeal (without copying).
- **Design Mentor** — conversational mentor that asks questions instead of giving answers.
- **Creative Memory** — *rejected* in favour of project-specific memory + knowledge base (FD: "Remember knowledge, not preferences").
