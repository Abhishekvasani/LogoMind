---
doc_id: PROD-BACKLOG-001
title: LogoMind Feature Backlog
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-07-17
related:
  - PROD-VISION-001 Product Vision
  - PROD-PERSONA-001 User Personas
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-BACKLOG-001 — Feature Backlog

> *Every feature in this backlog has passed the Five Questions Framework (FD-010) and the LogoMind Decision Filter. Features that fail either are not here — no matter how impressive they sound.*

---

## Overview

The backlog is organised by release priority:

| Priority | Meaning | Release |
|----------|---------|---------|
| 🔴 **Must Have** | The product does not function without these | v1.0 (MVP) |
| 🟠 **Should Have** | High value; included if feasible | v1.0 or v1.1 |
| 🟡 **Nice to Have** | Valuable but not essential | v1.5 or v2.0 |
| 🔵 **Future** | Long-term vision | v2.0+ |

Every feature is mapped to the persona it primarily serves and the engine/screen it depends on.

---

## 🔴 Must Have — v1.0 (Minimum Lovable Product)

These features are required for LogoMind to deliver its core promise. Without them, the product is not LogoMind.

| # | Feature | Persona | Engine / Screen | Notes |
|---|---------|---------|-----------------|-------|
| 1 | **Project creation** (Company Name + Industry + Brief) | All | Screen 2 | The entry point |
| 2 | **Brief analysis** (Brand Confidence Score + Missing Info) | All | LOG-DISC-001 | The Discovery Engine's core |
| 3 | **Guided Discovery** (3–5 high-impact questions) | Maya | LOG-DISC-001 | For briefs at 60–89% |
| 4 | **Discovery Workshop** (7-stage interactive) | Maya, Elena | LOG-DISC-001 + PROD-DW-001 | **The hero feature** |
| 5 | **Workshop link sharing** (client takes it independently) | Maya, Elena | LOG-DISC-001 | Sends link; results sync |
| 6 | **Brand DNA generation** (the 6 strands) | All | LOG-STRAT-001 | The Strategy Engine output |
| 7 | **Brand DNA editing** (Maya can refine) | Maya | Screen 4 | She knows the client |
| 8 | **Contradiction flagging** (never silently resolved) | All | LOG-STRAT-001 | Intellectual honesty |
| 9 | **Insight Report** (industry + competitors + clichés) | All | LOG-INSIGHT-001 | Category awareness |
| 10 | **Cliché Avoidance Report** | All | LOG-INSIGHT-001 | Prevents unoriginal work |
| 11 | **Concept Family generation** (3–5 territories) | All | LOG-CREATE-001 | **The signature output** |
| 12 | **Creative Council assessment** (9 minds) | All | LOG-CC-001 + LOG-JUDGE-001 | Qualitative evaluation |
| 13 | **Design Jury scoring** (10 dimensions + reasoning) | All | LOG-JUDGE-001 | Quantitative evaluation |
| 14 | **Concept DNA fingerprint** (per concept) | All | LOG-JUDGE-001 | Objective comparison |
| 15 | **SSB generation** (7 sections) | All | PROD-SSB-001 + SSB Composer | **The flagship output** |
| 16 | **SSB export** (PDF, Markdown) | All | Screen 7 | For sharing, printing |
| 17 | **Sketch upload + Coach critique** (conversational) | Maya | LOG-COACH-001 + Screen 7 | Iterative refinement |
| 18 | **Confidence levels visible** (everywhere) | All | LM-STD-003 | Intellectual honesty |
| 19 | **Progressive Disclosure** (Layer A default) | All | LM-STD-005 | Simple by default |
| 20 | **Project save/resume** (across sessions) | All | Application Layer | Persistence |
| 21 | **Dashboard** (project list + new project) | All | Screen 1 | Navigation |
| 22 | **User accounts** (basic auth) | All | Application Layer | Identity |
| 23 | **Creative Director Mode** (respectful challenge) | All | LOG-CREATE-001 | Signature behaviour |

**23 Must-Have features.** This is the MVP. Everything else can wait.

---

## 🟠 Should Have — v1.0 or v1.1

High value; included if feasible in v1, otherwise in the first update.

| # | Feature | Persona | Engine / Screen | Notes |
|---|---------|---------|-----------------|-------|
| 24 | **Presentation generation** (10-section deck) | Maya | LOG-PRESENT-001 + Screen 8 | Major value; may be v1.1 |
| 25 | **Presentation export** (PDF, Keynote, share link) | Maya | Screen 8 | Depends on #24 |
| 26 | **Objection-handling notes** (for designer only) | Maya | LOG-PRESENT-001 | Presentation appendix |
| 27 | **Trend Intelligence Advisor** (context-aware trends) | All | LOG-INSIGHT-001 | The Trend Taxonomy in action |
| 28 | **Trend vs Timeless Meter** (visual recommendation) | All | LOG-INSIGHT-001 | Glanceable strategic guidance |
| 29 | **Inspiration Mode** (5 brand territories for thin briefs) | Elena | LOG-DISC-001 | When even Workshop can't start |
| 30 | **Intent Extraction display** (show extracted intents) | All | LOG-DISC-001 | Transparency |
| 31 | **Multiple Concept Family comparison** | All | Screen 6 | Side-by-side |
| 32 | **SSB in-app interactive view** (expandable layers) | All | Screen 7 | Richer than PDF |
| 33 | **LIC library access** (browse the knowledge base) | Maya, Elena | Future screen | Educational layer |
| 34 | **Sketch iteration history** (track versions) | Maya | Screen 7 | Iteration visibility |

---

## 🟡 Nice to Have — v1.5 or v2.0

Valuable for growth and retention, but not required for launch.

| # | Feature | Persona | Notes |
|---|---------|---------|-------|
| 35 | **Team collaboration** (shared projects) | Marcus | Studio workflow |
| 36 | **Project history & insights** (cross-project patterns) | Marcus | Strategic learning |
| 37 | **Brand Guidelines generator** (from final concept) | Maya, Marcus | Post-presentation deliverable |
| 38 | **Mood Board Builder** | Maya | Visual reference collection |
| 39 | **Sketch Coach full canvas** (in-app sketching) | Maya | If we build our own canvas |
| 40 | **Adaptive Workshop** (questions adapt to answers) | All | Smarter branching |
| 41 | **Workshop analytics** (show where client hesitated) | Maya | Diagnostic data |
| 42 | **Comparison view** (two SSBs side-by-side) | Marcus | Portfolio review |
| 43 | **Custom LMKC additions** (studio's own knowledge) | Marcus | Studio-specific knowledge |
| 44 | **Export to Figma/Illustrator** (handoff) | Maya | Workflow integration |
| 45 | **Mobile companion** (review SSB on phone) | All | On-the-go access |
| 46 | **API access** (for advanced users) | Marcus | Integration |

---

## 🔵 Future — v2.0+ (LogoMind OS)

The long-term vision — multiple products on the same Intelligence Core.

| # | Feature | Notes |
|---|---------|-------|
| 47 | **Brand Strategist module** | Full strategy consulting workflow |
| 48 | **Naming Assistant** | Brand name generation (uses same strategic foundation) |
| 49 | **Tagline Generator** | Taglines from Brand DNA |
| 50 | **Packaging Strategy** | Extends identity to packaging |
| 51 | **Social Identity Planner** | Social media visual planning |
| 52 | **Pitch Presentation Builder** | Investor / stakeholder pitches |
| 53 | **Design Mentor** (conversational) | LOGOS asks questions; designer learns |
| 54 | **Creative Knowledge Academy** | Structured learning from LICs |
| 55 | **Adobe / Figma plugins** | Direct integration with design tools |
| 56 | **Logo testing suite** | Test concepts with real audiences |
| 57 | **Trademark awareness** (informational) | Conflict detection (not legal advice) |
| 58 | **Multi-language Workshop** | Adaptive to client's native language |
| 59 | **Video/voice Workshop** | Client speaks; LogoMind transcribes |
| 60 | **Live Workshop** (designer + client real-time) | Synchronous collaboration |

---

## Backlog Governance

### Admission Criteria (the Five Questions Framework, FD-010)

Every feature must answer all five before entering the backlog:

1. **Does it solve a real problem that designers face?**
2. **Does it fit our philosophy of helping designers think better?**
3. **Can we explain its value in one sentence?**
4. **What are the risks?**
5. **If we launched this to 100,000 designers tomorrow, would we still be proud of it?**

If any answer is *no*, the feature does not enter the backlog.

### The LogoMind Decision Filter (Constitution)

Additionally, every feature must pass:

1. Does it improve a designer's thinking?
2. Will it still make sense in 10 years?
3. Can we explain it in one sentence?
4. Does it respect the designer's creativity?
5. Would we proudly demo it to the world's best designers?

### What's NOT in the Backlog (and Why)

| Excluded Feature | Why Excluded |
|------------------|--------------|
| Logo generation | Violates Product Promise (FD-005) |
| "Generate 100 options" | LogoMind generates Concept Families (3–5), not spam |
| AI makes the creative decision | Violates Product Promise |
| Automated trademark filing | Out of scope; not legal advice |
| Trend-chasing dashboard | Trends are context, not a standalone tool |
| Mass-market "logo in 60 seconds" | Wrong audience (anti-persona) |
| Generic stock symbol library | LogoMind reasons about symbols; doesn't dispense them |

---

## Priority Rationale

### Why these 23 are Must-Have

The 23 Must-Have features form the complete LOGOS pipeline — from brief to SSB. Without any one of them, the pipeline breaks:
- Without Brief Analysis (#2), there's no Discovery
- Without Brand DNA (#6), there's no Strategy
- Without Concept Families (#11), there's no Create
- Without SSB (#15), there's no flagship output
- Without Confidence Levels (#18), there's no intellectual honesty

Every Must-Have feature is necessary. Every non-Must-Have is not.

### Why the SSB and Workshop are non-negotiable

The **Discovery Workshop (#4)** and **SSB (#15)** are LogoMind's defining features. They are the two things no competitor does. If v1.0 ships without either, it is not LogoMind — it is a generic AI design assistant.

### Why Presentation (#24) is Should-Have, not Must

The Presentation Builder is enormously valuable, but LogoMind can launch without it — designers can build presentations themselves from the SSB. Better to ship the core pipeline excellent than the full pipeline mediocre.

---

## Dependencies

Key feature dependencies:

```
Brief Analysis (#2) → Guided Discovery (#3) / Workshop (#4)
                            ↓
                    Brand DNA (#6)
                            ↓
                    Insight Report (#9)
                            ↓
                  Concept Families (#11)
                            ↓
                  Creative Council (#12)
                  + Jury Scoring (#13)
                            ↓
                       SSB (#15)
                            ↓
                Sketch Upload + Coach (#17)
                            ↓
                Presentation (#24) [Should Have]
```

The critical path runs from Brief Analysis to SSB. Every Must-Have is on this path.

---

## Estimated Effort (Rough)

For Phase 5 (Technical Build) planning — rough order of magnitude:

| Phase | Effort | Features |
|-------|--------|----------|
| **MVP Foundation** | Large | #1, 2, 20, 21, 22 (project mgmt, auth, dashboard) |
| **Discovery** | Large | #3, 4, 5, 29, 30 (the Workshop is substantial) |
| **Strategy** | Medium | #6, 7, 8 (Brand DNA generation + editing) |
| **Insight** | Medium | #9, 10, 27, 28 (research + trends) |
| **Create + Judge** | Large | #11, 12, 13, 14, 23, 31 (Concept Families + evaluation) |
| **SSB** | Medium | #15, 16, 32 (flagship output) |
| **Sketch Coach** | Medium | #17, 34 (conversational guidance) |
| **Cross-Cutting** | Medium | #18, 19 (confidence + progressive disclosure everywhere) |

Total: a substantial build, but well-scoped. The Intelligence Core (Phase 3) does the heavy reasoning; Phase 5 is largely about exposing it through clean UX.

---

*LogoMind Principle: Every feature must earn its place. The Five Questions Framework and the Decision Filter keep the backlog disciplined. A product with a hundred features is not better than one with twenty-three — if those twenty-three are the right ones.*
