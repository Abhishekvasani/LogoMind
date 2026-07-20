---
doc_id: PROD-DW-001
title: Brand Discovery Workshop — Full UX Specification
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-07-17
related:
  - LOG-DISC-001 Discovery Engine (reasoning source)
  - PROD-SCREEN-001 Screen Architecture (Screen 3)
  - PROD-JOURNEY-001 User Journey (Stage 3)
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-DW-001 — Brand Discovery Workshop (Full UX Spec)

> *The Discovery Workshop is LogoMind's hero feature. It is where the confused client becomes articulate, the vague brief becomes rich, and the designer's strategic work becomes possible. If we perfect only one feature, it is this one.*

---

## 1. Purpose

The Discovery Workshop transforms an incomplete client brief into a rich strategic foundation — through a guided, adaptive, 10–15 minute experience that feels like a conversation with a world-class brand consultant.

It is *not* a form. It is *not* a questionnaire. It is an **experience** — adaptive, conversational, and patient.

---

## 2. The Three Modes

Per the Discovery Engine (LOG-DISC-001), the Workshop has three modes based on Brand Confidence Score:

| Mode | Trigger | Description |
|------|---------|-------------|
| **Expert Mode** | Score ≥ 90% | No workshop needed; brief is rich enough to proceed directly to Strategy |
| **Guided Discovery** | Score 60–89% | 3–5 high-impact missing questions only; Maya answers herself |
| **Workshop Mode** | Score < 60% | Full 7-stage interactive workshop; can be self-run or with client |

This document specifies **Guided Discovery** and **Workshop Mode** in detail. Expert Mode skips the workshop entirely.

---

## 3. Guided Discovery Mode (Brief Score 60–89%)

### When It Activates
The brief has substance but is missing a few high-impact elements. LogoMind surfaces *only the questions whose answers would most change the creative direction* (per the Missing Information Detector, LOG-DISC-001).

### Experience
- 3–5 questions maximum
- One question at a time
- Each question explains why it's being asked (per CTO Decision #019: never ask without answering "Why am I asking?")
- ~2–3 minutes total

### Example Flow

```
┌────────────────────────────────────────────────┐
│  Guided Discovery — 3 questions                │
│  ████████░░░░░░░░░░░░  Q1 of 3                 │
│                                                 │
│  Q: Who is your ideal customer?                │
│                                                 │
│  Why I'm asking:                                │
│  Your brief mentions "coffee drinkers" — a     │
│  broad group. Knowing the specific audience     │
│  helps me calibrate the identity's voice.       │
│                                                 │
│  Choose all that fit, or type your own:         │
│  [ ] Urban professionals                         │
│  [ ] Students                                   │
│  [ ] Families                                   │
│  [ ] Luxury customers                           │
│  [ ] ___________________________________        │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

### Key Principle
**Every question shows its "Why."** This respects the user's intelligence and models the strategic thinking LogoMind teaches.

---

## 4. Workshop Mode (Brief Score < 60%) — The Hero Feature

### When It Activates
The brief is too thin to support strategic work. Common triggers:
- Only company name + industry provided
- Brief is generic ("we're a coffee shop")
- Brief contradicts itself or lacks audience/positioning

### Two Running Options

**Option A: Self-Run (Maya interviews the client externally)**
- Maya runs the workshop herself, typing client responses
- Useful when Maya has the client on a call

**Option B: Client-Run via Link (the client takes it directly)**
- Maya sends a link; the client completes it on their own time
- LogoMind's voice is warm, plain-language, and patient
- Results sync back to Maya's project when complete

### The Seven Workshop Stages

Each stage is one screen, one question cluster, one step forward. Progress is always visible.

---

### Stage 1 — Know Your Business

**Goal:** Capture the business basics and the origin story.

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Welcome to Your Brand Discovery                │
│  This usually takes 10–15 minutes.              │
│  Stage 1 of 7 — Know Your Business              │
│  ░░░░░░░░░░░░░░░░░░░░░  Progress                │
│                                                 │
│  Tell me about your business.                   │
│  What do you do, and why did you start?         │
│                                                 │
│  [_____________________________________]        │
│  [_____________________________________]        │
│  [_____________________________________]        │
│                                                 │
│  What type of [industry] are you?               │
│  [ ] Premium                                    │
│  [ ] Mid-market                                 │
│  [ ] Accessible                                 │
│  [ ] Niche / specialist                         │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Captures factual business info
- Begins populating the Brand DNA (purpose seed)
- Intent Extraction begins (e.g., "premium" → signals positioning intent)

---

### Stage 2 — Know Your Customers

**Goal:** Identify audience configuration (RS-LIC-BS-003).

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 2 of 7 — Know Your Customers             │
│  ███░░░░░░░░░░░░░░░░░░░  Progress               │
│                                                 │
│  Who buys from you?                             │
│  [ ] Families                                   │
│  [ ] Professionals                              │
│  [ ] Businesses                                 │
│  [ ] Students                                   │
│  [ ] Luxury customers                           │
│  [ ] Other: ________________                    │
│                                                 │
│  What do they care about most?                  │
│  [ ] Price                                      │
│  [ ] Quality                                    │
│  [ ] Trust                                      │
│  [ ] Innovation                                 │
│  [ ] Status                                     │
│  [ ] Sustainability                             │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Builds audience configuration
- Notes concerns, contexts, vocabularies
- Begins inferring positioning relative to audience

---

### Stage 3 — Discover Personality

**Goal:** Evoke brand personality through metaphor (RS-LIC-BS-004).

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 3 of 7 — Discover Personality            │
│  ██████░░░░░░░░░░░░░░░░  Progress               │
│                                                 │
│  If your brand walked into a room,              │
│  how would people describe it?                  │
│                                                 │
│  Pick the words that fit (choose 3–5):          │
│                                                 │
│  [ ] Elegant      [ ] Bold                      │
│  [ ] Friendly     [ ] Intelligent               │
│  [ ] Adventurous  [ ] Traditional               │
│  [ ] Premium      [ ] Playful                   │
│  [ ] Calm         [ ] Energetic                 │
│  [ ] Authoritative [ ] Approachable             │
│                                                 │
│  Why did you choose those? (Optional)           │
│  [_____________________________________]        │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Captures personality traits
- Begins coherence testing (RS-LIC-BS-004) — do the traits hang together?
- Flags contradictions (e.g., "Traditional" + "Energetic" may need resolution)

---

### Stage 4 — Emotional Destination

**Goal:** Identify the emotional goal — what audiences should feel.

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 4 of 7 — Emotional Destination           │
│  █████████░░░░░░░░░░░░░  Progress               │
│                                                 │
│  How should someone feel immediately            │
│  after seeing your logo for the first time?     │
│                                                 │
│  [ ] Safe          [ ] Excited                  │
│  [ ] Curious       [ ] Inspired                 │
│  [ ] Confident     [ ] Relaxed                  │
│  [ ] Proud         [ ] Powerful                 │
│  [ ] Welcomed      [ ] Intrigued                │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Captures the emotional goal
- Links to Brand DNA's "Emotional Goal" field
- Begins to map to colour/typography implications

---

### Stage 5 — Intent Extraction

**Goal:** Translate preferences into intent (per the Intent Extraction Engine, LOG-DISC-001).

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 5 of 7 — Intent Extraction               │
│  ████████████░░░░░░░░░░  Progress               │
│                                                 │
│  Do you have any preferences for the logo?      │
│  (Colours, symbols, styles — or things to       │
│  avoid. All optional.)                          │
│                                                 │
│  [_____________________________________]        │
│  [_____________________________________]        │
│                                                 │
│  ── If user mentioned a preference, probe ──    │
│                                                 │
│  You mentioned "gold." What about gold          │
│  appeals to you?                                │
│  [ ] Premium feeling                            │
│  [ ] Luxury                                     │
│  [ ] Success                                    │
│  [ ] Tradition                                  │
│  [ ] Warmth                                     │
│  [ ] ___________________________________        │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- **Intent Extraction active** — translates preferences into strategic intent:
  - "I want blue" → "I want trust"
  - "I want a shield" → "I want security"
  - "I want gold" → "I want premium"
- Stores the *intent*, not just the *preference*
- This is one of LogoMind's signature features

---

### Stage 6 — Inspiration Without Copying

**Goal:** Understand what the client admires, without copying.

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 6 of 7 — Inspiration                     │
│  ███████████████░░░░░░░░  Progress              │
│                                                 │
│  Are there 3–5 logos you admire?               │
│  Upload them, or describe them.                 │
│                                                 │
│  LogoMind will NOT copy them.                   │
│  We'll analyse what you like about them.        │
│                                                 │
│  [ Upload logo 1 ]                              │
│  [ Upload logo 2 ]                              │
│  [ Upload logo 3 ]                              │
│                                                 │
│  What do you like about each?                   │
│  [ ] Simplicity                                 │
│  [ ] Typography                                 │
│  [ ] Colours                                    │
│  [ ] Shape                                      │
│  [ ] Balance                                    │
│  [ ] Boldness                                   │
│  [ ] Other: ________________                    │
│                                                 │
│                [ Continue → ]                    │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Identifies the *patterns* the client responds to (simplicity, boldness, etc.)
- Does NOT store or replicate the specific logos
- Translates preferences into visual language guidance

---

### Stage 7 — What to Avoid

**Goal:** Capture anti-personality — what the brand must never feel like.

**Experience:**
```
┌────────────────────────────────────────────────┐
│  Stage 7 of 7 — What to Avoid                   │
│  ███████████████████░░░  Progress               │
│                                                 │
│  What should your brand NEVER feel like?        │
│                                                 │
│  [ ] Cheap                                      │
│  [ ] Childish                                   │
│  [ ] Aggressive                                 │
│  [ ] Cold                                       │
│  [ ] Generic                                    │
│  [ ] Old-fashioned                              │
│  [ ] Corporate / impersonal                     │
│  [ ] Complicated                                │
│                                                 │
│                [ Complete Workshop → ]           │
└────────────────────────────────────────────────┘
```

**Engine Activity:**
- Captures anti-personality
- Adds constraints to the Brand DNA (what the identity must avoid)
- Recalculates Brand Confidence Score (should now exceed 70%)

---

## 5. Adaptive Branching

The Workshop is not linear for every user. It adapts based on answers:

| Trigger | Adaptation |
|---------|------------|
| User selects "Premium" in Stage 1 | Skip "Accessible" questions later; probe premium cues |
| User answers "I don't know" | Trigger fallback path (see §6) |
| User's personality choices are incoherent | Surface gentle resolution question before proceeding |
| User mentions a specific symbol preference | Trigger Intent Extraction probe immediately |
| User uploads inspirational logos | Add analysis step before proceeding |
| Brand Confidence Score recovers early (> 70%) | Offer to skip remaining stages |

The Workshop is *never longer than it needs to be*. If enough is known, it stops.

---

## 6. Fallback Paths — Handling "I Don't Know"

When the client doesn't know an answer, LogoMind never gets stuck. It shifts to consultant mode:

### Pattern 1: Reframe to Options
> **Client:** "I don't know who my audience is."
>
> **LogoMind:** "That's perfectly common. Most businesses serve a few possible audiences. Here are six common audience types for [industry]. Which feels closest to your best customers?"
>
> [Presents option cards]

### Pattern 2: Reframe to Territory Exploration (Inspiration Mode)
> **Client:** "I really don't know what I want."
>
> **LogoMind:** "Let's explore five different ways your [industry] could be perceived. Each has a different personality and design implication. Which feels closest to your vision?"
>
> [Presents 5 strategic territories — client picks one]

### Pattern 3: Reframe to Story
> **Client:** "I can't articulate our purpose."
>
> **LogoMind:** "Tell me the story of why you started. Don't worry about strategy language — just tell me what happened."
>
> [Open text field; LogoMind extracts purpose from narrative]

The principle: **the Workshop meets the client where they are.** It never demands strategic vocabulary; it helps the client find their strategy through whatever language they have.

---

## 7. The Intent Extraction Engine (Workshop Integration)

Throughout the Workshop, the Intent Extraction Engine is active — translating stated preferences into strategic intent:

| Client Says | Engine Extracts | Stored As |
|-------------|----------------|-----------|
| "I like blue" | → trust | Intent: trust (colour is one expression) |
| "I want a shield" | → security | Intent: security (symbol is one expression) |
| "I want gold" | → premium | Intent: premium (colour is one expression) |
| "I want a lion" | → leadership | Intent: leadership (symbol is one expression) |
| "I want a circle" | → unity | Intent: unity (form is one expression) |
| "I want modern" | → contemporary relevance | Intent: contemporary (style is one expression) |

The Workshop stores *intents*, not *preferences*. This frees the creative work to express the intent through whatever form is most effective — not locked into the client's first instinct about how.

---

## 8. Progress Indicators & Time Budget

### The 5-Minute Rule (Product Law)

The Guided Discovery mode must be completable in **under 5 minutes**. The full Workshop must be completable in **10–15 minutes**. If either exceeds this, the experience is asking low-impact questions and must be refined.

### Progress Display

```
Stage 3 of 7 — Discover Personality
██████░░░░░░░░░░░░░░░░░░  ~8 minutes remaining
```

- Always show current stage
- Always show approximate time remaining
- Never show more than one question at a time (except Stage 6 upload)

---

## 9. Completion & Handoff

When the Workshop completes:

```
┌────────────────────────────────────────────────┐
│  ✓ Workshop Complete                            │
│                                                 │
│  Brand Confidence Score:                        │
│  ████████████████████░  87%                     │
│  Confidence: High                               │
│                                                 │
│  Here's what I understand about your brand:     │
│                                                 │
│  · Purpose: <one-line summary>                  │
│  · Audience: <one-line summary>                 │
│  · Personality: <one-line summary>              │
│  · Emotional Goal: <one-line summary>           │
│                                                 │
│  Is this accurate?                              │
│  [ Yes, proceed → ]    [ Adjust ↺ ]             │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Show what was learned.** The user sees the synthesis, not just "done."
- **Confirm accuracy.** The user validates before strategic work proceeds.
- **Allow adjustment.** If anything is wrong, the user can refine.
- **Route to Strategy.** On confirmation, the project advances to Stage 4 (Strategy).

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Time Budget** | Does Workshop complete in 10–15 minutes? | Yes (5 min for Guided) |
| **One Question at a Time** | Are stages broken into single decisions? | Yes — never overwhelm |
| **Why Visible** | Does every question explain why it's asked? | Yes (CTO Decision #019) |
| **Fallback Coverage** | Are "I don't know" paths graceful? | Yes — never get stuck |
| **Intent Extraction** | Are preferences translated to intents? | Yes — throughout |
| **Confidence Recalculation** | Does score update as Workshop progresses? | Yes — visible progress |

---

## 11. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Too Long** | Workshop exceeds 15 minutes | Time Budget check; trim low-impact questions |
| **No Fallback** | User stuck on "I don't know" | Fallback Coverage; always offer options |
| **Question Fatigue** | User bails mid-Workshop | Progress visible; offer "save and resume"; never too long |
| **Surface Compliance** | User clicks random options to finish | Detect low-engagement patterns; probe in follow-up |
| **Preference Lock-In** | Workshop stores literal preferences, not intents | Intent Extraction active throughout |

---

## 12. The Designer's View of Workshop Output

For Maya (the designer), the Workshop output appears as a refined Discovery Summary + Brand DNA draft in the Strategy View (Screen 4). She doesn't see the raw Workshop responses — she sees the synthesised strategic foundation, with confidence levels and the ability to edit.

For the client (if they took the Workshop via link), they see only the completion confirmation (§9). The strategic synthesis is Maya's to work with.

---

## 13. Future Versions

| Version | Enhancement |
|--------|-------------|
| v1.1 | Video/voice Workshop — client speaks; LogoMind transcribes and extracts |
| v1.2 | Multi-language Workshop — adaptive to client's native language |
| v1.3 | Workshop analytics — show Maya where the client hesitated or struggled |
| v2.0 | Live Workshop — designer and client take it together in real-time |

---

## Relationship to Other Specs

| Spec | Relationship |
|------|-------------|
| **LOG-DISC-001** (Discovery Engine) | The reasoning source — Workshop is the UX layer on the engine |
| **PROD-SCREEN-001** (Screen 3) | Workshop is one screen in the architecture |
| **PROD-JOURNEY-001** (Stage 3) | Workshop is one stage in the user journey |
| **RS-LIC-BS-003** (Target Audience) | Provides the Configuration framework used in Stage 2 |
| **RS-LIC-BS-004** (Brand Personality) | Provides the Personality method used in Stage 3 |

---

## The Hero Feature Principle

The Discovery Workshop embodies LogoMind's deepest insight:

> *Most designers struggle BEFORE sketching. Most AI tools help AFTER sketching starts. LogoMind enters at the beginning of the process — where the biggest pain exists.*

If LogoMind becomes successful, it will be because of the Discovery Workshop. Most AI tools assume the brief is complete. LogoMind helps create the brief when it isn't. That solves a problem thousands of logo designers face every day.

---

*LogoMind Principle: The Discovery Workshop is LogoMind's hero feature. It meets the confused client where they are, in whatever language they have, and helps them find strategic clarity they didn't know they had. The designer's strategic work becomes possible because of what the Workshop produces.*
