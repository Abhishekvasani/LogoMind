---
doc_id: LOG-CP-001
title: LOGOS Concept Prompt Engine v1.0
version: 1.0
status: Approved
governance_level: L2 — Engine Specification
founder_decision: FD-015
last_reviewed: 2026-08-03
related:
  - LOG-CREATE-001 Create Engine (upstream — provides Concept Families)
  - LOG-JUDGE-001 Judge Engine (upstream — evaluates Concept Families)
  - LOG-INSIGHT-001 Insight Engine (upstream — provides cliché context)
  - LOG-STRAT-001 Strategy Engine (upstream — provides Brand DNA)
  - PROD-SSB-001 Strategic Sketch Brief (downstream sibling deliverable)
  - FD-015 Concept Prompts & Wireframes
conformance: "This engine conforms to LM-STD-001 through LM-STD-006 and the Engine Blueprint Standard."
---

# LOG-CP-001 — Concept Prompt Engine

> *The Concept Prompt Engine is where strategy becomes executable. It takes an evaluated Concept Family and produces an executable concept — a detailed concept prompt (with variants and per-model adaptations), a composition wireframe, and a rationale trace — that the designer takes to their own image tool. It does not generate images, and it does not make the creative decision. It produces a strategy-grounded instrument (FD-015).*

---

## 1. Mission

Transform one evaluated Concept Family (from the Create + Judge engines) into an **executable concept**: a detailed, model-agnostic concept prompt with **four variants** and **per-model adaptations**, a **composition/layout wireframe** (delivered as a structured spec the front-end renders deterministically), and a **rationale trace** back to Brand DNA.

The designer then takes the prompt and wireframe to their own image model (Midjourney, Ideogram, Recraft, Stable Diffusion, etc.). LogoMind generates no images and makes no creative decision.

---

## 2. Purpose in the Pipeline

```
LOGOS Strategy → LOGOS Insight → LOGOS Create → LOGOS Judge → LOGOS Concept Prompt → SSB / Sketch
(Brand DNA)       (clichés)        (Concept        (evaluation)   (executable concept     (existing
                                   Families)                      per family)              pipeline tail)
                                                                                          ▲
                                                                                          │
                                                                                 THE CONCEPT PROMPT ENGINE
                                                                                 outputs prompt + wireframe
                                                                                 + rationale per family
```

The Concept Prompt Engine occupies the execution pivot — the moment evaluated strategic territories become concrete, model-ready instruments. Its output is not a logo; it is the *sharpest possible brief* for an image model, grounded in everything the pipeline reasoned about upstream.

This engine is the explicit, governed home (FD-015) for prompt and wireframe output. The Create Engine remains the home of strategic Concept Families (it "does not generate logos"; it now also does not generate prompts — that responsibility moved here to preserve single-responsibility).

---

## 3. The Signature Principle: The Wireframe Is a Spec, Not an Image

> Most AI tools either generate finished images (which look AI-generic and aren't editable) or produce text prompts (which leave composition to chance).
>
> LogoMind generates a **structured wireframe spec** — element kinds, geometry, position, relative size, balance, alignment — that the front-end renders to clean, deterministic, fully-editable SVG.

This is the engine's defence against the "generic" failure mode. Because the wireframe is generated *deterministically from a spec* (not drawn by an image model), it:

- never looks AI-generated,
- is fully unit-testable (spec → rendered elements),
- is editable downstream (the designer opens the SVG in Figma/Illustrator),
- works identically across every image model (it is a *composition instruction*, not a style).

The LLM describes layout; it never draws pixels.

---

## 4. Inputs

### Required Data
- **Concept Family** (from Create Engine) — `family_label`, `theme`, `core_meaning_served`, `symbols`, `visual_language`, `why_it_works`.
- **Judge result** (from Judge Engine) — `classification`, `composite`, `concept_dna`, `refinement_recommendations`. This tells the engine how the family was evaluated and what to emphasise or correct.
- **Brand DNA** (from Strategy Engine) — purpose, positioning, differentiation, audience, personality, archetype, emotional goal. The prompt must trace to these.
- **Insight Report** (from Insight Engine) — clichés to avoid, opportunities to exploit.

### Optional Data
- Client symbol preferences and the strategy's handling of them (carried in the family).

### Knowledge Sources
- **RS-LIC-PH-005 Originality** — keeps the prompt from drifting into cliché (the Combination Method applies to prompt construction too).
- The Create Engine's `visual_language` (forms, treatment, composition, palette) — the prompt must *execute* this, not contradict it.

---

## 5. Reasoning Steps

```
Step 1: DISTIL THE CORE CONCEPT
   → Read the family + its judge evaluation.
   → Write ONE sentence: the visual concept this family becomes.
   → This sentence anchors every variant.

Step 2: GENERATE FOUR PROMPT VARIANTS
   → Produce exactly four, each emphasising a different angle:
     ├── minimal       — fewest elements, maximum clarity, single-weight
     ├── detailed      — richer treatment, full visual_language honoured
     ├── typographic-led — the wordmark/lettering is the hero; symbol subordinate
     └── symbolic      — the mark/symbol is the hero; typography subordinate
   → Each variant is a complete, model-agnostic natural-language prompt.
   → Each carries a one-line `intent` stating what it emphasises.

Step 3: WRITE PER-MODEL ADAPTATIONS
   → For each model family (midjourney, ideogram, stable-diffusion, recraft, general):
     ├── notes: one line on how to tune the prompt for that family's quirks
     └── example_suffix: a concrete tunable (e.g. "--ar 1:1 --style raw" for MJ)

Step 4: COMPOSE THE WIREFRAME SPEC
   → Describe layout as structured data, never as pixels or prose imagery:
     ├── orientation (horizontal | stacked | lockup | emblem)
     ├── balance (e.g. "60/40 symbol-to-text")
     ├── alignment (center | left | baseline-aligned)
     ├── safe_margin (e.g. "12% padding")
     ├── elements[]: each with kind, geometry, position, relative_size, notes
     └── favicon_note: how the composition degrades at favicon size
   → The spec must be renderable by a deterministic SVG renderer.

Step 5: TRACE THE RATIONALE
   → One short paragraph: why these variants, traced to Brand DNA meaning
     and the family's visual_language. What strategic territory each covers.

Step 6: SURFACE CLICHÉS AVOIDED
   → List the specific clichés (from Insight) deliberately NOT prompted,
     with a phrase on what was used instead.

Step 7: ASSIGN CONFIDENCE (LM-STD-003)
   → Honest C-level: how well-supported is this executable concept by the
     upstream strategy? Never faked.
```

---

## 6. Decision Rules

| Rule | Condition | Action |
|------|-----------|--------|
| **DR-1** | Judge classification is `reject` | Still produce the concept (the designer may iterate), but set confidence ≤ C2 and note the rejection in the rationale |
| **DR-2** | A variant would require a cliché symbol | Discard that phrasing; re-express via the Combination Method (RS-LIC-PH-005) |
| **DR-3** | The family's `visual_language` conflicts with a variant style | Resolve in favour of `visual_language`; note the resolution in the variant's `intent` |
| **DR-4** | The wireframe spec is ambiguous or un-renderable | Simplify to a known orientation + 2–3 elements; never emit a freeform description |
| **DR-5** | No clear favicon degradation story | Set `favicon_note` to the honest constraint and lower confidence |

---

## 7. Confidence Calculation

Each executable concept carries a confidence score reflecting how well-supported it is by upstream strategy, not how "good" the logo might be (the engine makes no aesthetic judgement).

| Factor | Weight |
|--------|--------|
| Traceability to Brand DNA (does every variant serve a meaning?) | 35% |
| Wireframe renderability (is the spec clean and unambiguous?) | 25% |
| Cliché avoidance visible (are specific clichés named and sidestepped?) | 20% |
| Judge alignment (does it honour the evaluation + refinements?) | 20% |

Concepts scoring < C3 are flagged as *exploratory* — useful starting points with caveats. The designer always decides.

---

## 8. Outputs

### Primary Output: Executable Concept (per family)

```yaml
concept_prompt:
  family_label: <A | B | C | ...>
  core_concept: "<one-sentence distillation of the family as a visual>"

  variants:
    - style: minimal
      prompt: "<complete model-agnostic concept prompt>"
      intent: "<one line: what this variant emphasises>"
    - style: detailed
      prompt: "..."
      intent: "..."
    - style: typographic-led
      prompt: "..."
      intent: "..."
    - style: symbolic
      prompt: "..."
      intent: "..."

  model_adaptations:
    - model_family: midjourney
      notes: "<how to tune for MJ>"
      example_suffix: "<e.g. --ar 1:1 --style raw>"
    - model_family: ideogram
      notes: "..."
      example_suffix: "..."
    - model_family: stable-diffusion
      notes: "..."
      example_suffix: "..."
    - model_family: recraft
      notes: "..."
      example_suffix: "..."
    - model_family: general
      notes: "..."
      example_suffix: "..."

  wireframe:
    orientation: <horizontal | stacked | lockup | emblem>
    balance: "<e.g. 60/40 symbol-to-text>"
    alignment: <center | left | baseline-aligned>
    safe_margin: "<e.g. 12% padding>"
    elements:
      - kind: <symbol | wordmark | tagline | container | negative-space>
        geometry: <circle | hexagon | rectangle | monogram | baseline-bar | custom>
        position: <center | left-of-text | above | below | integrated>
        relative_size: <dominant | balanced | accent | small>
        notes: "<optional detail>"
    favicon_note: "<how it degrades at small size>"

  rationale: "<paragraph tracing variants to Brand DNA + visual_language>"
  cliches_avoided:
    - "<cliché deliberately not prompted>"
  confidence: <C1 | C2 | C3 | C4 | C5>
```

### Secondary Outputs
- **Cliché Avoidance** — surfaced in `cliches_avoided`, mirroring the Create Engine's cliché report so the designer sees what was rejected and why.
- **Favicon degradation note** — directly serves the "must work at favicon size" quality check from LOG-CREATE-001's "Why?" Loop.

---

## 9. What This Engine Is Not

- ❌ It is **not** an image generator. It produces prompts and a wireframe *spec*.
- ❌ It is **not** a creative decision-maker. It produces instruments; the designer chooses and executes.
- ❌ It is **not** a competitor to the Create Engine. Create produces strategic territories; this engine executes one territory as a model-ready concept.
- ❌ It is **not** model-specific. Variants are model-agnostic; model behaviour lives in `model_adaptations`.

---

## 10. Quality Checks

| Check | Question | Pass Criterion |
|-------|----------|----------------|
| **Variant Count** | Are there exactly four variants with the named styles? | Yes |
| **Model Coverage** | Are all five model families addressed? | Yes |
| **Wireframe Renderability** | Is the spec composed of known element kinds/geometry/positions? | Yes — no freeform description |
| **Cliché Avoidance** | Are specific clichés named and sidestepped? | Yes — consulted from Insight |
| **Brand DNA Trace** | Can each variant's emphasis be traced to a Brand DNA meaning? | Yes |
| **Favicon Note** | Is there an honest small-size degradation story? | Yes |
| **Honest Confidence** | Is the C-level supported by the upstream strategy? | Yes (LM-STD-003) |

---

## 11. Failure Cases

| Failure | What Happens | Prevention |
|---------|--------------|------------|
| **Image-y Wireframe** | Engine describes the mark as imagery ("a soaring eagle") instead of geometry | Enforce the element vocabulary (kind/geometry/position); reject freeform |
| **Generic Prompt** | Variants read like a stock prompt with no strategic grounding | Require Brand DNA trace per variant; cliché-avoidance list |
| **Model Bias** | The "model-agnostic" prompt is secretly tuned for one model | Keep tuning in `model_adaptations` only; variants stay neutral |
| **Cliché Compliance** | Engine prompts the very clichés Insight flagged | Cliché check before emitting each variant |
| **Decision Lock-In** | Engine asserts one variant as "the answer" | All four are presented as parallel starting points; no ranking by the engine |
| **Skipped Confidence** | Output shipped without an honest C-level | LM-STD-003 — confidence is required, never faked |

---

## 12. Learning Opportunities

- Which variant styles do designers actually use downstream? (Informs future variant set)
- Which wireframe orientations correlate with designer satisfaction? (Builds layout intelligence)
- Which model adaptations most need tuning per real-model behaviour? (Keeps the adaptation set honest)
- Where do real image models fail to honour the wireframe spec? (Improves the spec vocabulary)

---

## 13. Future Versions

| Version | Enhancement |
|--------|-------------|
| v1.1 | Refinement loop — designer feedback reshapes a single variant |
| v1.2 | Animated/motion wireframe orientation |
| v1.3 | Per-model prompt *re-generation* (not just suffix tuning) |
| v2.0 | Co-creative mode — designer edits the wireframe spec; engine rewrites prompts to match |

---

## Relationship to Other Engines

| Engine | Relationship |
|--------|-------------|
| **LOGOS Create** (upstream) | Provides the Concept Family this engine executes |
| **LOGOS Judge** (upstream) | Provides evaluation + refinements the engine honours |
| **LOGOS Insight** (upstream) | Provides the cliché list the engine avoids |
| **LOGOS Strategy** (upstream) | Provides Brand DNA the prompts must trace to |
| **SSB (PROD-SSB-001)** (sibling) | The SSB remains the strategic deliverable; this engine is the executable sibling that turns a chosen family into a model-ready concept |

---

## The "Why?" Loop

For every executable concept, the engine applies the "Why?" Loop inherited from LOG-CREATE-001:

- Why this core concept?
- Why these four variants?
- Is any variant leaning on a cliché?
- Does the wireframe spec survive rendering at favicon size?
- Does each variant trace to a Brand DNA meaning?
- Would a real image model be able to execute this without guessing?
- Have I confused "model-agnostic" with "vague"?

Only concepts that survive the "Why?" Loop are emitted.
