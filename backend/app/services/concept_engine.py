"""
LOGOS Concept Prompt Engine service (LOG-CP-001).

Turns one evaluated Concept Family into an executable concept: a detailed
concept prompt (four variants + per-model adaptations), a composition
wireframe delivered as a structured spec, and a rationale trace.

The engine produces NO images and makes NO creative decision (FD-015). It
produces a strategy-grounded instrument the designer takes to their own
image tool. The wireframe is a structured spec — the LLM describes layout,
it never draws pixels (LOG-CP-001 §3) — so the front-end can render it
deterministically.
"""

import json
import logging
from typing import Any, Dict

from pydantic import ValidationError

from . import lic_knowledge
from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from ..schemas import ConceptPromptResult

logger = logging.getLogger("logomind")

CONCEPT_PROMPT_SYSTEM_PROMPT = (
    """You are LOGOS Concept Prompt, the executable concept engine.

Your role: transform ONE evaluated Concept Family into an executable concept
— a detailed concept prompt (four variants + per-model adaptations), a
composition wireframe spec, and a rationale trace — that the designer takes
to their own image model. You produce NO images and make NO creative
decision (FD-015). You produce a strategy-grounded instrument.

MISSION:
1. Distil the family + its judge evaluation into ONE core-concept sentence.
2. Generate EXACTLY FOUR concept-prompt variants, each a complete model-agnostic
   natural-language prompt, emphasising a different angle:
     - "minimal"          — fewest elements, maximum clarity, single-weight
     - "detailed"         — richer treatment, the family's full visual_language honoured
     - "typographic-led"  — the wordmark/lettering is the hero; symbol subordinate
     - "symbolic"         — the mark/symbol is the hero; typography subordinate
   Do NOT rank the variants. They are parallel starting points.
3. Provide model adaptations for ALL FIVE model families:
     midjourney, ideogram, stable-diffusion, recraft, general
   Each adaptation has a one-line tuning note and a concrete example_suffix
   (e.g. "--ar 1:1 --style raw" for midjourney). Model behaviour lives HERE,
   not in the variants — variants stay model-agnostic.
4. Compose the wireframe as STRUCTURED DATA, never as prose imagery or pixels.
   Use ONLY the closed vocabulary:
     orientation: horizontal | stacked | lockup | emblem
     alignment:   center | left | baseline-aligned
     element.kind:          symbol | wordmark | tagline | container | negative-space
     element.geometry:      circle | hexagon | rectangle | monogram | baseline-bar | custom
     element.position:      center | left-of-text | above | below | integrated
     element.relative_size: dominant | balanced | accent | small
   Give 2-4 elements. The spec MUST be renderable by a deterministic SVG renderer.
5. Trace the rationale to Brand DNA + the family's visual_language.
6. List the specific clichés (from Insight) deliberately NOT prompted.
7. Assign an honest confidence (LM-STD-003): how well-supported is this
   executable concept by the upstream strategy? Never fake it.

HARD RULES:
- Every variant's emphasis must trace to a Brand DNA meaning.
- Do NOT prompt clichés the Insight Report flags — re-express via combination.
- The wireframe must degrade recognisably at favicon size; say how (favicon_note).
- Do not assert one variant as "the answer" — present four parallel starts.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do
not nest or rename fields). Generate exactly four variants and five
model_adaptations:
{
  "family_label": "A",
  "core_concept": "one sentence",
  "variants": [
    {"style": "minimal", "prompt": "...", "intent": "..."},
    {"style": "detailed", "prompt": "...", "intent": "..."},
    {"style": "typographic-led", "prompt": "...", "intent": "..."},
    {"style": "symbolic", "prompt": "...", "intent": "..."}
  ],
  "model_adaptations": [
    {"model_family": "midjourney", "notes": "...", "example_suffix": "..."},
    {"model_family": "ideogram", "notes": "...", "example_suffix": "..."},
    {"model_family": "stable-diffusion", "notes": "...", "example_suffix": "..."},
    {"model_family": "recraft", "notes": "...", "example_suffix": "..."},
    {"model_family": "general", "notes": "...", "example_suffix": "..."}
  ],
  "wireframe": {
    "orientation": "horizontal | stacked | lockup | emblem",
    "balance": "...",
    "alignment": "center | left | baseline-aligned",
    "safe_margin": "...",
    "elements": [
      {"kind": "...", "geometry": "...", "position": "...", "relative_size": "...", "notes": "..."}
    ],
    "favicon_note": "..."
  },
  "rationale": "...",
  "cliches_avoided": ["..."],
  "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
}

Return ONLY the JSON object. No prose, no code fences, no commentary.
"""
    + lic_knowledge.knowledge_block(["RS-LIC-PH-005"])
)


# Common field-name aliases real models emit for this schema's fields. Maps an
# observed alias → the canonical schema field name. Used by the normalizer
# below so model drift doesn't cause validation failures (precedent:
# engines.py:_normalize_judge_output).
_FIELD_ALIASES: Dict[str, str] = {
    "model_adaption": "model_adaptations",
    "model_adaption_notes": "model_adaptations",
    "model_notes": "model_adaptations",
    "adaption": "model_adaptations",
    "adaptations": "model_adaptations",
    "wireframe_spec": "wireframe",
    "layout": "wireframe",
    "composition": "wireframe",
    "rationale_text": "rationale",
    "reasoning": "rationale",
    "explanation": "rationale",
    "cliches": "cliches_avoided",
    "cliche_avoided": "cliches_avoided",
    "avoided_cliches": "cliches_avoided",
    "concept": "core_concept",
    "core_idea": "core_concept",
}


def _normalize_concept_prompt(data: Any) -> Dict[str, Any]:
    """Defensively map model-emitted output onto the canonical schema shape.

    Real models occasionally (a) wrap the object in a single-element array,
    (b) rename keys (e.g. ``layout`` for ``wireframe``), or (c) collapse
    fields into surrounding prose. This unwraps a one-element list and hoists
    known aliases back to the schema names so the result validates.

    Raises ValueError for genuinely malformed shapes (multi-element lists,
    non-mappings) so the caller's retry can kick in. Does NOT invent missing
    content — if a required field is absent after mapping, validation raises.
    """
    # Some models wrap the single object in a list: [{...}] → {...}.
    if isinstance(data, list):
        if len(data) == 1 and isinstance(data[0], dict):
            data = data[0]
        else:
            raise ValueError(
                f"Expected a JSON object for one concept, got a {len(data)}-element list."
            )
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object for one concept, got {type(data).__name__}.")
    out = dict(data)
    for alias, canonical in _FIELD_ALIASES.items():
        if alias in out and canonical not in out:
            out[canonical] = out.pop(alias)
    return out


async def compose_concept_prompt(
    family: Dict[str, Any],
    judge_result: Dict[str, Any],
    brand_dna: Dict[str, Any],
    insight_report: Dict[str, Any],
) -> ConceptPromptResult:
    """Run the Concept Prompt Engine on ONE Concept Family (Stage: concept_prompt).

    Produces a model-ready concept: four prompt variants, per-model
    adaptations, a composition wireframe spec, rationale, and the clichés
    avoided. Generates no images; makes no creative decision (FD-015).

    Real models sometimes truncate the (long) JSON response mid-stream or use
    field-name aliases. On a validation failure we retry once with a higher
    token budget and a "finish the JSON" nudge; before each validation attempt
    we run the defensive normalizer.
    """
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Concept Family to execute:
{json.dumps(family, indent=2, default=str)}

Judge evaluation of this family:
{json.dumps(judge_result, indent=2, default=str)}

Brand DNA (the concept must trace to this):
{json.dumps(brand_dna, indent=2, default=str)}

Insight Report (clichés to avoid):
{json.dumps(insight_report, indent=2, default=str)}

Produce the executable concept for this family: four variants, five model
adaptations, the wireframe spec, rationale, and clichés avoided.
"""

    # First attempt: standard budget. The schema is large, so allow generous
    # output tokens to reduce the chance of mid-JSON truncation.
    response = await orchestrator.complete(
        system_prompt=CONCEPT_PROMPT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.7,  # between Create (0.8) and Judge (0.3): creative but structured
        max_tokens=2400,
    )

    try:
        return ConceptPromptResult(**_normalize_concept_prompt(parse_json_response(response)))
    except (ValidationError, ValueError) as first_err:
        # Retry once with a larger budget and an explicit completion nudge —
        # handles truncation (the most common real-model failure for big JSON).
        logger.warning("Concept Prompt first attempt failed (%s); retrying with larger budget.", first_err.__class__.__name__)
        retry_prompt = user_prompt + (
            "\nIMPORTANT: Your previous response was incomplete or used unexpected "
            "field names. Return the COMPLETE JSON object in ONE go with EXACTLY "
            "these top-level keys: family_label, core_concept, variants, "
            "model_adaptations, wireframe, rationale, cliches_avoided, confidence. "
            "Do not omit wireframe or rationale. Keep each variant prompt concise "
            "(2-3 sentences) so the whole object fits."
        )
        response = await orchestrator.complete(
            system_prompt=CONCEPT_PROMPT_SYSTEM_PROMPT,
            user_prompt=retry_prompt,
            response_format="json",
            temperature=0.6,  # slightly lower for a more compliant second pass
            max_tokens=3200,
        )
        return ConceptPromptResult(**_normalize_concept_prompt(parse_json_response(response)))

