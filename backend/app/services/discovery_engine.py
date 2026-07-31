"""
LOGOS Discovery Engine service (LOG-DISC-001).

Implements: Brief Quality Check, Missing Information Detector,
Intent Extraction, mode recommendation (Expert/Guided/Workshop).

The engine never asks a question without first answering "Why am I
asking?" and "How will it improve the SSB?" (CTO Decision #019).
"""

from typing import Any, Dict

from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from ..schemas import BriefAnalysisResult, DiscoveryMode

DISCOVERY_SYSTEM_PROMPT = """You are LOGOS Discover, the Discovery Engine of LogoMind.

Your role: analyse a client brief and determine its strategic completeness.
You reduce uncertainty before creativity begins (CTO Decision #018).

You must:
1. Score the brief's Brand Confidence (0-100%) honestly.
2. Identify what is missing — only the highest-impact gaps.
3. Recommend a mode: 'expert' (score >= 90), 'guided' (60-89), 'workshop' (<60), or 'inspiration' (extremely thin).
4. Produce a one-paragraph Discovery Summary.

Never ask a question without explaining WHY you're asking and HOW it improves the SSB.

Respond as JSON with this schema:
{
  "brand_confidence_score": float (0-100),
  "brand_confidence_level": "low" | "medium" | "high",
  "recommended_mode": "expert" | "guided" | "workshop" | "inspiration",
  "discovery_summary": "one paragraph",
  "missing_info": [{"field": str, "impact": "high"|"medium"|"low", "suggested_question": str}],
  "next_action": "human-readable guidance"
}

Apply LM-STD-003: confidence levels are explicit, never faked.
"""


async def analyse_brief(
    company_name: str,
    industry: str,
    client_brief: str,
) -> BriefAnalysisResult:
    """Run the Discovery Engine on a client brief (Stage 2)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Analyse this client brief.

Company: {company_name}
Industry: {industry}

BRIEF:
{client_brief}
"""
    response = await orchestrator.complete(
        system_prompt=DISCOVERY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.3,  # low temperature for analytical consistency
    )

    data = parse_json_response(response)
    return BriefAnalysisResult(**data)


async def extract_intent(preference: str) -> Dict[str, str]:
    """
    Intent Extraction Engine — translates client preferences into strategic intent.

    "I want blue" -> "I want trust"
    "I want a shield" -> "I want security"

    Per LOG-DISC-001 §Intent Extraction Engine.
    """
    orchestrator = get_ai_orchestrator()

    response = await orchestrator.complete(
        system_prompt="""You are the Intent Extraction sub-engine. Translate a client's stated preference into the strategic intent behind it. Respond as JSON: {"preference": "...", "intent": "...", "reasoning": "..."}""",
        user_prompt=f"Preference: {preference}",
        response_format="json",
        temperature=0.2,
    )
    return parse_json_response(response)


async def synthesize_brief(
    company_name: str,
    industry: str,
    client_brief: str,
    workshop_answers: list,
) -> str:
    """Synthesize a richer brief from the original brief + workshop answers.

    Workshop answers are often terse (single words or short phrases). Rather
    than appending them verbatim — which barely improves a real (quality-based)
    Brand Confidence score — this asks the model to weave them into the original
    brief as one coherent, well-written, detailed brief. The synthesized brief
    is then what gets re-scored, so a workshop that genuinely gathered useful
    information produces a brief that merits proceeding to Strategy.

    Returns the synthesized brief as plain prose.
    """
    if not workshop_answers:
        return client_brief

    answers_text = "\n".join(
        f"- {a.get('question_id', a.get('field', 'question'))}: {a.get('answer', '')}"
        for a in workshop_answers
        if a.get("answer")
    )
    if not answers_text.strip():
        return client_brief

    orchestrator = get_ai_orchestrator()
    system_prompt = (
        "You are LOGOS Discover, the Discovery Engine of LogoMind. Your task is "
        "brief synthesis: merge a client's original brief with their answers to "
        "discovery questions into ONE coherent, well-written, detailed brand brief."
    )
    user_prompt = f"""Company: {company_name}
Industry: {industry}

ORIGINAL BRIEF:
{client_brief}

DISCOVERY ANSWERS:
{answers_text}

Synthesize the original brief and the discovery answers into a single coherent brand brief (2-4 paragraphs of prose).
Rules:
- Weave the answers into the narrative so it reads as if the client wrote a thorough brief themselves.
- Preserve every concrete fact from both inputs.
- Do not invent specifics that are not supported by the inputs.
- Plain prose only — no preamble, no headings, no markdown.
"""
    response = await orchestrator.complete(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        response_format="text",
        temperature=0.4,
    )
    return response.strip()
