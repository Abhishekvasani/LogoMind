---
doc_id: LOG-DISC-001
title: LOGOS Discovery Engine v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
last_reviewed: 2026-07-14
---

# LOGOS Discovery Engine v1.0

> The Discovery Engine is arguably the most important engine in the system — **every decision downstream depends on it.** Its goal is not to ask questions, but to **reduce uncertainty before creativity begins** (CTO Decision #018).

---

## Mission

Transform a raw, often incomplete client brief into a rich understanding of the brand — so that every subsequent engine works from clarity, not assumption.

---

## The Core Insight

> **The problem is not that clients give bad briefs. The problem is that most clients are not branding experts.**

A client may know what they sell, but rarely how to express their brand strategically. If LogoMind expects a perfect brief, it fails in the real world. So the Discovery Engine **builds the brief when it isn't complete.**

---

## The Four Jobs

| Job | Purpose |
|-----|---------|
| **Detect** | Identify what is known and what is missing. |
| **Infer** | Reasonably fill gaps from context and industry knowledge. |
| **Prioritize** | Ask only the highest-impact missing questions. |
| **Measure** | Quantify brief quality (the Brand Confidence Score). |

---

## The Discovery Pyramid

The engine works from the foundation upward:

```
                  Vision & Differentiation
                         ↑
              Audience & Positioning
                         ↑
                Brand Personality
                         ↑
            Industry & Business Basics
```

Gaps at the base block everything above. The engine fills from the bottom up.

---

## Three Working Modes

Based on the **Brand Confidence Score**, the engine selects a mode:

| Brief Quality | Score | Mode | Behaviour |
|---------------|-------|------|-----------|
| **High** | 90–100% | **Expert Mode** | Proceed with full analysis; minimal questions. |
| **Medium** | 60–89% | **Guided Discovery** | Proceed, but ask a few high-impact questions. |
| **Low** | < 60% | **Brand Discovery Workshop** | Run an interactive workshop before any analysis. |

### Brand Discovery Workshop Stages

1. **Know Your Business** — name, industry, what they do, why they started.
2. **Know Your Customers** — who buys, what they care about.
3. **Discover Personality** — "If your brand walked into a room, how would people describe it?"
4. **Emotional Destination** — "How should someone feel immediately after seeing your logo?"
5. **Intent Extraction** — "I like gold." → "What about gold appeals to you?" → premium / luxury / success.
6. **Inspiration Without Copying** — analyse liked logos for *why* they appeal.
7. **What to Avoid** — "What should your brand never feel like?"

---

## The Missing Information Detector (CTO Proposal #004)

The engine never asks every possible question. It asks **only the most impactful missing questions.**

> Client says: "We manufacture furniture."
>
> Engine thinks: *This is enough to proceed, but I still don't know: premium or affordable? residential or commercial? handmade or mass-produced? modern or traditional?*

It surfaces only the questions whose answers would most change the creative direction.

---

## Intent Extraction Engine

Clients describe **solutions, not problems.** The Discovery Engine translates:

| Client Says | Engine Infers |
|-------------|---------------|
| "I want blue." | → "I want trust." |
| "I want a shield." | → "I want security." |
| "I want gold." | → "I want premium quality." |
| "I want a lion." | → "I want leadership." |
| "I want a circle." | → "I want unity." |

This distinguishes **preferences** from **intent** — and intent is what drives strategy.

---

## Curiosity Patterns

The engine asks questions in four patterns:

| Pattern | Example |
|---------|---------|
| **Clarify** | "When you say 'modern,' what specifically do you mean?" |
| **Compare** | "Of these five directions, which feels closest to your vision?" |
| **Prioritize** | "If you could only communicate one thing, what would it be?" |
| **Challenge** | "You requested a lion, but lions are overused in this industry. May I suggest alternatives?" |

---

## The Discovery Canvas

At the end of discovery, the engine produces a status table:

| Area | Status | Confidence |
|------|--------|------------|
| Industry & Business | ✅ Clear | High |
| Audience | ⚠️ Partial | Medium |
| Positioning | ❌ Missing | Low |
| Brand Purpose | ❌ Missing | Low |
| Personality | ✅ Clear | High |
| Competitors | ⚠️ Partial | Medium |
| Constraints | ✅ Clear | High |

This becomes the input to **LOGOS Strategy** (the Brand DNA Engine).

---

## The 5-Minute Rule (Product Law)

The Discovery Workshop must be completable in **10–15 minutes**. If it takes longer, the engine is asking low-impact questions and must be refined.

---

## Inputs & Outputs

| | |
|---|---|
| **Input** | Raw client brief (any completeness level) |
| **Output** | Discovery Summary, Brand Confidence Score, Brand DNA (draft) |
| **Knowledge Sources** | LMKC — Industry Intelligence, Brand Archetypes, Audience Psychology |
| **Quality Check** | Can LOGOS Strategy proceed with confidence > 70%? |

---

## Future Versions

- **Adaptive branching** — questions adapt based on previous answers.
- **Trend Intelligence Advisor** — integrated trend-awareness (currently a separate section).
- **Creative Compass** — strategic positioning scales (Traditional↔Modern, Minimal↔Detailed, etc.).
- **Creative Risk Meter** — Conservative / Balanced / Bold assessment.
