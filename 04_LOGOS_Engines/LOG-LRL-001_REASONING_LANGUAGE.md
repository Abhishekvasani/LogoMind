---
doc_id: LOG-LRL-001
title: LogoMind Reasoning Language (LRL) v1.0
version: 1.0
status: Approved — Permanent Intellectual Property
governance_level: L2 — Engine Specification
last_reviewed: 2026-07-14
---

# LogoMind Reasoning Language (LRL) v1.0

> LRL is **proprietary intellectual property**. It is a structured vocabulary that makes LOGOS's reasoning explicit, traceable, and machine-readable. It is model-independent — it works regardless of which AI model powers the system.

---

## Purpose

Most AI tools produce answers. LOGOS produces **reasoning paths**. LRL is the language those paths are written in. It ensures every recommendation can be traced from raw fact through interpretation to final advice.

---

## The Nine-Term Core Vocabulary

| Term | Meaning | Example |
|------|---------|---------|
| **FACT** | An established, verifiable piece of knowledge. | "Circles have no corners." |
| **ASSUMPTION** | Something taken as true without verification. | "The target audience is 25–40." |
| **HYPOTHESIS** | A testable proposal. | "An abstract mark may differentiate better than a literal one here." |
| **INSIGHT** | A non-obvious understanding drawn from facts + interpretation. | "This brand's real differentiator is precision, not speed." |
| **OPPORTUNITY** | A strategic opening identified by reasoning. | "No competitor uses negative space — it's available." |
| **CONSTRAINT** | A limitation that shapes the solution. | "The mark must work embroidered at 2cm." |
| **RISK** | A potential weakness or failure mode. | "The shield symbol is overused in this industry." |
| **RECOMMENDATION** | A advised direction, with reasoning attached. | "Use a keystone form — it signals stability without the cliché of a shield." |
| **RATIONALE** | The reasoning chain supporting a recommendation. | "Keystone → stability → trust → banking audience → differentiator." |

---

## The Reasoning Chain

```
FACT
  ↓ (combined with)
ASSUMPTION / HYPOTHESIS
  ↓ (produces)
INSIGHT
  ↓ (reveals)
OPPORTUNITY
  ↓ (constrained by)
CONSTRAINT
  ↓ (evaluated against)
RISK
  ↓ (leads to)
RECOMMENDATION
  ↓ (supported by)
RATIONALE
```

---

## Worked Example

**Brief:** A construction company called NovaBuild.

| Step | Term | Content |
|------|------|---------|
| 1 | FACT | Construction logos commonly use shields, hammers, and buildings. |
| 2 | ASSUMPTION | The client wants to communicate trust and strength. |
| 3 | HYPOTHESIS | An abstract geometry may communicate strength more originally than a literal shield. |
| 4 | INSIGHT | NovaBuild's real differentiator is precision engineering, not raw strength. |
| 5 | OPPORTUNITY | No competitor in their segment uses a keystone or compass form. |
| 6 | CONSTRAINT | The mark must work on hard-hat embroidery and site signage. |
| 7 | RISK | A keystone could be confused with architecture-only firms. |
| 8 | RECOMMENDATION | Explore a keystone + N monogram with clean geometry. |
| 9 | RATIONALE | Keystone signals stability (trust); the N integrates the name; clean geometry signals precision (the true differentiator); works at small scale; avoids the overused shield. |

---

## The Three Dimensions of Every Statement

Every LRL statement carries three dimensions (CTO Decision #021):

1. **Reasoning Type** — Which of the nine terms it is.
2. **Confidence** — How strongly supported (per LM-STD-003).
3. **Evidence Source** — Where the support comes from.

---

## The Evidence Layer

| Source Type | Weight |
|-------------|--------|
| **Established Evidence** | Documented, verifiable, cross-cultural. |
| **Professional Consensus** | Broad agreement among experienced practitioners. |
| **LogoMind Interpretation** | LogoMind's own synthesis — clearly labelled as such. |
| **Open Question** | Unresolved; presented honestly as evolving. |

Evidence is always **separated from interpretation** (LM-STD-002).

---

## Two Reasoning Modes (CTO Decision #022)

| Mode | Default? | What it shows |
|------|----------|---------------|
| **Designer Mode** | ✅ Yes | The recommendation and a concise rationale. Reduced cognitive load. |
| **Expert Mode** | No (on demand) | The full reasoning chain — facts, assumptions, hypotheses, risks. For experienced designers who want depth. |

This implements **Progressive Disclosure** (FD-008): simple by default, powerful on demand.

---

## Three Reasoning Zones

| Zone | Content |
|------|---------|
| **Knowledge Zone** | Facts and established principles (drawn from LMKC). |
| **Interpretation Zone** | Insights, opportunities, hypotheses (LOGOS reasoning). |
| **Decision Zone** | Recommendations, constraints, risks (actionable output). |

LRL keeps these zones distinct so the reader always knows whether they are looking at *what is known*, *what LOGOS infers*, or *what is recommended*.

---

## Reserved for v1.1

**TRADE-OFF** — A formal term for explicitly stating what is gained and lost in a recommendation. To be added when the framework has enough production use to define it precisely.
