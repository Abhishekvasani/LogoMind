"""
LOGOS Contest Reader — the Contest Brief Decoder (Stage 3).

Freelancer.com (and similar) logo-contest briefs arrive as semi-structured free
text: "Company name: …", "Do you have colors in mind: …", "Anything to avoid:
…". Downstream engines (Discovery, Client Fit) do far better with clean,
structured signals than with raw prose. This engine normalises a pasted contest
brief into a ContestBrief — extracting company, industry, do's/don'ts, preferred
and avoided colors, style keywords, must-include/avoid elements, and references.

It produces a reading of what the contest holder asked for — not a creative
decision (FD-015). Missing fields are left empty rather than guessed, so the
persona engine never builds on fabricated requirements.
"""

import logging
from typing import Any, Dict

from pydantic import ValidationError

from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from ..schemas import ContestBrief

logger = logging.getLogger("logomind")

CONTEST_DECODE_SYSTEM_PROMPT = """You are LOGOS Contest Reader, the Contest Brief Decoder of LogoMind.

Your role: read a pasted logo-contest brief (e.g. from freelancer.com) and
extract its structured signals into a ContestBrief. You are doing information
EXTRACTION, not creative interpretation.

RULES:
- Extract ONLY what the brief actually states. Never invent colors, styles, or
  requirements that aren't in the text. If a field is absent, leave it empty.
- Map the brief's natural phrasing to the schema fields:
    "colors in mind" / "preferred colors"  -> colors_preferred
    "colors to avoid" / "do not use"        -> colors_avoided
    "style" / "look and feel"               -> style_keywords
    "ideas" / "must include" / "elements"   -> must_include
    "avoid" / "do not" / "anything else"    -> must_avoid / donts
    "sample logos" / "references" / "like"  -> references
    "tagline" / "slogan"                    -> tagline
- dos = explicit positive instructions; donts = explicit prohibitions.
- decoded_summary: ONE plain paragraph capturing the contest holder's intent in
  their own vocabulary (this feeds the client brief and persona).
- confidence: how complete/parseable the brief was (C5 = fully explicit,
  C1 = extremely thin / mostly unreadable).

Respond as JSON with EXACTLY this schema (field names verbatim; arrays of
short strings):
{
  "company_name": "string or null",
  "industry": "string or null",
  "tagline": "string or null",
  "dos": ["..."],
  "donts": ["..."],
  "colors_preferred": ["..."],
  "colors_avoided": ["..."],
  "style_keywords": ["..."],
  "must_include": ["..."],
  "must_avoid": ["..."],
  "references": ["..."],
  "decoded_summary": "one paragraph",
  "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
}

Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


def _normalize_contest_brief(data: Dict[str, Any]) -> Dict[str, Any]:
    """Defensively coerce model output to the ContestBrief shape.

    Lists occasionally come back as comma-strings or single strings; nullable
    fields as empty strings. Normalise so validation rarely fails.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object, got {type(data).__name__}.")
    out = dict(data)

    def _as_list(val: Any) -> list:
        if val is None:
            return []
        if isinstance(val, list):
            return [str(x).strip() for x in val if str(x).strip()]
        if isinstance(val, str):
            # comma-or-newline separated single string -> list
            parts = [p.strip() for p in val.replace("\n", ",").split(",") if p.strip()]
            return parts
        return [str(val)]

    for key in ("dos", "donts", "colors_preferred", "colors_avoided",
                "style_keywords", "must_include", "must_avoid", "references"):
        out[key] = _as_list(out.get(key))

    # Normalize nullable string fields: "" -> None.
    for key in ("company_name", "industry", "tagline"):
        v = out.get(key)
        if isinstance(v, str) and not v.strip():
            out[key] = None
        elif v is not None and not isinstance(v, str):
            out[key] = str(v)

    out.setdefault("decoded_summary", "Contest brief decoded; see structured fields.")
    out.setdefault("confidence", "C3")
    return out


async def decode_contest_brief(raw_text: str) -> ContestBrief:
    """Decode a pasted contest brief into a structured ContestBrief (Stage 3)."""
    if not raw_text or not raw_text.strip():
        raise ValueError("No contest text provided to decode.")

    orchestrator = get_ai_orchestrator()
    user_prompt = f"""CONTEST BRIEF (raw text — extract its signals; invent nothing):
{raw_text}
"""
    response = await orchestrator.complete(
        system_prompt=CONTEST_DECODE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.1,  # extraction — minimise creativity/variation
    )
    try:
        return ContestBrief(**_normalize_contest_brief(parse_json_response(response)))
    except (ValidationError, ValueError) as first_err:
        logger.warning("Contest decode first attempt failed (%s); retrying.", first_err.__class__.__name__)
        retry = await orchestrator.complete(
            system_prompt=CONTEST_DECODE_SYSTEM_PROMPT,
            user_prompt=user_prompt + (
                "\nReturn the COMPLETE JSON object with exactly these keys: "
                "company_name, industry, tagline, dos, donts, colors_preferred, "
                "colors_avoided, style_keywords, must_include, must_avoid, "
                "references, decoded_summary, confidence."
            ),
            response_format="json",
            temperature=0.1,
        )
        return ContestBrief(**_normalize_contest_brief(parse_json_response(retry)))


def contest_brief_to_enrichment(brief: ContestBrief) -> str:
    """Render a ContestBrief as a compact, readable enrichment block.

    Appended to the project's client_brief so Discovery/Strategy also benefit
    from the decoded contest signals (not just the persona).
    """
    parts = []
    if brief.tagline:
        parts.append(f"Tagline: {brief.tagline}")
    if brief.colors_preferred:
        parts.append(f"Preferred colors: {', '.join(brief.colors_preferred)}")
    if brief.colors_avoided:
        parts.append(f"Colors to avoid: {', '.join(brief.colors_avoided)}")
    if brief.style_keywords:
        parts.append(f"Style: {', '.join(brief.style_keywords)}")
    if brief.must_include:
        parts.append(f"Must include: {', '.join(brief.must_include)}")
    if brief.must_avoid:
        parts.append(f"Must avoid: {', '.join(brief.must_avoid)}")
    if brief.dos:
        parts.append(f"Do: {', '.join(brief.dos)}")
    if brief.donts:
        parts.append(f"Don't: {', '.join(brief.donts)}")
    if brief.references:
        parts.append(f"References/likes: {', '.join(brief.references)}")
    if not parts:
        return brief.decoded_summary
    return brief.decoded_summary + "\n\nDecoded contest requirements:\n" + "\n".join(parts)
