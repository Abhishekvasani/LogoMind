# LogoMind AI

> **Reason. Create. Refine.**

LogoMind AI is a long-term knowledge infrastructure project for logo and brand-identity design. It exists to develop **professional judgment** rather than merely transfer information. The repository is designed to become the world's most rigorous, maintainable, and trustworthy body of knowledge for identity design.

---

## What LogoMind Is

LogoMind is **not** an AI logo generator. It is a **Strategic Design Intelligence Platform** — a structured methodology that software (eventually) delivers. At its heart are two proprietary assets:

- **LOGOS** — *LogoMind Oriented Generative & Strategic Orchestration System* — the reasoning engine that thinks like an experienced creative director.
- **LMKC / LKG** — *LogoMind Knowledge Core* / *LogoMind Knowledge Graph* — a structured, interconnected knowledge system that LOGOS reasons over.

The product's promise:

> Transform a simple client brief into a complete creative strategy that helps designers sketch distinctive, meaningful, and timeless logo concepts.

---

## Repository Layers

| Layer | Folder | Purpose |
|-------|--------|---------|
| **Foundation** | `01_Foundation/` | Charter, Constitution, identity, milestones |
| **Philosophy** | `02_Philosophy/` | Mission, core principles, virtues, manifesto |
| **LKOS Standards** | `03_LKOS_Standards/` | The 6 governing standards (LM-STD-001 through 006) |
| **LOGOS Engines** | `04_LOGOS_Engines/` | Reasoning engine specifications |
| **Reference Standards** | `05_RS_LICs/` | Knowledge objects (RS-LICs) |
| **Assets** | `06_Assets/` | Case studies, decision studio, reasoning gallery |
| **Research** | `07_Research/` | Source research feeding the knowledge core |
| **Quality** | `08_Quality/` | Review frameworks, audit checklists |
| **Operations** | `09_Operations/` | Operating model, production pipeline, decision log |
| **Extracted Drafts** | `10_Drafts_Extracted/` | Raw drafts recovered from the founding conversation |

---

## The LKOS (LogoMind Knowledge Operating System)

Six core standards govern every knowledge object in the repository:

| Standard | Name | Governs |
|----------|------|---------|
| LM-STD-001 | Learning Contract | What each artifact teaches |
| LM-STD-002 | Statement Taxonomy | How statements are classified |
| LM-STD-003 | Confidence Framework | How strongly supported a claim is |
| LM-STD-004 | Terminology Governance | Canonical vocabulary |
| LM-STD-005 | Knowledge Layering | How knowledge is layered |
| LM-STD-006 | Quality Review | How quality is assured |

---

## Guiding Principles

1. **Knowledge before opinion.**
2. **Strategy before aesthetics.**
3. **Meaning before style.**
4. **Explainability over mystery.**
5. **The designer always makes the final creative decision.**
6. **Reason. Create. Refine.**

---

## Working with This Repository

- **GitHub is the single source of truth.**
- Every document carries an **Identifier, Version, Status, and Metadata**.
- Cross-reference related artifacts; preserve a single source of truth for each concept.
- The **core LKOS is frozen** (Architecture Freeze v1.0) — refine only when repeated production friction, discovered contradictions, or strong evidence justifies change.

---

## Status

**Current phase:** Phase 5 complete; Phase 6 (Launch) next. LogoMind is **runnable software**:

- **Knowledge:** 24 LIC volumes across 11 domains (Philosophy 10, Brand Strategy 5, Symbol 33-entry catalog, Color 18 + WCAG, Typography, Identity, Industry Intelligence, Client Psychology, Production & Deliverables, Contest Dynamics, Trademark & Distinctiveness) — loaded and injected into the engines by `backend/app/services/lic_knowledge.py`.
- **Engines:** 13 fully specified LOGOS engines (incl. Concept Prompt, Client Fit, Contest Brief Decoder), 9 of them knowledge-grounded at prompt-build time.
- **App:** 13-stage pipeline (FastAPI + Next.js), Claude-inspired dark theme with light/dark toggle, 29-test backend suite, mock/OpenAI/OpenRouter/NIM providers. Run it: see `PHASE5_README.md`.
- **Open before launch:** authentication, file upload, Alembic migrations, production deployment (see `ROADMAP.md` v5.1).

**Origin:** This repository was reconstructed from the founding conversation (June–July 2026) between the Founder (Abhishek) and the original AI collaborator. The `10_Drafts_Extracted/` folder contains a catalog of every draft produced during that conversation, classified and assessed.
