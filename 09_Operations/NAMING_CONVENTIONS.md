---
doc_id: STD-DOC-001
title: LogoMind Document Standard & Naming Conventions
version: 1.0
status: Approved
governance_level: L1 — Repository Standard
last_reviewed: 2026-07-14
---

# LogoMind Document Standard & Naming Conventions

---

## Document Identity

Every document in the repository carries front-matter metadata:

```yaml
---
doc_id: <IDENTIFIER>
title: <Title>
version: <SEMVER>
status: <Draft | Approved | Reference Standard | Superseded>
governance_level: <L0–L5>
last_reviewed: <YYYY-MM-DD>
---
```

---

## Document ID Prefixes

| Prefix | Document Type | Example |
|--------|---------------|---------|
| `FD` | Founder's Decision | FD-001 |
| `CD` | CTO Decision | CD-080 |
| `LM-STD` | LKOS Standard | LM-STD-001 |
| `LM-CON` | Constitution-level document | LM-CON-001 |
| `LM-OP` | Operating standard | LM-OP-001 |
| `LOG-*` | LOGOS Engine spec | LOG-DISC-001 |
| `RS-LIC` | Reference Standard LIC | RS-LIC-PH-001 |
| `TERM` | Canonical term definition | TERM-001 |
| `S` | Seed (future idea) | S-001 |
| `LM-PHIL` | Philosophy document | LM-PHIL-001 |

---

## RS-LIC ID Format

```
RS-LIC-<CATEGORY>-<NUMBER>

RS-LIC-PH-001   ← Philosophy series, card 1
RS-LIC-BS-014   ← Brand Strategy series, card 14
RS-LIC-SY-087   ← Symbol Intelligence series, card 87
RS-LIC-TY-021   ← Typography Intelligence series, card 21
RS-LIC-CL-030   ← Color Intelligence series, card 30
RS-LIC-ID-008   ← Identity Design series, card 8
```

### Category Codes
| Code | Category |
|------|----------|
| PH | Philosophy |
| BS | Brand Strategy |
| SY | Symbol Intelligence |
| TY | Typography Intelligence |
| CL | Color Intelligence |
| ID | Identity Design |
| PS | Psychology |
| SE | Semiotics |
| PR | Production |

---

## File Naming

Files use `UPPER_SNAKE_CASE` with the doc_id prefix:

```
LM-STD-001_LEARNING_CONTRACT.md
RS-LIC-PH-001_Meaning.md
LOG-DISC-001_DISCOVERY_ENGINE.md
```

---

## Repository Maturity Levels

| Level | Name | Meaning |
|-------|------|---------|
| L0 | Constitution | Founding documents; change rarely. |
| L1 | Standard | Governing standards; frozen in v1.0. |
| L2 | Reference Standard | Knowledge objects (RS-LICs). |
| L3 | Asset | Case studies, diagrams, exercises. |
| L4 | Working Draft | In-progress; not yet reviewed. |

---

## Versioning

Semantic versioning: `MAJOR.MINOR`

- **MAJOR** — structural or philosophical change.
- **MINOR** — content addition or refinement.

Every version change is recorded in the document's Evolution Log.
