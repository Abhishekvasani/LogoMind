---
doc_id: LM-STD-004
title: Terminology Governance Standard
version: 1.0
status: Approved — Foundation Frozen
governance_level: L1 — Core Standard
governs: Canonical vocabulary across the repository
last_reviewed: 2026-07-14
---

# LM-STD-004 — Terminology Governance

> The repository's **Language Layer**. One word = one meaning. One concept = one canonical term. No synonyms wandering the knowledge base.

---

## 1. Purpose

If "brand," "identity," and "logo" are used interchangeably, reasoning becomes unreliable. LogoMind maintains a canonical vocabulary so that every knowledge object, every engine, and every recommendation speaks the same precise language.

---

## 2. Governance Principles

1. **One canonical definition per concept.** The first place a term is defined becomes its canonical source.
2. **Concepts are separated from implementations.** "Meaning" (the concept) is defined once; how it is applied varies.
3. **Canonical definitions are Repository Assets.** They are versioned, reviewed, and protected.
4. **Contextual definitions are allowed but must reference the canonical one.**

---

## 3. Canonical Vocabulary v1.0

| Term ID | Term | Canonical Definition | Stability |
|---------|------|----------------------|-----------|
| TERM-001 | **Meaning** | The significance a brand carries in the minds of its audience — what the identity is understood to stand for. | Stable |
| TERM-002 | **Purpose** | The reason an organisation exists beyond profit; the problem it exists to solve. | Stable |
| TERM-003 | **Identity** | The total way an organisation is recognised — strategic, verbal, and visual. | Stable |
| TERM-004 | **Visual Identity** | The visible expression of identity — logo, colour, typography, composition, and their system. | Stable |
| TERM-005 | **Logo** | The primary mark of a visual identity; the single most condensed visual representation of a brand. | Stable |
| TERM-006 | **Symbol** | A form (object, shape, or abstract mark) that represents an idea beyond its literal appearance. | Stable |
| TERM-007 | **Brand** | The total perception of an organisation held by its audience — built through every interaction over time. | Stable |
| TERM-008 | **Communication** | The act of conveying meaning from brand to audience through visual, verbal, and experiential channels. | Stable |
| TERM-009 | **Recognition** | The audience's ability to identify a brand from its visual cues without additional context. | Stable |
| TERM-010 | **Perception** | The meaning the audience constructs in their own mind — which may differ from the intended meaning. | Stable |

---

## 4. Definition Standards

Every canonical definition must be:

- **Stable** — independent of trends or tools.
- **Precise** — distinguishes the concept from its neighbours.
- **Operational** — usable in reasoning, not merely descriptive.
- **Layered** — one canonical definition, with contextual notes where needed.

---

## 5. Stability Levels

| Level | Meaning | Change Policy |
|-------|---------|---------------|
| **Stable** | Foundational; unlikely to change. | Change requires strong evidence and Founder approval. |
| **Managed** | Established but may evolve with the discipline. | Change requires CTO review. |
| **Emerging** | New or contested; expected to refine. | Change is normal; tracked in Evolution Log. |

---

## 6. Canonical Definition Rules

1. **Never redefine a canonical term inside an LIC.** LICs use terms; they do not redefine them.
2. **Never use two terms for the same concept.** If a synonym appears, it points to the canonical term.
3. **Definitions are trend-independent.** "A logo is..." must be as true in 2050 as in 2026.
4. **Knowledge Integrity Rule:** The terms Meaning, Purpose, Identity, Brand, and Logo must never be redefined by downstream content.

---

## 7. Cross-Reference Policy

When a term is used in an LIC, it links to its canonical definition (TERM-XXX). This ensures a reader can always trace a word to its authoritative source.

---

## Relationship to Other Standards

- **LM-STD-002** (Statement Taxonomy) relies on canonical terms to build precise statements.
- **LM-STD-003** (Confidence) applies to the *claims* made using these terms.
- **LM-STD-005** (Knowledge Layering) determines *where* each term is introduced.
- **LM-STD-006** (Quality Review) audits terminology consistency.
