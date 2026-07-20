---
doc_id: PROD-SCREEN-001
title: LogoMind Screen Architecture
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-07-17
related:
  - PROD-VISION-001 Product Vision
  - PROD-JOURNEY-001 User Journey
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-SCREEN-001 — Screen Architecture

> *Every major screen in LogoMind has a single responsibility. No screen tries to do two things. This is the principle that keeps the product clean as it grows (CTO Decision #017: One Screen. One Purpose.).*

---

## 1. The Screen Inventory

LogoMind has **eight major screens** in v1. Each has a single responsibility and a single primary action.

| # | Screen | Single Responsibility | Primary Action |
|---|--------|----------------------|----------------|
| 1 | **Dashboard** | Show projects; start new ones | "+ New Project" |
| 2 | **New Project** | Capture the brief | "Analyze Project" |
| 3 | **Discovery Workshop** | Build the brief when incomplete | "Complete Workshop" |
| 4 | **Strategy View** | Display and refine Brand DNA | "Approve Brand DNA" |
| 5 | **Insight View** | Display category research | "Continue to Create" |
| 6 | **Concept Families** | Display generated creative territories | "Select Family" |
| 7 | **SSB + Sketch Workspace** | Deliver the brief; receive sketches | "Request Presentation" / "Upload Sketch" |
| 8 | **Presentation View** | Deliver the client deck | "Export Presentation" |

A 9th screen — **Judge Report** — appears as a tab within the Concept Families screen rather than as a separate screen, because evaluation and selection happen together.

---

## 2. Screen 1 — Dashboard

### Responsibility
*Show projects; start new ones.*

### Layout
```
┌────────────────────────────────────────────────┐
│  LOGOMIND                  Maya  ·  Settings    │
├────────────────────────────────────────────────┤
│                                                 │
│  + New Project                                  │
│                                                 │
│  RECENT PROJECTS                                │
│  ┌────────┐ ┌────────┐ ┌────────┐               │
│  │ North- │ │ Eco-   │ │ Studio │               │
│  │ bridge │ │ Logic  │ │ Forma  │               │
│  │ Coffee │ │ Tech   │ │        │               │
│  │ Phase: │ │ Phase: │ │ Phase: │               │
│  │ Sketch │ │ Discov.│ │ Pres.  │               │
│  └────────┘ └────────┘ └────────┘               │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Elements
- LogoMind wordmark (top left)
- User menu (top right)
- Large "+ New Project" CTA
- Recent project cards showing: name, client, current phase, last edited
- Search (future)

### What It Does NOT Have
- No design tools (those are external — Figma, Illustrator)
- No "generate logo" button (violates Product Promise)
- No tutorials or marketing (those live on the marketing site, separate)

---

## 3. Screen 2 — New Project

### Responsibility
*Capture the brief.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back to Dashboard                            │
├────────────────────────────────────────────────┤
│                                                 │
│  NEW PROJECT                                    │
│                                                 │
│  Company Name                                   │
│  [___________________________________]          │
│                                                 │
│  Industry                                       │
│  [___________________________________]          │
│                                                 │
│  Client Brief                                   │
│  Paste whatever you have — even one sentence.   │
│  LogoMind will work with it.                    │
│  [___________________________________]          │
│  [___________________________________]          │
│  [___________________________________]          │
│  [___________________________________]          │
│                                                 │
│  Client Contact (optional — for Workshop link)  │
│  [___________________________________]          │
│                                                 │
│              [ Analyze Project → ]              │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Minimal friction.** Only Company Name, Industry, and Brief are required.
- **Brief tolerance.** The form explicitly says "even one sentence" — lowering the barrier.
- **No 50-field intake.** The Discovery Engine extracts the rest through reasoning or workshop.

### What Happens on Submit
- LogoMind transitions to a "thinking" state
- Discovery Engine analyses the brief (~30–60 seconds)
- Routes to Screen 3 (Workshop) or Screen 4 (Strategy) based on Brand Confidence Score

---

## 4. Screen 3 — Discovery Workshop

### Responsibility
*Build the brief when incomplete.*

### Layout (Workshop Mode)
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Workshop     │
├────────────────────────────────────────────────┤
│                                                 │
│  Stage 3 of 7: Discover Personality             │
│  ████████████░░░░░░░░░  Progress                │
│  ~8 minutes remaining                           │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │  If your brand walked into a room,      │   │
│  │  how would people describe it?          │   │
│  │                                          │   │
│  │  [ Elegant ]  [ Bold ]  [ Friendly ]    │   │
│  │  [ Intelligent ] [ Adventurous ]        │   │
│  │  [ Traditional ] [ Premium ]            │   │
│  │  [ Playful ]                            │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Why did you choose those? (Optional)           │
│  [___________________________________]          │
│                                                 │
│              [ Continue → ]                     │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **One question at a time.** Never overwhelm.
- **Card-based choices.** Easier than open fields for confused clients.
- **Progress visible.** Always show how far through and time remaining.
- **Optional explanations.** Clients can say as much or as little as they want.
- **Intent Extraction active.** When client says "I like gold," a follow-up probes "What about gold?"

### Three Modes (per Discovery Engine)
- **Guided Discovery** (Brief Score 60–89%): 3–5 high-impact questions only. Maya answers herself.
- **Workshop Mode** (Brief Score < 60%): Full 7-stage workshop. Can be run with client (via link) or by Maya as interview.
- **Inspiration Mode** (Brief extremely thin): LogoMind proposes 5 possible brand territories; client chooses.

(Full UX specification in PROD-DW-001.)

---

## 5. Screen 4 — Strategy View

### Responsibility
*Display and refine Brand DNA.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Strategy     │
├────────────────────────────────────────────────┤
│                                                 │
│  BRAND DNA                            [Edit]    │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ PURPOSE                                 │   │
│  │ Return something real to a neighbourhood │   │
│  │ that has lost it.                       │   │
│  │ Confidence: 🟢 C4  [Why?]               │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ POSITIONING                             │   │
│  │ For urban professionals who want...     │   │
│  │ [full positioning statement]            │   │
│  │ Confidence: 🟢 C4  [Why?]               │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ ⚠ CONTRADICTION FLAGGED                 │   │
│  │ "Premium" positioning conflicts with    │   │
│  │ "Accessible" audience configuration.    │   │
│  │ [Resolve →]                             │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│           [ Approve Brand DNA → ]               │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Each element in its own card** — clear separation.
- **Confidence visible per element** (per LM-STD-003) — never fake certainty.
- **Contradictions surfaced, never silently resolved** — Maya decides.
- **Editable** — Maya knows the client; LogoMind doesn't.

---

## 6. Screen 5 — Insight View

### Responsibility
*Display category research.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Insight      │
├────────────────────────────────────────────────┤
│                                                 │
│  INDUSTRY: Coffee (Independent Roasters)        │
│                                                 │
│  ┌──────────────────┐  ┌──────────────────┐    │
│  │ CLICHÉS TO AVOID │  │ OPPORTUNITIES    │    │
│  │                  │  │                  │    │
│  │ · Coffee bean    │  │ · Negative space │    │
│  │ · Steam swirl    │  │ · Letter-based   │    │
│  │ · Cup silhouette │  │ · Abstract warmth│    │
│  │ · Brown palette  │  │ · Craft signals  │    │
│  │   (overused)     │  │                  │    │
│  └──────────────────┘  └──────────────────┘    │
│                                                 │
│  COMPETITOR MAP                                 │
│  [visual grid of competitors with identities]   │
│                                                 │
│  TREND INTELLIGENCE                             │
│  Timeless ◄━━━━━━━━━●━━━━━► Trend-forward      │
│                    85% / 15%                    │
│  Recommended for: Heritage craft brand          │
│                                                 │
│         [ Continue to Create → ]                │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Scannable, not dense.** Insights should be quick to absorb.
- **Action-oriented.** Every insight points to a "what to do" — not just "what is."
- **Trend Meter visual.** The Trend vs Timeless balance is a glanceable indicator.

---

## 7. Screen 6 — Concept Families

### Responsibility
*Display generated creative territories; let Maya choose.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Create       │
├────────────────────────────────────────────────┤
│                                                 │
│  CONCEPT FAMILIES                               │
│                                                 │
│  ┌────────────────────┐ ┌────────────────────┐ │
│  │ FAMILY A           │ │ FAMILY B           │ │
│  │ Craft & Process    │ │ Community &        │ │
│  │                    │ │ Connection         │ │
│  │ Symbols:           │ │                    │ │
│  │ · Hand-formed      │ │ Symbols:           │ │
│  │   curves           │ │ · Linked circles   │ │
│  │ · Pour geometry    │ │ · Negative space   │ │
│  │ · Roast gradient   │ │   forming N        │ │
│  │                    │ │ · Conversation     │ │
│  │ Why it works:      │ │   mark             │ │
│  │ <reasoning>        │ │                    │ │
│  │                    │ │ Why it works:      │ │
│  │ Council: 8/9       │ │ <reasoning>        │ │
│  │ Confidence: 🟢 C4  │ │                    │ │
│  │                    │ │ Council: 7/9       │ │
│  │ [Select Family]    │ │ Confidence: 🔵 C3  │ │
│  └────────────────────┘ └────────────────────┘ │
│                                                 │
│  ┌────────────────────┐ ┌────────────────────┐ │
│  │ FAMILY C           │ │ FAMILY D           │ │
│  │ [details...]       │ │ [details...]       │ │
│  └────────────────────┘ └────────────────────┘ │
│                                                 │
│  💡 Creative Director Note:                     │
│  "Client requested a coffee bean. That symbol   │
│  is overused in this category. Family A's       │
│  'pour geometry' carries the meaning of craft   │
│  more originally."                              │
│                                                 │
│         [ Continue to Judge → ]                 │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Family cards** — each is a strategic territory, not a single idea.
- **Side-by-side comparison** — easy to scan.
- **Creative Director Notes** — surface LogoMind's strategic challenges to weak client requests.
- **Council + Confidence** visible per family.
- **Judge Report** appears as a tab when families are selected for evaluation.

---

## 8. Screen 7 — SSB + Sketch Workspace

### Responsibility
*Deliver the brief; receive sketches for critique.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Sketch Brief  │
├────────────────────────────────────────────────┤
│                                                 │
│  ┌─────────────────────┐  ┌─────────────────┐  │
│  │ STRATEGIC SKETCH    │  │ SKETCH WORKSPACE │  │
│  │ BRIEF               │  │                  │  │
│  │                     │  │ [Upload Sketch]  │  │
│  │ 1. Project Essence  │  │                  │  │
│  │ <text>              │  │ Sketch 1:        │  │
│  │                     │  │ [thumbnail]      │  │
│  │ 2. Brand DNA        │  │ Coach: "Try..."  │  │
│  │ Snapshot            │  │                  │  │
│  │ <text>              │  │ Sketch 2:        │  │
│  │                     │  │ [thumbnail]      │  │
│  │ 3. Creative North   │  │ Coach: "..."     │  │
│  │ Star                │  │                  │  │
│  │ <text>              │  │ [Upload Sketch]  │  │
│  │                     │  │                  │  │
│  │ [Full SSB view]     │  │                  │  │
│  │ [Export SSB]        │  │                  │  │
│  └─────────────────────┘  └─────────────────┘  │
│                                                 │
│    [ Request Presentation → ]                   │
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Two-column layout.** Brief on the left (reference); sketch workspace on the right (work).
- **Brief is always visible** while sketching.
- **Sketch Coach is conversational** — appears under each uploaded sketch.
- **Export SSB** — for designers who sketch outside LogoMind (most will).

---

## 9. Screen 8 — Presentation View

### Responsibility
*Deliver the client-ready presentation.*

### Layout
```
┌────────────────────────────────────────────────┐
│  ← Back  ·  Northbridge Coffee  ·  Presentation │
├────────────────────────────────────────────────┤
│                                                 │
│  CLIENT PRESENTATION                            │
│                                                 │
│  ┌─────────────────────────────────────────┐   │
│  │ [Slide 1 of 10 — Cover]                 │   │
│  │                                          │   │
│  │ Northbridge Coffee                      │   │
│  │ Identity System — Strategic Presentation│   │
│  │                                          │   │
│  │ ← Prev          1 / 10          Next →   │   │
│  └─────────────────────────────────────────┘   │
│                                                 │
│  Sections:                                      │
│  1. Cover                                       │
│  2. Executive Summary                           │
│  3. Brand Foundation                            │
│  4. Strategic Exploration                       │
│  5. The Chosen Concept                          │
│  6. Design Rationale                            │
│  7. Applications                                │
│  8. Future-Proofing                             │
│  9. Brand Guidelines Summary                    │
│  10. Q&A Preparation                            │
│                                                 │
│  OBJECTION-HANDLING NOTES (for designer only)   │
│  · "Too simple" → Reduction Sequence reasoning  │
│  · "Add [X]" → Simplicity defence               │
│  · "I prefer [competitor]" → Differentiation    │
│                                                 │
│  [ Export PDF ] [ Export Keynote ] [ Share Link]│
│                                                 │
└────────────────────────────────────────────────┘
```

### Key Principles
- **Slide-by-slide navigation** with overview.
- **Objection-handling notes** — for designer only; not in client export.
- **Multiple export formats** — PDF, Keynote, shareable link.

---

## 10. Cross-Screen Principles

These apply to every screen:

| Principle | Application |
|-----------|-------------|
| **One Screen, One Purpose** | Each screen has a single responsibility and a single primary action |
| **Engines Invisible** | Maya never sees "running the Strategy Engine" — she sees a brand becoming clear |
| **Confidence Visible** | Every claim shows its confidence level (LM-STD-003) |
| **Contradictions Surfaced** | Never silently resolved; always flagged for Maya's decision |
| **Progressive Disclosure** | Layer A (essence) by default; deeper layers on demand |
| **Edit Where It Matters** | Strategic elements (Brand DNA, Concept Families) are editable; engine internals are not |
| **Tangible Output Per Stage** | Every stage produces something Maya can see, share, or act on |

---

## 11. Screen Flow

```
Dashboard → New Project → [Discovery Workshop] → Strategy → Insight
                              (if needed)
                                                              ↓
                                                          Concept
                                                          Families
                                                              ↓
                                                          SSB +
                                                          Sketch
                                                              ↓
                                                          Presentation
                                                              ↓
                                                          Dashboard
```

Note: Maya can always go back to a previous screen to review or refine. The flow is linear by default but revisitable. Nothing is locked.

---

## 12. What's NOT a Screen

To maintain screen discipline, these are explicitly **not screens** in v1:

| Non-Screen | Why |
|-----------|-----|
| **Logo generator** | Violates Product Promise |
| **Symbol library browser** | LogoMind reasons about symbols; doesn't dispense them |
| **Trend tracker dashboard** | Trends are context (Insight View); not a standalone tool |
| **Brand guidelines editor** | Future v2; v1 produces a summary only |
| **Team management console** | Future v2 (Marcus's persona) |
| **Course/academy** | Future; the LICs are educational artefacts but not a course UI |

---

## 13. Future Screens (v2+)

| Screen | Persona | Priority |
|--------|---------|----------|
| Team Dashboard | Marcus | v2 |
| Brand Guidelines Editor | Maya, Marcus | v2 |
| Mood Board Builder | Maya | v2 |
| Project History & Insights | Marcus | v2 |
| Sketch Coach (full canvas) | Maya | v2 (v1 is conversational upload only) |

---

*LogoMind Principle: Every screen has a single responsibility and a single primary action. Complexity emerges from the journey across screens — never from cramming multiple purposes into one screen.*
