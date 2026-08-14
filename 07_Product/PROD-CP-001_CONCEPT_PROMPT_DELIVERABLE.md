---
doc_id: PROD-CP-001
title: Concept Prompt Deliverable Specification
version: 1.0
status: Approved
governance_level: L2 — Product Specification
last_reviewed: 2026-08-03
related:
  - FD-015 Concept Prompts & Wireframes
  - LOG-CP-001 Concept Prompt Engine
  - LOG-CREATE-001 Create Engine
  - LOG-JUDGE-001 Judge Engine
  - PROD-SSB-001 Strategic Sketch Brief
  - PROD-SCREEN-001 Screen Architecture
conformance: "This document conforms to LM-STD-001 through LM-STD-006."
---

# PROD-CP-001 — The Concept Prompt Deliverable

> *This document defines what the Concept Prompt deliverable is, what it contains, and how the designer experiences it. It is the executable sibling of the Strategic Sketch Brief: where the SSB is the strategy, the Concept Prompt is the strategy made model-ready.*

---

## 1. The One-Sentence Definition

> **The Concept Prompt deliverable turns each evaluated Concept Family into a model-ready concept: a detailed concept prompt with four variants and per-model adaptations, a composition wireframe the designer can render and edit, and a rationale trace — that the designer takes to their own image tool.**

Every word earns its place:
- **Turns each evaluated Concept Family** — one deliverable per family, produced after Judge.
- **Model-ready concept** — the output is shaped to be executed by an external image model, not by LogoMind.
- **Four variants** — parallel starting points, not ranked; the designer chooses.
- **Per-model adaptations** — model behaviour is separated from the concept itself.
- **Composition wireframe** — a deterministic, editable layout, not an AI image.
- **The designer takes it to their own image tool** — LogoMind generates no images and makes no decision (FD-015).

---

## 2. What the Deliverable Is

The Concept Prompt is the **designer's execution instrument** — the bridge between LogoMind's strategic reasoning and the designer's chosen image model. It exists because writing a concept prompt cold produces generic output; writing one grounded in Brand DNA, evaluated concepts, and cliché awareness produces genuinely distinctive starting points.

The Concept Prompt is *not*:
- ❌ A logo (it produces no images)
- ❌ A final answer (it offers four parallel starting points)
- ❌ Model-locked (variants are model-agnostic; tuning is separate)
- ❌ A replacement for the designer's eye (the designer still selects, edits, and executes)

---

## 3. The Concept Card (per family)

Each Concept Family produces one **Concept Card**. The card has five regions:

| Region | Contains | Purpose |
|--------|----------|---------|
| **Header** | Family label, core concept sentence, confidence pill | One-glance identity |
| **Variants** | Four prompts (minimal / detailed / typographic-led / symbolic), each with a Copy button and intent line | The model-ready starting points |
| **Model Adaptations** | Five rows (Midjourney / Ideogram / Stable Diffusion / Recraft / General), each with tuning notes + example suffix | How to tune per model |
| **Wireframe** | Rendered SVG preview + raw spec + Download SVG / Copy PNG + favicon tile | The composition blueprint |
| **Rationale & Clichés** | Trace to Brand DNA + the clichés deliberately avoided | Why these choices |

---

## 4. The Four Variant Styles

Each family yields exactly four concept prompts, each emphasising a different angle. They are parallel starting points — the engine does **not** rank them.

| Style | Emphasis | When the designer reaches for it |
|-------|----------|----------------------------------|
| **minimal** | Fewest elements, maximum clarity, single-weight | When the brand needs instant legibility and favicon resilience |
| **detailed** | Richer treatment, the full `visual_language` honoured | When the brand has room for craft and texture |
| **typographic-led** | The wordmark/lettering is the hero; the symbol is subordinate | When the name itself carries the brand |
| **symbolic** | The mark/symbol is the hero; typography is subordinate | When the symbol is the memorable asset |

Each variant carries a one-line `intent` so the designer knows what it emphasises before reading the full prompt.

---

## 5. The Wireframe Spec Vocabulary

The wireframe is delivered as a **structured spec**, never as prose imagery. This is what makes it deterministic, editable, and never AI-generic. The vocabulary is closed:

### 5.1 Top-level spec
| Field | Values |
|-------|--------|
| `orientation` | `horizontal` \| `stacked` \| `lockup` \| `emblem` |
| `balance` | freeform short string (e.g. "60/40 symbol-to-text", "centered") |
| `alignment` | `center` \| `left` \| `baseline-aligned` |
| `safe_margin` | short string (e.g. "12% padding") |
| `elements[]` | 2–4 element descriptors (below) |
| `favicon_note` | how the composition degrades at favicon size |

### 5.2 Element descriptor
| Field | Values |
|-------|--------|
| `kind` | `symbol` \| `wordmark` \| `tagline` \| `container` \| `negative-space` |
| `geometry` | `circle` \| `hexagon` \| `rectangle` \| `monogram` \| `baseline-bar` \| `custom` |
| `position` | `center` \| `left-of-text` \| `above` \| `below` \| `integrated` |
| `relative_size` | `dominant` \| `balanced` \| `accent` \| `small` |
| `notes` | optional short detail |

The front-end renderer maps each `geometry` to a clean SVG primitive, positions it per `position`, and scales it per `relative_size`. Element labels are drawn beside each shape so the wireframe reads as a **layout diagram**, not a logo attempt.

---

## 6. The Per-Model Adaptation Set

Model behaviour is separated from the concept itself. Each card carries five adaptation rows:

| Model Family | What the adaptation addresses |
|--------------|-------------------------------|
| **midjourney** | Aspect ratio, stylisation flags (e.g. `--ar 1:1 --style raw`) |
| **ideogram** | Text-rendering reliability and prompt structure |
| **stable-diffusion** | Sampler/prompt-weighting considerations |
| **recraft** | Vector-style and style presets |
| **general** | Model-agnostic guardrails that help any model |

Each row has a `notes` line (how to tune) and an `example_suffix` (a concrete, copy-pasteable tunable). This keeps the four variants genuinely model-agnostic.

---

## 7. Export Formats

| Format | Use |
|--------|-----|
| **Copy prompt** | One-click copy of any variant's prompt to the clipboard |
| **Copy model suffix** | One-click copy of an adaptation's `example_suffix` |
| **Download SVG** | The wireframe as an editable vector (open in Figma/Illustrator) |
| **Copy PNG** | The wireframe rasterised for quick sharing |

All export is client-side; no backend round-trip.

---

## 8. Progressive Disclosure

Per LM-STD-005, the card is layered:

- **Layer A — Essence (10 seconds):** header + core concept + the wireframe preview.
- **Layer B — Working (1 minute):** all four variants (skim intents) + the model adaptation table.
- **Layer C — Deep (on demand):** full prompts, raw wireframe spec, rationale, clichés avoided.

The designer should be able to pick a variant to try within a minute of landing on a card.

---

## 9. The Product Promise (inherited)

> **LogoMind will never make a creative decision for the designer.**

The Concept Prompt deliverable honours this absolutely:
- It offers four parallel starting points — it does not pick one.
- It produces a wireframe *spec* — it does not render the logo.
- It traces rationale — it does not assert correctness.
- The designer selects, edits, and executes in their own tool.

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Four variants present** | Are minimal/detailed/typographic-led/symbolic all present? | Yes |
| **Five model families** | Are MJ/Ideogram/SD/Recraft/General all addressed? | Yes |
| **Wireframe renderable** | Is the spec within the closed vocabulary? | Yes |
| **No cliché compliance** | Are Insight clichés avoided, not prompted? | Yes |
| **Brand DNA trace** | Can each variant's emphasis be traced to Brand DNA? | Yes |
| **Honest confidence** | Is the C-level supported by upstream strategy? | Yes (LM-STD-003) |
| **Copy/export works** | Do copy-prompt, download-SVG, copy-PNG all function client-side? | Yes |

---

## 11. Relationship to Upstream

| Source | What it provides to the Concept Card |
|--------|--------------------------------------|
| **LOG-CREATE-001** | The Concept Family (theme, symbols, visual language) |
| **LOG-JUDGE-001** | The evaluation (classification, refinements) the card honours |
| **LOG-INSIGHT-001** | The cliché list the card avoids |
| **LOG-STRAT-001** | The Brand DNA every variant traces to |

---

## 12. What Success Looks Like

The Concept Prompt deliverable succeeds when a designer says:

> *"I pasted the prompt into Midjourney and got something I could actually work from — not the generic slop I usually get."*
>
> *"The wireframe told me exactly how to compose it before I'd drawn anything."*
>
> *"Four variants meant I could explore in minutes instead of starting over each time."*

Not: *"It generated my logo."* That sentence should never describe this deliverable.
