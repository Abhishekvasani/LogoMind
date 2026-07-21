"""
LOGOS Discovery Engine service (LOG-DISC-001).

Implements: Brief Quality Check, Missing Information Detector,
Intent Extraction, mode recommendation (Expert/Guided/Workshop).

The engine never asks a question without first answering "Why am I
asking?" and "How will it improve the SSB?" (CTO Decision #019).
"""

import json
from typing import Any, Dict

from .ai_orchestrator import get_ai_orchestrator
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

    data = json.loads(response)
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
    return json.loads(response)
