---
doc_id: LM-STD-002
title: Statement Taxonomy Standard
version: 1.0
status: Approved — Foundation Frozen
governance_level: L1 — Core Standard
governs: How statements are classified within knowledge artifacts
last_reviewed: 2026-07-14
---

# LM-STD-002 — Statement Taxonomy

> The repository's **Logic Layer**. Every statement in LogoMind must declare what kind of statement it is, so that reasoning is transparent and auditable.

---

## 1. Purpose

LogoMind teaches reasoning, not just conclusions. To do that, every statement must be *classifiable* — the reader must know whether they are reading a fact, a principle, an opinion, or an open question.

---

## 2. The Ten Canonical Statement Types

| Type | Purpose | Question Answered | Authority Level |
|------|---------|-------------------|-----------------|
| **Definition** | Establishes what a concept is | "What is this?" | Canonical |
| **Principle** | States a fundamental truth of the discipline | "What always holds?" | High |
| **Observation** | Reports a pattern noticed in practice | "What tends to happen?" | Professional |
| **Guideline** | Offers practical direction | "What should I usually do?" | Professional |
| **Framework** | Provides a structured way to think | "How do I structure this?" | Professional |
| **Method** | Describes a repeatable procedure | "How do I execute this step by step?" | Professional |
| **Evidence** | Cites support for a claim | "What supports this?" | Established |
| **Interpretation** | Applies knowledge to a specific case | "What does this mean here?" | Contextual |
| **Reflection** | Invites the designer to think | "What should I question?" | Invitational |
| **Open Question** | Marks an unresolved issue | "What don't we know yet?" | Exploratory |

---

## 3. Statement Hierarchy

```
Definition  (what is true)
    ↓
Principle   (what always holds)
    ↓
Framework   (how to structure thinking)
    ↓
Method      (how to execute)
    ↓
Guideline   (what usually works)
    ↓
Observation (what tends to happen)
    ↓
Interpretation (what it means here)
```

A Definition can never be contradicted by an Observation. A Principle outranks a Guideline.

---

## 4. Editorial Rules

1. **Never present an interpretation as a definition.**
2. **Never present an observation as a principle.**
3. **Every claim has a type — if the type is unclear, the statement is unclear.**
4. **Open Questions must be visibly marked** — they are not weaknesses; they are intellectual honesty.
5. **Reflections must not contain hidden conclusions.**

---

## 5. Statement Metadata

In machine-readable form, each statement may carry:

```yaml
type: principle
confidence: C4  # see LM-STD-003
evidence: established
source: LM-STD-002 §3
```

---

## Relationship to Other Standards

- **LM-STD-003** (Confidence) adds *how strongly* a statement is supported.
- **LM-STD-004** (Terminology) ensures the *words* in statements are canonical.
- **LM-STD-006** (Quality Review) audits that statements are correctly typed.
