---
doc_id: PROD-JOURNEY-001
title: LogoMind User Journey
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-07-17
related:
  - PROD-VISION-001 Product Vision
  - PROD-PERSONA-001 User Personas
  - LOGOS Architecture (engine pipeline)
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-JOURNEY-001 — User Journey

> *This is the project arc from Maya's perspective — what she does, what she sees, what she feels, at each stage. The LOGOS engines are invisible; the journey is what she experiences.*

---

## Overview

A LogoMind project has **nine stages**, grouped into **four phases**. Each stage maps to one or more LOGOS engines working behind the scenes, but Maya never sees the engines — she sees their output.

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE LOGOMIND PROJECT JOURNEY                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ENTRY        DISCOVERY        STRATEGY         EXPLORATION      │
│  ─────        ─────────        ────────         ───────────      │
│  1. Start     2. Discover      4. Strategise    6. Explore      │
│               3. Workshop                       5. Insight      │
│                                                                  │
│  CRAFT        DELIVERY                                          │
│  ─────        ────────                                          │
│  7. Sketch    9. Present                                        │
│  8. Critique                                                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stage 1 — Start a Project (Entry)

### What Maya Does
- Opens LogoMind
- Clicks **"+ New Project"**
- Enters: Company Name, Industry, Client Contact (optional)
- Pastes the client brief (any completeness level — even just "they make furniture")

### What Maya Sees
- A clean dashboard with "Recent Projects" and "+ New Project"
- A simple form — Company Name, Industry, Brief (large text area)
- An optional "Client Contact" field for sharing the Discovery Workshop later
- A single button: **"Analyze Project →"**

### What Maya Feels
- *"This is simple — I can start in 30 seconds."*
- Relief that she doesn't have to fill a 50-field intake form

### Engine Activity
- None yet — this is data entry

### Entry Condition
- Maya has a project (paid or speculative)
- Exit Condition: Brief submitted → proceed to Stage 2 (Discovery)

---

## Stage 2 — Discovery: Analysis (Discovery Engine)

### What Maya Does
- Submits the brief
- Waits while LogoMind analyses (~30–60 seconds)
- Reviews the **Brand Confidence Score** and Discovery Summary

### What Maya Sees
- A "thinking" state — LogoMind is processing
- The **Brand Confidence Score** (0–100%):
  ```
  Brief Completeness
  ████████████░░░░░░░░  62%
  Confidence: Medium
  ```
- A **Missing Information** panel: what's known, what's inferred, what's missing
- A recommendation:
  - **Score ≥ 90%**: "You have a rich brief. Proceed to Strategy."
  - **Score 60–89%**: "Good foundation. Let me ask a few high-impact questions." (Guided Discovery)
  - **Score < 60%**: "Let's run a Discovery Workshop with your client." (Workshop Mode)

### What Maya Feels
- *"Oh — the brief is actually incomplete. I hadn't noticed."*
- *"LogoMind noticed what I would have missed."*
- Confidence that the strategic work will be grounded

### Engine Activity
- **LOGOS Discover** (LOG-DISC-001): Brief Quality Check, Missing Information Detector

### Exit Condition
- Brand Confidence Score ≥ 70% → proceed to Stage 4 (Strategy)
- Score < 70% → proceed to Stage 3 (Workshop or Guided Discovery)

---

## Stage 3 — Discovery Workshop (If Brief Is Incomplete)

### What Maya Does
- **Option A (Guided Discovery)**: Answers 3–5 high-impact questions LogoMind surfaces
- **Option B (Workshop Mode)**: Invites the client (via link) to a 10–15 minute interactive workshop, OR runs it herself as a structured interview

### What Maya Sees (Workshop Mode)
- Seven-stage guided workshop (per LOG-DISC-001):
  1. Know Your Business
  2. Know Your Customers
  3. Discover Personality
  4. Emotional Destination
  5. Intent Extraction ("I like gold" → "What about gold?")
  6. Inspiration Without Copying
  7. What to Avoid
- Interactive cards (per the Brand Discovery Canvas concept)
- Progress indicator and estimated time remaining
- The **Intent Extraction Engine** translating preferences into intent in real time

### What Maya Feels
- *"My client is actually articulating their brand — finally."*
- *"This would have taken me an hour of unstructured conversation."*
- Professional pride that she's running a disciplined discovery

### Engine Activity
- **LOGOS Discover** (LOG-DISC-001): Discovery Workshop, Intent Extraction Engine
- **LOGOS Strategy** (LOG-STRAT-001) begins populating as inputs arrive

### Exit Condition
- Workshop complete → Brand Confidence Score recalculated → proceed to Stage 4 (Strategy)

---

## Stage 4 — Strategy: Brand DNA (Strategy Engine)

### What Maya Does
- Reviews the generated **Brand DNA**
- Adjusts any element that doesn't match her understanding
- Approves the Brand DNA (or flags concerns)

### What Maya Sees
- A structured Brand DNA document:
  ```
  PURPOSE: <one-sentence statement>
  POSITIONING: <full positioning statement>
  DIFFERENTIATION: <primary differentiator + Three Tests evidence>
  AUDIENCE: <configuration — concerns, contexts, vocabularies>
  PERSONALITY: <character description, not adjectives>
  ARCHETYPE: <identified archetype or "no clean archetype">
  EMOTIONAL GOAL: <what the audience should feel>
  ```
- Each element expandable to show reasoning + confidence level
- **Contradictions flagged** — never silently resolved
- Edit controls for Maya to refine based on her client knowledge

### What Maya Feels
- *"I've never seen this client's brand articulated this clearly."*
- *"This is what I've been missing — a strategic foundation."*
- Empowerment — she understands the brand deeply before sketching

### Engine Activity
- **LOGOS Strategy** (LOG-STRAT-001): 7-step synthesis, applying Brand Strategy Series

### Exit Condition
- Brand DNA approved → proceed to Stage 5 (Insight)

---

## Stage 5 — Insight: Research & Trends (Insight Engine)

### What Maya Does
- Reviews the **Insight Report** (category context, clichés, opportunities, trends)
- Notes what to avoid and where the white space is

### What Maya Sees
- **Industry Analysis**: what the category looks like, common symbols, palettes
- **Competitor Map**: identified competitors with their visual language
- **Cliché Avoidance Report**: symbols that are overused in this category
- **Opportunities**: where the white space is
- **Trend Intelligence**: context-aware recommendations with the Trend vs Timeless Meter:
  ```
  Timeless ◄━━━━━━━━━━●━━━━━► Trend-forward
                       75% / 25%
  Recommended for this brand
  ```

### What Maya Feels
- *"I didn't realise how overused [symbol] was in this category."*
- *"Now I know where to differentiate."*
- Confidence that her concept won't be cliché

### Engine Activity
- **LOGOS Insight** (LOG-INSIGHT-001): industry analysis, competitor mapping, cliché detection, trend intelligence

### Exit Condition
- Insight Report reviewed → proceed to Stage 6 (Create)

---

## Stage 6 — Create: Concept Families (Create Engine)

### What Maya Does
- Reviews the **3–5 Concept Families** LogoMind generated
- Reads each family's theme, symbols, visual language, and rationale
- Chooses 1–2 families to develop further (the SSB will focus on the strongest)

### What Maya Sees
- Concept Family cards:
  ```
  ┌─────────────────────────────┐
  │ FAMILY A — Nature + Tech     │
  │ Theme: Sustainable precision │
  │ Symbols: leaf, hexagon,      │
  │          growth rings        │
  │ Visual language: organic     │
  │  geometry, balanced asymm.   │
  │ Why it works: <reasoning>    │
  │ Confidence: C4               │
  │ [Recommendation: Strong]     │
  └─────────────────────────────┘
  ```
- Each family expandable to show full detail
- Creative Council assessment per family (the 9 minds' take)
- Cliché flags on any symbol that risks overuse
- **Creative Director Mode** notices where appropriate: *"The client requested [X], but [Y] may serve their intent better…"*

### What Maya Feels
- *"These aren't logos — they're directions. I can think within them."*
- *"This breaks my creative rut — I'd never have considered Family C."*
- Ownership — she chooses; LogoMind doesn't decide

### Engine Activity
- **LOGOS Create** (LOG-CREATE-001): Combination Method, Concept Family generation, Creative Council assessment

### Exit Condition
- Maya selects 1–2 families → proceed to Judge (which may send back for refinement)

---

## Stage 7 — Judge: Evaluation (Judge Engine)

### What Maya Does
- Reviews the **Judge Report** for each family she selected
- Sees the 10-dimension scores with reasoning
- Reads the Creative Council verdicts
- Decides which family to develop (or requests refinement)

### What Maya Sees
- Per-family evaluation:
  ```
  FAMILY A — Nature + Tech
  Creative Council: 7/9 minds endorse; Context mind flags favicon risk
  Jury Scores:
    Meaning:        8.5  ████████▌
    Simplicity:     9.0  █████████
    Clarity:        7.5  ███████▌
    Originality:    8.0  ████████
    Memorability:   7.0  ███████
    Authenticity:   9.0  █████████
    Timelessness:   8.5  █████████▌
    Relevance:      8.0  ████████
    Consistency:    7.5  ███████▌
    Brand Fit:      9.5  █████████▌
  COMPOSITE: 8.3 — DEVELOP WITH REFINEMENT
  Refinement: strengthen memorability; test at favicon size
  ```
- Concept DNA fingerprint for objective comparison

### What Maya Feels
- *"Now I know what to refine before I sketch."*
- *"The evaluation is honest — it flags uncertainty, doesn't fake confidence."*
- Trust in the system — it's a real second opinion

### Engine Activity
- **LOGOS Judge** (LOG-JUDGE-001): Creative Council + Design Jury scoring

### Exit Condition
- Maya chooses a family → proceed to Stage 8 (SSB + Sketch)

---

## Stage 8 — SSB + Sketch (Craft Phase)

### What Maya Does
- Receives the **Strategic Sketch Brief** — the flagship output
- Reads the brief: the creative North Star, the opportunities, the sketch missions
- Leaves LogoMind to sketch in her own tools (Figma, Illustrator, paper)
- Returns to upload sketches for critique (optional, iterative)

### What Maya Sees — The SSB

The Strategic Sketch Brief (full structure specified in PROD-SSB-001):

```
1. PROJECT ESSENCE        — one-paragraph synthesis
2. BRAND DNA SNAPSHOT     — the six strands
3. CREATIVE NORTH STAR    — the single sentence
4. CREATIVE TERRITORIES   — chosen family + alternatives
5. OPPORTUNITIES & WARNINGS — explore this; avoid that
6. CREATIVE COUNCIL ADVICE — 9-mind guidance table
7. SKETCH MISSIONS        — 5-10 specific directions with rationale
```

### What Maya Sees — Sketch Coach (when she returns)

When she uploads a sketch, the Sketch Coach (LOG-COACH-001) responds conversationally:
> *"Good start. Have you considered removing the secondary outline? It may not survive at favicon size. Also — the negative space beneath the bridge could form an arch, adding a secondary meaning. What's your instinct?"*

### What Maya Feels
- *"I have a strategic foundation I've never had before."*
- *"I'm sketching with intention, not guessing."*
- *"The Coach is a collaborator, not an instructor."*

### Engine Activity
- **SSB Composer** assembles the brief from Judge output
- **LOGOS Coach** (LOG-COACH-001): conversational guidance on uploaded sketches

### Exit Condition
- Maya finalises a concept → proceed to Stage 9 (Presentation)

---

## Stage 9 — Presentation (Delivery)

### What Maya Does
- Requests LogoMind generate a **client-ready presentation** from the project history
- Reviews the generated deck
- Customises as needed
- Exports (PDF, Keynote, or shareable link)

### What Maya Sees
- A structured 10-section presentation (per LOG-PRESENT-001):
  1. Cover
  2. Executive summary
  3. Brand foundation
  4. Strategic exploration
  5. The chosen concept
  6. Design rationale (symbol, colour, typography, construction)
  7. Applications (favicon, signage, monochrome, reverse)
  8. Future-proofing
  9. Brand guidelines summary
  10. Q&A preparation
- **Objection-handling notes** for likely client concerns
- Export options

### What Maya Feels
- *"I can defend this work strategically — not just aesthetically."*
- *"The client will understand WHY, not just WHAT."*
- Professional confidence — she's presenting as a strategist, not just a designer

### Engine Activity
- **LOGOS Present** (LOG-PRESENT-001): narrative assembly, rationale generation, objection preparation

### Exit Condition
- Presentation exported → project delivered → Maya returns for the next project

---

## The Emotional Arc

Across the nine stages, Maya's emotional journey is:

```
Stage 1 (Start):        Neutral → Mild engagement
Stage 2 (Discovery):    Surprise → "LogoMind noticed what I missed"
Stage 3 (Workshop):     Relief → "The client is articulating their brand"
Stage 4 (Strategy):     Empowerment → "I understand this brand deeply"
Stage 5 (Insight):      Clarity → "I know where to differentiate"
Stage 6 (Create):       Stimulation → "New directions I wouldn't have considered"
Stage 7 (Judge):        Confidence → "I know what to refine and why"
Stage 8 (Sketch):       Ownership → "I'm crafting with intention"
Stage 9 (Present):      Pride → "I can defend this work strategically"
```

The emotional target: Maya feels like a **strategically grounded creative professional** — not a technician executing a brief, but a thinker making defensible decisions.

---

## The Invisible Engines

Throughout the journey, the LOGOS engines are **invisible** — Maya never thinks about "running the Strategy Engine" or "invoking the Creative Council." She experiences:

- A brief that gets richer
- A brand that becomes clear
- A category that becomes navigable
- Concepts that emerge strategically
- An evaluation that's honest
- A brief that gives her direction
- A coach that helps her refine
- A presentation that sells the reasoning

The engines are the means; the experience is the product.

---

## Journey Variants

The journey above is the **full path** (brief starts incomplete, runs Workshop). Variants:

### Fast Path (Brief Starts Complete)
- Stage 1 → Stage 2 (high score) → Stage 4 → Stage 5 → Stage 6 → Stage 7 → Stage 8 → Stage 9
- Workshop (Stage 3) is skipped

### Entrepreneur Path (Elena)
- Stage 1 → Stage 2 (low score) → Stage 3 (Workshop, self-run) → Stage 4 (Brand DNA only)
- Elena exports the Brand DNA + SSB as a brief for a designer
- Stages 5–9 are for the designer she hires

### Studio Path (Marcus's team)
- Same as Maya's journey, but with shared projects, version history, and team visibility

---

*LogoMind Principle: The journey is what the designer experiences. The engines are invisible. Every stage must produce a tangible artefact the designer can see, share, or act on — never just "processing."*
