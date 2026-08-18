---
doc_id: RS-LIC-INDEX
title: LIC Knowledge Index
version: 1.0
status: Living Document
governance_level: L1 — Navigation
last_reviewed: 2026-08-14
---

# 05_RS_LICs — Knowledge Index

The LIC (Licensed Intelligence Corpus) volumes are LogoMind's knowledge base. They are **loaded and sliced at startup** by `backend/app/services/lic_knowledge.py` — each volume's operational core (tables, tests, frameworks) is extracted and injected into the engine prompts listed below. `/health` reports which extracts resolved.

**24 volumes · 11 domains.** IDs follow `RS-LIC-<SERIES>-<NNN|VOLUME>`.

## Textbook Series (deep, 11-section template)

| Series | Volumes | Operational core (what engines receive) |
|--------|---------|------------------------------------------|
| **PH — Philosophy** | PH-001 Meaning · PH-002 Purpose · PH-003 Simplicity · PH-004 Clarity · PH-005 Originality · PH-006 Memorability · PH-007 Authenticity · PH-008 Timelessness · PH-009 Relevance · PH-010 Consistency | Professional sequences, audits, tests, failure modes — e.g. PH-005's Combination Method + 5 Originality Tests; PH-008's Trend Taxonomy |
| **BS — Brand Strategy** | BS-001 Positioning · BS-002 Differentiation · BS-003 Target Audience · BS-004 Personality · BS-005 Archetypes | Statement templates, audits, the Twelve Classical Archetypes table |

## Starter-Set Catalogs (compact, field-per-entry, machine-friendly)

| Volume | Entries | Feeds | Status vs target |
|--------|---------|-------|------------------|
| `RS-LIC-SY-VOLUME` — Symbol | 33 symbols | Create, Insight, Client Fit | 33 / 150+ |
| `RS-LIC-CL-VOLUME` — Color | 18 colours + WCAG standards | Create, Client Fit | 18 / 50+ |
| `RS-LIC-TY-VOLUME` — Typography | 10 categories + semantics/pairing | Create | 10 / 40+ |
| `RS-LIC-ID-VOLUME` — Identity | 10 concepts (grids, logo types…) | Create, Concept Prompt, SSB | 10 / 60+ |
| `RS-LIC-IND-VOLUME` — Industry | 14 categories: conventions, cliché maps, opportunities | Insight, Create | 14 / 30+ |
| `RS-LIC-PSY-VOLUME` — Client Psychology | 8 decision-maker types + Feedback Decoder + Objection Taxonomy + Rationale Narrative | Client Fit, Presentation | 8 / 12+ types |
| `RS-LIC-PRD-VOLUME` — Production & Deliverables | 6 entries + Production Checklist | Concept Prompt, Coach, SSB | starter |
| `RS-LIC-CON-VOLUME` — Contest Dynamics | 6 entries + Contest Signal Framework | Client Fit refine loop | starter |
| `RS-LIC-TM-VOLUME` — Trademark & Distinctiveness | 4 entries + Trademark Check | Judge | starter |

## Engine → Knowledge map

| Engine | Injects |
|--------|---------|
| Strategy | BS-001…005 (all five frameworks) |
| Insight | PH-008, PH-009, SY, IND |
| Create | PH-005, SY, CL, TY, ID, IND + style anchors |
| Judge | PH-005, PH-003, PH-004, PH-006, PH-008, TM |
| Client Fit | CL, SY, BS-005, PSY, CON |
| Concept Prompt | PH-005, ID, PRD + style anchors |
| SSB | ID, PRD |
| Sketch Coach | PH-003, PH-004, PRD |
| Presentation | PSY |

The Contest Brief Decoder is deliberately knowledge-light (extraction purity). Guarded by tests: `backend/tests/test_knowledge.py` asserts every registry entry resolves and every wiring claim above holds.

## Conventions

- Frontmatter carries `doc_id`, `status`, `last_reviewed`, `related`, and conformance to LM-STD-001…006.
- Catalog volumes self-declare expansion targets in their **Volume Metadata** table.
- Slicers target markdown anchors (bold section headers) so extracts survive prose edits; each slicer caps size for token budget.
