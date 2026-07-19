---
doc_id: LM-STD-006
title: Quality Review Standard (LQRS)
version: 1.0
status: Approved — Foundation Frozen
governance_level: L1 — Core Standard
governs: How quality is assured across all knowledge artifacts
last_reviewed: 2026-07-14
---

# LM-STD-006 — LogoMind Quality Review Standard

> Quality is **a property of every step**, not a final inspection. This standard defines how we verify an artifact is worthy of publication.

---

## 1. Purpose

Every RS-LIC, engine spec, and asset must meet a defined quality bar before it enters the repository as a Reference Standard. This standard makes that bar explicit, repeatable, and auditable.

---

## 2. The Five Quality Dimensions

| Dimension | Weight | Question |
|-----------|--------|----------|
| **Intellectual Integrity** | 30% | Is it true, principled, and evidence-based? |
| **Educational Quality** | 25% | Does it genuinely develop judgment? |
| **Editorial Quality** | 20% | Is it clear, well-structured, and well-written? |
| **Architectural Quality** | 15% | Does it integrate with the repository correctly? |
| **Professional Excellence** | 10% | Does it contribute lasting value to the discipline? |

---

## 3. Dimension Checklists

### Intellectual Integrity
- [ ] Conceptual accuracy — claims are correct.
- [ ] First-principles integrity — reasoning traces to foundations.
- [ ] Evidence integrity — claims are supported; evidence is separated from interpretation.

### Educational Quality
- [ ] Learning design — the artifact teaches, not just informs.
- [ ] Transferability — the designer can apply it to novel situations.
- [ ] Practical value — it improves real design decisions.

### Editorial Quality
- [ ] Structural — sections fulfil their purpose.
- [ ] Language — precise, clear, jargon explained.
- [ ] Visual communication — diagrams aid understanding.

### Architectural Quality
- [ ] Repository integration — cross-references are correct.
- [ ] Version governance — metadata is complete.
- [ ] Standards compliance — conforms to LM-STD-001 through 005.

### Professional Excellence
- [ ] Professional judgment — it develops expert thinking.
- [ ] Intellectual honesty — uncertainty is communicated.
- [ ] Long-term value — it will remain relevant for years.

---

## 4. The Four Review Gates

| Gate | Focus | Pass Criterion |
|------|-------|----------------|
| **G1 — Draft Review** | Completeness and structure | All sections present; no placeholders. |
| **G2 — Technical Review** | Accuracy and reasoning | Claims verified; evidence checked. |
| **G3 — Editorial Review** | Clarity and language | Meets editorial rules; no ambiguity. |
| **G4 — Repository Review** | Integration and conformance | Cross-references valid; standards met. |

An artifact passes to **Approved** only when all four gates pass.

---

## 5. Quality Scorecard

Each artifact is scored out of 50 (10 per dimension, weighted):

| Score | Status |
|-------|--------|
| 48–50 | **Reference Standard** — exemplary; the bar for all future artifacts. |
| 45–47 | **Approved** — published; refinements are enhancements. |
| 40–44 | **Good** — published with noted improvements needed. |
| < 40 | **Not Ready** — returned for revision. |

**Publication threshold: ≥ 45/50**, with no critical weakness in any dimension.

---

## 6. Critical vs. Improvement Findings

- **Critical finding** — blocks publication. Must be fixed.
- **Improvement finding** — does not block publication. Tracked for future revision.

---

## 7. Quality Debt

Like technical debt, **quality debt** accumulates when improvements are deferred. It is tracked in the artifact's Evolution Log and reviewed periodically.

---

## 8. The Six Questions Publication Test

Before publication, the artifact must answer:

1. **Is it correct?** (intellectual)
2. **Is it clear?** (editorial)
3. **Is it useful?** (educational)
4. **Is it consistent?** (architectural)
5. **Is it maintainable?** (architectural)
6. **Is it worthy?** (professional excellence)

---

## 9. Three CTO Refinements

- **The "Would We Teach This?" Test** — Would we be proud to teach this to a room of professional designers?
- **The Delete Test** — If we deleted this section, would the artifact be weaker? If not, delete it.
- **The Transfer Test** — Can a designer apply this to a brief we never anticipated?

---

## Relationship to Other Standards

LM-STD-006 is the **final gate**. It audits conformance to all other standards:

- LM-STD-001 — Is the Learning Contract fulfilled?
- LM-STD-002 — Are statements correctly typed?
- LM-STD-003 — Are confidence labels present and justified?
- LM-STD-004 — Is terminology canonical?
- LM-STD-005 — Are layers respected?
