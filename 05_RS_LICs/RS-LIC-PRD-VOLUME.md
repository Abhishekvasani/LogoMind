---
doc_id: RS-LIC-PRD-VOLUME
title: Production & Deliverables Volume — Starter Set
version: 1.0
status: Approved
category: Production Intelligence
volume: Production Intelligence Series
last_reviewed: 2026-08-14
related:
  - LOG-CP-001 Concept Prompt Engine (wireframes must survive production)
  - LOG-COACH-001 Sketch Coach (production constraints: favicon, embroidery, monochrome)
conformance: "Conforms to LM-STD-001 through LM-STD-006."
---

# Production & Deliverables — Starter Set

> *A mark that cannot be produced everywhere is not a mark — it is a picture of one. Production constraints are design constraints.*

---

## RS-LIC-PRD-001 — The Scale Test

**Definition:** Every mark must stay legible and characterful at four production sizes: 16px (favicon), 32px (app icon), 100px (card/letterhead), 1000px+ (signage/vinyl)
**At 16px:** Thin strokes vanish, counters fill, detail becomes noise — the SILHOUETTE must carry alone
**At 32px:** One internal detail may survive; anything more competes with itself
**At 100px:** Craft shows — optically corrected spacing, stroke joins, negative space
**At 1000px:** Every construction flaw is amplified — wobbly curves and unequal strokes become monuments to error
**Favicon Rule:** If the full lockup fails at 16px, ship the symbol alone as the favicon — never a shrunken lockup
**Best For:** Testing every direction BEFORE commitment; wireframe specs that declare scale behaviour

---

## RS-LIC-PRD-002 — Stroke & Detail Craft

**Definition:** Minimum stroke weights and detail density rules that survive real reproduction
**Minimum stroke:** At 16px, no stroke thinner than ~1.5px rendered (2px safe); vector masters should keep stroke-to-canvas ratio consistent when scaled
**Detail density:** One focal detail per mark; a second detail must be subordinate in size or contrast
**Vinyl/signage:** Interior gaps must exceed cutting tolerance — trapped islands and hairline gaps are the first casualties
**Embroidery:** Minimum satin-stitch width (~1mm at garment scale); gradients and hairlines cannot be sewn — test the one-colour outline version
**Engraving/etching:** Tapered strokes beat uniform ones; fine serifs burn away
**Best For:** Coach critique of sketches; Concept Prompt wireframe stroke guidance

---

## RS-LIC-PRD-003 — File Format Standards

**Definition:** What to deliver, in which format, and why
**SVG:** The master vector for screen — infinite scale, smallest size, editable; deliver with strokes expanded or documented
**AI / EPS:** Source vector for print vendors and legacy workflows; outline all type before handoff
**PDF (vector):** The print handoff — CMYK, embedded profiles, fonts outlined; one file per finished size where imposition matters
**PNG:** Raster for placements needing transparency — deliver 1x/2x/3x or ≥2000px master; never scale UP from raster
**JPEG:** Photographs only — never logos (no transparency, compression artefacts on flat colour)
**ICO / multi-size PNG set:** Favicons: 16, 32, 48, 180 (apple-touch), 192, 512
**WEBP:** Modern web raster — smaller than PNG at equal quality; optional companion
**Best For:** Handoff planning; Coach and SSB production notes

---

## RS-LIC-PRD-004 — Colour Modes & Versions

**Definition:** The full version set a professional identity ships in
**RGB:** Screen master (SVG/web)
**CMYK:** Print conversion — check for gamut shift; saturated screen blues/oranges drift (test the conversion, don't trust it)
**Pantone (PMS):** Spot-colour standard for exact brand colour in print; one or two spots maximum for cost sanity
**Monochrome (1-colour):** Solid black and reversed (white) versions — the embroidery/stamp/legal-fax test; if it fails here, the mark over-relies on colour
**Grayscale:** Where single-colour reproduction must keep hierarchy
**Best For:** Palette specification in SSB; judging whether a mark's identity lives in form or only in colour

---

## RS-LIC-PRD-005 — Clear Space & Minimum Sizes

**Definition:** The exclusion zone and floor sizes that protect the mark in use
**Clear-space rule:** Exclusion zone = a fixed unit derived from the mark itself (commonly the cap-height or the symbol's key dimension) applied on all sides — define it, publish it
**Minimum size (full lockup):** The smallest size at which the lockup stays legible — measured in mm for print, px for screen; publish it
**Minimum size (symbol alone):** Always smaller than the lockup; the favicon answer
**Co-branding:** Double the clear space when another logo shares the field
**Best For:** SSB guideline summaries; Coach pitfalls ("will it survive a co-branded footer?")

---

## RS-LIC-PRD-006 — Handoff Package Standards

**Definition:** The professional deliverable checklist that separates a logo from an identity
**Master files:** Editable source (AI) + universal vector (SVG, EPS, PDF) + raster set (PNG @1x/2x/3x, favicon set)
**Version set:** Full colour (RGB + CMYK), mono black, reversed white, grayscale
**Colour specification:** HEX (screen), RGB, CMYK, Pantone where budgeted — one palette sheet
**Construction sheet:** Grid, clear space unit, minimum sizes — one page
**Naming discipline:** `brand_logo-version-colour-mode.format` (e.g. `acme_logo-primary-cmyk.pdf`) — the client's future self is the user
**Best For:** The final-mile checklist; Presentation "Applications" and "Guidelines Summary" sections

---

## Volume Metadata

| Field | Value |
|-------|-------|
| Entries | 6 (starter set) |
| Full volume target | Add: motion/logo-animation specs, responsive/variable logo systems in depth, accessibility (contrast in application), packaging/pre-press, screen-print and merch reproduction |
| Feeds | Concept Prompt (scale-aware wireframes), Sketch Coach (production constraints), SSB (guideline summary), Presentation (applications) |

---

## Production Checklist Framework

| Checkpoint | The question | Fail sign |
|-------------------|--------------|-----------|
| 16px silhouette | Does the mark read as a shape alone? | Detail noise; unreadable blob |
| One-colour test | Does it survive solid black + reversed white? | Identity dies without colour |
| Stroke floor | Do any strokes fall below minimum at small sizes? | Vanishing hairlines |
| Reproduction spread | Vinyl / embroidery / engraving viable? | Trapped islands; unsewable detail |
| Gamut check | Does CMYK conversion hold the palette's intent? | Sad shifted blue |
| Clear space defined | Is the exclusion zone measurable and published? | "Leave some room" |
| Version set | Full-colour, mono, reverse, grayscale all exist? | Colour-dependent mark |
| Handoff named | Does every file follow naming discipline? | `final_final_v3.png` |

---

*LogoMind Principle: Production is not a phase after design — it is a constraint during design. The professional mark is designed at 16px and 3 metres at once, and every deliverable exists so the client never has to ask.*
