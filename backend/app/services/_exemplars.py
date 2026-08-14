"""Gold-standard style anchors for LogoMind's creative engines.

Free / quantised models (NVIDIA NIM nemotron, OpenRouter free tiers) drift
toward generic, adjective-heavy output unless shown a concrete quality target.
These compact worked contrasts are injected into the engine system prompts as
few-shot anchors — they teach the *style* (vivid, specific, craft-grounded,
renderable), not content to copy.

Design:
  - CONTRAST format ("GENERIC fails / VIVID target") — the single most
    token-efficient way to teach "avoid this, do that".
  - Each VIVID example names exact colour, stroke weight, material, grid, and
    ONE distinctive memory hook — the five things that separate a prompt a
    thousand logos could satisfy from one only THIS brand owns.
  - Deliberately different industries from a typical live brief, so the model
    anchors on craft, not copyable subject matter.
"""

# ─── Concept Prompt engine: prompt-writing style anchor ─────────────────
# Teaches the difference between a non-renderable generic prompt and a vivid,
# distinctive, copyable one. Injected into CONCEPT_PROMPT_SYSTEM_PROMPT.
CONCEPT_PROMPT_STYLE_ANCHOR = """\
=== STYLE ANCHOR — match this specificity; reject the generic failure mode ===

GENERIC (FAILS — could describe a thousand logos):
  "A modern, clean, professional logo for a coffee brand with a bean."

VIVID (TARGET — renderable, distinctive, craft-grounded):
  minimal variant:
  "A continuous single-weight 3u line in burnt sienna on warm cream; the line
   draws a coffee-bean crease that folds into the lowercase 'o' of a customised
   humanist-sans wordmark, so the letter and the bean share one stroke. Flat
   vector, matte, no gradient, 1x clear-space on a 1:1.618 grid; the negative
   space inside the 'o' doubles as rising steam."

WHY IT WORKS (the bar every variant must clear):
  - names EXACT colour + stroke weight + material + grid (renderable by any model)
  - ONE memory hook only this brand owns (the bean-that-is-the-letter)
  - leads with the strongest visual idea, not the brand name
  - zero generic adjectives ("modern/clean/professional" = automatic failure)
=== END STYLE ANCHOR ==="""


# ─── Create engine: concept-family visual-language style anchor ─────────
# Teaches concrete visual_language fields (forms/treatment/composition/palette)
# that name a system, not an adjective. Injected into CREATE_SYSTEM_PROMPT.
CREATE_STYLE_ANCHOR = """\
=== STYLE ANCHOR — visual_language must name a SYSTEM, not adjectives ===

GENERIC (FAILS): forms="geometric"; treatment="clean"; palette="blue and white"
VIVID (TARGET):
  forms      = "concentric circles on a 1:√2 grid; the outer ring opens into a
                notch at 2 o'clock"
  treatment  = "single-weight 4u strokes, butt joints, matte; no fills, no shadow"
  composition= "centred mark, 1.25x clear-space; wordmark below on shared baseline"
  palette    = "deep teal (#0F4C5C) dominant, warm sand (#E6B655) secondary,
                ivory (#F7F4EC) ground — depart from default finance blue"

RULE: if a visual_language field could apply to any brand in the category, it
is wrong. Name the specific system, weight, ratio, and hex-grounded palette.
=== END STYLE ANCHOR ==="""
