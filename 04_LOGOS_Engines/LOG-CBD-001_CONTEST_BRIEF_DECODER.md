---
doc_id: LOG-CBD-001
title: LOGOS Contest Reader — Contest Brief Decoder v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
last_reviewed: 2026-08-14
related:
  - LOG-CFP-001 Client Fit (downstream — the decoded brief is a pre-committed taste input)
  - LOG-DISC-001 Discovery Engine (downstream — the enriched brief sharpens analysis)
  - RS-LIC-CON-VOLUME Contest Dynamics (the brief-reality context)
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-CBD-001 — Contest Brief Decoder

> *Freelancer-style contest briefs arrive as semi-structured free text written in minutes. This engine reads what the holder actually wrote — and invents nothing. Extraction, not interpretation: the preferred and avoided colours are the brief's only pre-committed taste, and they are treated as such.*

---

## 1. Mission

Normalise a pasted contest brief into a structured `ContestBrief` — company, industry, tagline, dos/don'ts, preferred/avoided colours, style keywords, must-include/avoid, references — so downstream engines receive clean signals instead of prose.

## 2. Purpose in the Pipeline

Input tooling (Stage 3), filed under the Client Fit stage. The decoded brief attaches to the project, enriches the client brief with a readable requirements block (so Discovery and Strategy also benefit), and becomes the highest-signal taste input to the Client Preference Predictor — after contest feedback, but ahead of everything the holder never said.

## 3. The Signature Principle: Invent Nothing

Extraction ONLY. If a field is absent from the text, it stays empty — never guessed. The persona engine must never build on fabricated requirements, so the decoder's empty field is a feature, not a gap.

## 4. Inputs

### Required Data
- `raw_text` — the pasted contest brief (any structure)

### Knowledge Sources
- RS-LIC-CON-VOLUME (contest-brief reality: what the holder's lines mean, why contradictions are unranked priorities)

## 5. Reasoning Steps

1. Map natural phrasing to schema fields: "colors in mind" → `colors_preferred`; "anything to avoid" → `must_avoid`/`donts`; "style / look and feel" → `style_keywords`; "sample logos / references" → `references`; "tagline / slogan" → `tagline`.
2. Separate explicit positives (`dos`, `must_include`) from explicit prohibitions (`donts`, `must_avoid`).
3. Write `decoded_summary`: ONE plain paragraph of the holder's intent in their own vocabulary.
4. Grade `confidence` C1–C5 by completeness/parseability (C5 fully explicit → C1 unreadable).

## 6. Decision Rules

- Extraction temperature is minimal; creativity is a defect here.
- Contradictions ("modern but timeless") are preserved verbatim — they are unranked priorities for the persona engine to weigh, not errors to resolve.
- Attachment enriches the project's client brief with a readable block; company/industry fill only if empty.

## 7. Confidence Calculation

LM-STD-003 C1–C5, driven purely by how much explicit signal the text contained — never by inference quality.

## 8. Outputs

### Primary Output: ContestBrief
Structured fields (above) + `decoded_summary` + `confidence`.

### Secondary Outputs
- Enrichment block appended to the project's `client_brief` (so Discovery/Strategy see structured requirements, not just prose)
- Decision-log entry on attach

## 9. What This Engine Is Not

- Not a creative engine — zero interpretation beyond field mapping (FD-015 discipline)
- Not a strategist — contradictions and gaps pass through untouched

## 10. Quality Checks

- Lists normalise (comma/newline strings → arrays; empty strings → null)
- Every populated field traces to text the holder actually wrote
- Normaliser repairs common model drift so validation rarely fails

## 11. Failure Cases

- Empty/garbage text → explicit error (never a fabricated brief)
- Unparseable structure → low confidence with whatever did resolve

## 12. Learning Opportunities

Which phrasings map ambiguously; which fields contest holders consistently omit (feed the Workshop's question bank).

## 13. Future Versions

- Batch decode (portfolio of past contests for a holder → taste profile)
- Platform-aware decoding (format-specific quirks)

## Relationship to Other Engines

Raw contest text → **Contest Brief Decoder** → enriched brief + decoded signals → Client Fit (and Discovery/Strategy upstream context).

## The "Why?" Loop

Why these fields? Because the holder wrote them — and nothing else. The decoder's restraint is what makes the downstream persona trustworthy.
