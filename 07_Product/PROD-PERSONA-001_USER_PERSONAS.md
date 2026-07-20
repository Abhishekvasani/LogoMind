---
doc_id: PROD-PERSONA-001
title: LogoMind User Personas
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-07-17
related:
  - PROD-VISION-001 Product Vision
  - RS-LIC-BS-003 Target Audience (methodology source)
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-PERSONA-001 — User Personas

> *This document applies LogoMind's own audience methodology (RS-LIC-BS-003) to itself. Each persona is a configuration of concerns, contexts, and vocabularies — not a demographic bucket.*

---

## Overview

LogoMind serves three primary personas. They share the discipline of identity design but differ in scale, constraints, and what they need from LogoMind. Every Phase 4 screen, workflow, and feature must serve at least one persona clearly — and must not alienate the others.

| Persona | Primary | Secondary |
|---------|---------|-----------|
| **Maya — The Solo Freelancer** | ✅ Primary user | The core persona LogoMind is built for first |
| **Marcus — The Small Studio Lead** | ✅ Primary user | Represents the team-collaboration dimension |
| **Elena — The Strategic Entrepreneur** | 🟡 Secondary | Discovers LogoMind for self-understanding before hiring a designer |

---

## Persona 1: Maya — The Solo Freelancer

### Identity
- **Name:** Maya Chen
- **Role:** Independent identity designer
- **Experience:** 4–8 years professional
- **Working context:** Solo; home studio or co-working space; 8–15 identity projects per year

### Configuration (per RS-LIC-BS-003)

**Concerns**
- *“I want to do strategically grounded work, not just decorative work.”*
- *“I don't have a creative director to bounce ideas off.”*
- *“Clients come to me with vague briefs and I spend hours extracting what they actually want.”*
- *“I’m never fully sure if my concept is genuinely good or just feels good to me.”*
- *“I lose work to agencies who present better even when my design is stronger.”*

**Contexts**
- Works from a laptop, often in coffee shops or home studio
- Encounters briefs through email, referrals, freelance platforms
- Presents to clients via video calls and PDF decks
- Uses Figma/Illustrator for execution; uses no strategic tooling

**Vocabularies**
- Fluent in design vocabulary (typography, composition, craft)
- *Less* fluent in strategy vocabulary (positioning, archetypes, differentiation tests)
- Responds to mentor-like voice; resists corporate voice

### What Maya Needs From LogoMind

| Need | LogoMind Capability |
|------|---------------------|
| Help extracting a real brief from a confused client | Discovery Engine — Guided Discovery + Workshop modes |
| A structured strategic process she doesn't have to invent | Strategy Engine — Brand DNA Builder |
| A creative director's perspective on her concepts | Creative Council (9 minds) + Judge Engine |
| Confidence her concept is defensible before presentation | Judge Report + SSB |
| Help presenting strategically, not just aesthetically | Presentation Builder |

### Maya's Success Moment

> *“I used to dread the client call where they ask ‘why this concept?’ Now I have the reasoning ready. The client bought the work without a single revision.”*

### What Would Make Maya Leave

- LogoMind generating logos and skipping the thinking (violates the promise)
- A corporate/enterprise voice that doesn't respect her craft
- Being treated as a junior designer rather than a professional
- Slow, multi-step workflows that interrupt her momentum

---

## Persona 2: Marcus — The Small Studio Lead

### Identity
- **Name:** Marcus Okafor
- **Role:** Founder/lead designer at a 3–8 person identity studio
- **Experience:** 8–15 years professional
- **Working context:** Small studio; 20–40 identity projects per year; manages junior designers

### Configuration

**Concerns**
- *“My junior designers produce inconsistent strategic work.”*
- *“I want a repeatable process so quality doesn't depend on which designer takes the project.”*
- *“I'm the creative director but I can't be in every meeting.”*
- *“We need to scale without losing quality.”*
- *“New hires take months to get up to speed on how we think.”*

**Contexts**
- Works from a studio; team uses shared project management tools
- Briefs come through the studio's intake process
- Presents to clients as a team
- Uses Figma, Notion, Slack; some legacy Adobe workflow

**Vocabularies**
- Fluent in both design and strategy vocabulary
- Speaks the language of process, systems, consistency
- Responds to professional, structured voice

### What Marcus Needs From LogoMind

| Need | LogoMind Capability |
|------|---------------------|
| A repeatable strategic process for the studio | LOGOS pipeline as standardised workflow |
| Onboarding for new designers into studio thinking | The LICs as training material |
| Consistent quality control across designers | Judge Engine as the studio's quality gate |
| Shared project memory (per-project, not global) | Project Memory (per FD-007) |
| Team visibility into strategic reasoning | SSB as the shared strategic artefact |

### Marcus's Success Moment

> *“Our junior designers are producing work I used to only expect from seniors. The Judge Engine catches what I would have caught — before I have to.”*

### What Would Make Marcus Leave

- No team collaboration features (he needs shared projects)
- Inconsistent output across runs of the same brief
- Lack of version control / project history
- Quality that varies by which designer inputs the brief

---

## Persona 3: Elena — The Strategic Entrepreneur

### Identity
- **Name:** Elena Vasquez
- **Role:** Founder of a 2-year-old consumer brand; considering a rebrand
- **Experience:** Business expert, design novice
- **Working context:** Pre-designer; wants to understand her own brand before hiring

### Configuration

**Concerns**
- *“I don't know how to brief a designer properly.”*
- *“I know my business but not how to express it as a brand.”*
- *“Designers I've spoken to use vocabulary I don't understand.”*
- *“I don't want to pay for strategy I could do myself if I had the right tool.”*
- *“I want to walk into a designer relationship with clarity.”*

**Contexts**
- Works from phone and laptop between business tasks
- Encounters LogoMind through entrepreneur communities, design blogs
- Intends to hire a designer after using LogoMind

**Vocabularies**
- Fluent in business vocabulary (positioning, audience, market)
- *Not* fluent in design vocabulary
- Responds to plain-language explanation; intimidated by jargon

### What Elena Needs From LogoMind

| Need | LogoMind Capability |
|------|---------------------|
| Help articulating her brand strategically | Discovery Workshop (Inspiration Mode) |
| A brief she can take to a designer | SSB (exportable as a designer-ready document) |
| Plain-language explanation of strategy concepts | Progressive Disclosure (Layer A) |
| Understanding of what she should ask a designer for | SSB + Brand DNA |

### Elena's Success Moment

> *“I walked into my first designer meeting with a brief that impressed them. They said I'd done the strategy work they usually have to extract from clients.”*

### What Would Make Elena Leave

- Design jargon without plain-language translation
- Pressure to design the logo herself (she knows she shouldn't)
- A process that assumes design expertise she doesn't have

---

## Persona Priority for v1

For Phase 5 (Technical Build) v1, the priority is:

```
Maya (Solo Freelancer)  ████████████████████  PRIMARY — every feature must serve her
Marcus (Studio Lead)    ████████████          SECONDARY — team features can be v2
Elena (Entrepreneur)    ████████              TERTIARY — Discovery Workshop serves her standalone
```

**Rationale:** Maya is the persona the Product Vision is built for. Building for her first ensures the core experience is excellent. Marcus's team needs can be layered on in v2 without rework. Elena is served by the Discovery Workshop, which is also Maya's entry point — building it serves both.

---

## Persona Anti-Patterns (Who We're NOT Building For)

These personas are explicitly *not* served — and features aimed at them should be rejected:

| Anti-Persona | Why Excluded |
|--------------|--------------|
| **"I just want a logo fast"** | LogoMind adds time to strategy; if you want to skip strategy, use a generator |
| **"I want AI to make the creative decisions"** | Violates the Product Promise (FD-005) |
| **"I want to generate 100 logo options"** | LogoMind generates Concept Families (3–5), not logo spam |
| **"I don't want to think; I want output"** | LogoMind develops judgment, which requires engagement |

---

## How Personas Govern Phase 4

Every screen, workflow, and feature in Phase 4 must:

1. **Serve Maya clearly** — she is the v1 user.
2. **Not alienate Marcus** — the experience should scale to team use later.
3. **Welcome Elena where natural** — particularly in Discovery Workshop.

If a feature serves none of these personas, or primarily serves an anti-persona, it is rejected.

---

*LogoMind Principle: LogoMind is built first for the solo designer who wants to do strategically grounded work but lacks the strategic resources of a full agency. Every other audience is welcomed after that core experience is excellent.*
