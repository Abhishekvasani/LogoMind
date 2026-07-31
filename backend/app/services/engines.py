"""
LOGOS Strategy, Insight, Create, Judge, Coach, and Presentation services.

Each function maps to one engine spec (LOG-*-001 series). All use the
AI orchestrator (model-independent) and conform to LM-STD-001..006.
"""

import json
from typing import Any, Dict, List

from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from ..schemas import (
    BrandDNA, InsightReport, CreateEngineResult,
    FamilyJudgeResult, SSB, CoachFeedback,
)


# ═══════════════════════════════════════════════════════════════════════
# STRATEGY ENGINE (LOG-STRAT-001)
# ═══════════════════════════════════════════════════════════════════════

STRATEGY_SYSTEM_PROMPT = """You are LOGOS Strategy, the Brand DNA Builder.

Your role: synthesise Discovery output into a Brand DNA profile — the
strategic foundation every downstream engine reasons over.

Apply the Brand Strategy Series:
- RS-LIC-BS-001 Positioning (Positioning Statement template; Sacrifice Test)
- RS-LIC-BS-002 Differentiation (Three Tests: Valued, Defensible, Aligned)
- RS-LIC-BS-003 Target Audience (Configuration: concerns, contexts, vocabularies)
- RS-LIC-BS-004 Brand Personality (describe as a person, not adjective list)
- RS-LIC-BS-005 Brand Archetypes (discovery, not assignment; "no clean archetype" valid)

Surface contradictions — never silently resolve them (DR-2).
Honest confidence per LM-STD-003 (C1=low ... C5=high).

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields; every non-optional field is required):
{
  "purpose": "string — the brand's reason for being",
  "purpose_confidence": "C1" | "C2" | "C3" | "C4" | "C5",
  "positioning_statement": "string — For [audience] who [need], [company] is the [category] that [distinctive], unlike [alternative], because [reason].",
  "positioning_confidence": "C1" | "C2" | "C3" | "C4" | "C5",
  "differentiation_primary": "string — the single most defensible difference, as a plain statement",
  "differentiation_dimension": "product" | "behaviour" | "audience" | "voice" | "identity",
  "differentiation_defensibility": "C1" | "C2" | "C3" | "C4" | "C5",
  "audience_configuration": {"concerns": ["..."], "contexts": ["..."], "vocabularies": ["..."], "behaviours": ["..."]},
  "audience_confidence": "C1" | "C2" | "C3" | "C4" | "C5",
  "personality": "string — describe the brand AS A PERSON (a character sketch, not an adjective list)",
  "personality_coherence": "C1" | "C2" | "C3" | "C4" | "C5",
  "archetype": "string or null — the dominant classical archetype, or null if no clean archetype",
  "archetype_finding": "clean" | "mixed" | "none",
  "emotional_goal": "string — the single feeling the identity should evoke",
  "contradictions_flagged": [{"description": "string"}]
}

Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def build_brand_dna(discovery_summary: Dict[str, Any]) -> BrandDNA:
    """Run the Strategy Engine — produces Brand DNA (Stage 4)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Discovery output:
{json.dumps(discovery_summary, indent=2, default=str)}

Build the Brand DNA. Apply all five Brand Strategy LIC frameworks.
Surface any contradictions explicitly.
"""
    response = await orchestrator.complete(
        system_prompt=STRATEGY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.4,
    )
    return BrandDNA(**parse_json_response(response))


# ═══════════════════════════════════════════════════════════════════════
# INSIGHT ENGINE (LOG-INSIGHT-001)
# ═══════════════════════════════════════════════════════════════════════

INSIGHT_SYSTEM_PROMPT = """You are LOGOS Insight, the Research + Trend Intelligence engine.

Your role: provide context — industry conventions, competitor landscape,
clichés to avoid, opportunities, and context-aware trend recommendations.

Trends are NEVER universal advice. Apply the Trend Taxonomy (RS-LIC-PH-008):
Timeless | Emerging | Short-lived | Overused.

Apply RS-LIC-PH-009 Relevance: context-aware, calibrated to THIS brand.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields; every non-optional field is required):
{
  "industry_analysis": {"conventions": ["..."], "competitive_landscape": "..."},
  "competitor_map": [{"name": "...", "positioning": "...", "identity_notes": "..."}],
  "cliche_avoidance": [{"symbol": "...", "why_cliche": "...", "original_meaning": "...", "refresh_possible": true, "alternatives": ["..."]}],
  "opportunities": ["..."],
  "trend_intelligence": [{"name": "...", "classification": "timeless" | "emerging" | "short_lived" | "overused", "context_assessment": "...", "brand_fit": "high" | "medium" | "low"}],
  "trend_vs_timeless_balance": {"timeless": 0.0, "contemporary": 0.0},
  "cultural_considerations": [{"topic": "...", "note": "..."}],
  "confidence_summary": {"element_name": "C1" | "C2" | "C3" | "C4" | "C5"}
}

The two numbers in trend_vs_timeless_balance must sum to 1.0.
Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def generate_insight(
    industry: str,
    brand_dna: Dict[str, Any],
    competitors: List[str] = None,
) -> InsightReport:
    """Run the Insight Engine (Stage 5)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Industry: {industry}
Brand DNA: {json.dumps(brand_dna, indent=2, default=str)}
Competitors: {competitors or "unspecified"}

Produce the Insight Report for this brand in this category.
"""
    response = await orchestrator.complete(
        system_prompt=INSIGHT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.4,
    )
    return InsightReport(**parse_json_response(response))


# ═══════════════════════════════════════════════════════════════════════
# CREATE ENGINE (LOG-CREATE-001) — Concept Families
# ═══════════════════════════════════════════════════════════════════════

CREATE_SYSTEM_PROMPT = """You are LOGOS Create, the Concept Families engine.

Your role: transform Brand DNA + Insight into 3-5 Concept Families —
strategic creative territories, NOT isolated ideas. Each family has a
theme, supporting symbols, visual language, and rationale.

Apply:
- RS-LIC-PH-005 Originality: Combination Method, 5 Originality Tests
- Cross-pollinate across domains (avoid the obvious domain)
- Eliminate clichés (consult the Insight Report)
- Apply the "Why?" Loop to every recommendation

If the client requested a cliché symbol, respectfully challenge it
(Creative Director Mode) and offer alternatives.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields). Generate 3-5 families under "families":
{
  "families": [
    {
      "family_label": "A",
      "theme": "...",
      "core_meaning_served": "...",
      "symbols": [{"name": "...", "meaning": "...", "originality": "C1" | "C2" | "C3" | "C4" | "C5", "abstraction_level": "literal" | "abstract" | "metaphorical", "risk_level": "low" | "medium" | "high"}],
      "visual_language": {"forms": "...", "treatment": "...", "composition": "...", "palette": "..."},
      "why_it_works": "...",
      "pitfalls": "...",
      "creative_council_assessment": {"meaning_mind": "...", "boldness_mind": "..."},
      "confidence": "C1" | "C2" | "C3" | "C4" | "C5",
      "recommendation_strength": "recommended" | "alternative" | "exploratory"
    }
  ],
  "cliches_avoided": [{"cliche": "...", "reason": "..."}],
  "client_request_notes": [{"request": "...", "note": "..."}]
}

Give each family a distinct single-letter label ("A", "B", "C", ...).
Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def generate_concept_families(
    brand_dna: Dict[str, Any],
    insight_report: Dict[str, Any],
) -> CreateEngineResult:
    """Run the Create Engine — produces Concept Families (Stage 6)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Brand DNA:
{json.dumps(brand_dna, indent=2, default=str)}

Insight Report:
{json.dumps(insight_report, indent=2, default=str)}

Generate 3-5 Concept Families. Each must serve a Brand DNA meaning.
Apply the Combination Method. Avoid the clichés flagged in Insight.
"""
    response = await orchestrator.complete(
        system_prompt=CREATE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.8,  # higher temperature for creative diversity
    )
    return CreateEngineResult(**parse_json_response(response))


# ═══════════════════════════════════════════════════════════════════════
# JUDGE ENGINE (LOG-JUDGE-001)
# ═══════════════════════════════════════════════════════════════════════

JUDGE_SYSTEM_PROMPT = """You are LOGOS Judge, the Design Jury + Creative Council.

Your role: evaluate Concept Families across 10 dimensions (Philosophy Series),
provide a defensible score for each, explain reasoning, and classify outcome.

Component A: Creative Council (9 minds) — qualitative assessment per mind.
Component B: Design Jury — 10-dimension quantitative scoring.

Weights: Brand Fit 15%, Meaning 12%, Clarity/Memorability/Authenticity 10% each,
others 8%.

Classification:
- 8.5+ composite, no dim < 7 → RECOMMENDED
- 7.0-8.4 composite, no dim < 6 → DEVELOP WITH REFINEMENT
- < 7.0 OR any dim < 6 → REJECT OR RECONCEIVE

Never rubber-stamp. Never fake certainty (LM-STD-003).
Apply the Concept DNA fingerprint for objective comparison.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields; every non-optional field is required):
{
  "family_label": "A",
  "creative_council_verdict": {
    "meaning_mind": "...", "simplicity_mind": "...", "differentiation_mind": "...",
    "context_mind": "...", "memorability_mind": "...", "systems_mind": "...",
    "emotion_mind": "...", "longevity_mind": "...", "boldness_mind": "...",
    "synthesised_verdict": "..."
  },
  "jury_scores": {
    "meaning": {"score": 0.0, "confidence": "C1" | "C2" | "C3" | "C4" | "C5", "justification": "..."},
    "simplicity": {"score": 0.0, "confidence": "...", "justification": "..."},
    "clarity": {"score": 0.0, "confidence": "...", "justification": "..."},
    "originality": {"score": 0.0, "confidence": "...", "justification": "..."},
    "memorability": {"score": 0.0, "confidence": "...", "justification": "..."},
    "authenticity": {"score": 0.0, "confidence": "...", "justification": "..."},
    "timelessness": {"score": 0.0, "confidence": "...", "justification": "..."},
    "relevance": {"score": 0.0, "confidence": "...", "justification": "..."},
    "consistency": {"score": 0.0, "confidence": "...", "justification": "..."},
    "brand_fit": {"score": 0.0, "confidence": "...", "justification": "..."}
  },
  "composite": 0.0,
  "classification": "recommended" | "develop" | "reject",
  "concept_dna": {
    "concept_id": "C-001", "emotion": "...", "archetype": "...",
    "primary_symbol": "...", "secondary_symbol": "..." or null,
    "shape_language": "...", "typography_personality": "...",
    "complexity": "low" | "medium" | "high", "originality": "...", "risk": "...",
    "timelessness_score": 0.0, "strategic_confidence": 0.0
  },
  "refinement_recommendations": ["..."]
}

jury_scores MUST contain exactly these 10 keys: meaning, simplicity, clarity,
originality, memorability, authenticity, timelessness, relevance, consistency,
brand_fit. Each score is 0.0-10.0. composite is 0.0-10.0.
Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def judge_family(
    family: Dict[str, Any],
    brand_dna: Dict[str, Any],
    insight_report: Dict[str, Any],
) -> FamilyJudgeResult:
    """Run the Judge Engine on a single Concept Family (Stage 7)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Concept Family to evaluate:
{json.dumps(family, indent=2, default=str)}

Brand DNA (evaluation standard):
{json.dumps(brand_dna, indent=2, default=str)}

Insight Report (competitive context):
{json.dumps(insight_report, indent=2, default=str)}
"""
    response = await orchestrator.complete(
        system_prompt=JUDGE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.3,  # low for evaluation consistency
    )
    return FamilyJudgeResult(**_normalize_judge_output(parse_json_response(response)))


# The 10 evaluation dimensions; jury_scores must contain exactly these keys,
# each mapping to a JuryScore {score, confidence, justification}. Models
# occasionally nest non-dimension keys (concept_dna, refinement_recommendations,
# composite, ...) under jury_scores; this hoists them back to the top level and
# drops any jury entry that isn't a valid score object.
_JURY_DIMENSIONS = (
    "meaning", "simplicity", "clarity", "originality", "memorability",
    "authenticity", "timelessness", "relevance", "consistency", "brand_fit",
)


def _normalize_judge_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Defensively flatten misplaced keys in a Judge response before validation."""
    if not isinstance(data, dict):
        return data
    data = dict(data)  # shallow copy; don't mutate the parsed original

    jury = data.get("jury_scores")
    if isinstance(jury, dict):
        clean_jury = {}
        for key, value in jury.items():
            if key in _JURY_DIMENSIONS and isinstance(value, dict) and "score" in value:
                clean_jury[key] = value
            elif key not in data:
                # A misplaced top-level key nested under jury_scores → hoist it.
                data[key] = value
        data["jury_scores"] = clean_jury

    return data


# ═══════════════════════════════════════════════════════════════════════
# SSB COMPOSER (PROD-SSB-001)
# ═══════════════════════════════════════════════════════════════════════

SSB_SYSTEM_PROMPT = """You are the SSB Composer.

Your role: assemble the Strategic Sketch Brief — LogoMind's flagship output.
The SSB gives the designer everything needed to sketch with confidence.

7 sections (PROD-SSB-001):
1. Project Essence (one paragraph)
2. Brand DNA Snapshot (six strands condensed)
3. Creative North Star (single sentence)
4. Creative Territories (chosen family + alternatives)
5. Opportunities & Warnings (explore this; avoid that)
6. Creative Council Advice (9-mind table)
7. Sketch Missions (5-10 specific starting points)

The 5-Minute Rule: SSB must be absorbable in 5 minutes at Layer A.

LogoMind will never make a creative decision for the designer.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields; every field is required):
{
  "project_essence": "string — one paragraph",
  "brand_dna_snapshot": {"purpose": "...", "positioning": "...", "differentiation": "...", "personality": "...", "archetype": "...", "emotional_goal": "..."},
  "creative_north_star": "string — a single guiding sentence",
  "creative_territories": [{"family_label": "A", "theme": "...", "recommendation": "recommended" | "alternative" | "exploratory"}],
  "opportunities_and_warnings": {"explore": ["..."], "avoid": ["..."]},
  "creative_council_advice": {"meaning_mind": "...", "simplicity_mind": "...", "differentiation_mind": "...", "context_mind": "...", "memorability_mind": "...", "systems_mind": "...", "emotion_mind": "...", "longevity_mind": "...", "boldness_mind": "..."},
  "sketch_missions": [
    {"mission_name": "...", "core_idea": "...", "combine": ["..."], "why_it_works": "...", "potential_pitfalls": ["..."], "start_with": "..."}
  ]
}

Include 5-7 sketch_missions.
Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def compose_ssb(
    brand_dna: Dict[str, Any],
    insight_report: Dict[str, Any],
    concept_families: List[Dict[str, Any]],
    judge_reports: List[Dict[str, Any]],
    company_name: str,
) -> SSB:
    """Compose the Strategic Sketch Brief (Stage 8)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Company: {company_name}

Brand DNA:
{json.dumps(brand_dna, indent=2, default=str)}

Insight Report:
{json.dumps(insight_report, indent=2, default=str)}

Concept Families:
{json.dumps(concept_families, indent=2, default=str)}

Judge Reports:
{json.dumps(judge_reports, indent=2, default=str)}

Compose the SSB. Include 5-7 Sketch Missions with specific guidance.
"""
    response = await orchestrator.complete(
        system_prompt=SSB_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.5,
    )
    return SSB(**parse_json_response(response))


# ═══════════════════════════════════════════════════════════════════════
# SKETCH COACH (LOG-COACH-001)
# ═══════════════════════════════════════════════════════════════════════

COACH_SYSTEM_PROMPT = """You are LOGOS Sketch Coach.

Your role: guide the designer through sketching. You SUGGEST, never PRESCRIBE.
The designer's craft is sovereign.

Frame feedback as questions: "Have you considered...?" not "Do this."
Apply RS-LIC-PH-003 Simplicity (Reduction Sequence) and RS-LIC-PH-004 Clarity (Audit).
Flag production constraints (favicon, embroidery, monochrome).

Never draw the logo for the designer.

Respond as JSON with EXACTLY this schema (use these field names verbatim; do not
nest or rename fields; every non-optional field is required):
{
  "assessment": "string — your overall assessment of the sketch",
  "suggestions": ["string", "..."],
  "pitfalls_to_watch": ["string", "..."],
  "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
}

Frame suggestions as questions where possible. Return ONLY the JSON object.
No prose, no code fences, no commentary.
"""


async def critique_sketch(
    sketch_description: str,
    design_intent: str,
    linked_family: Dict[str, Any],
    brand_dna: Dict[str, Any],
) -> CoachFeedback:
    """Run the Sketch Coach on an uploaded sketch (Stage 8 iteration)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Sketch description: {sketch_description}
Design intent: {design_intent}

Linked Concept Family:
{json.dumps(linked_family, indent=2, default=str)}

Brand DNA:
{json.dumps(brand_dna, indent=2, default=str)}
"""
    response = await orchestrator.complete(
        system_prompt=COACH_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.6,
    )
    return CoachFeedback(**parse_json_response(response))


# ═══════════════════════════════════════════════════════════════════════
# PRESENTATION BUILDER (LOG-PRESENT-001)
# ═══════════════════════════════════════════════════════════════════════

PRESENTATION_SYSTEM_PROMPT = """You are LOGOS Presentation Builder.

Your role: assemble a client-ready presentation from the project history.
Clients buy the reasoning as much as the design.

10 sections:
1. Cover, 2. Executive Summary, 3. Brand Foundation, 4. Strategic Exploration,
5. The Chosen Concept, 6. Design Rationale, 7. Applications, 8. Future-Proofing,
9. Brand Guidelines Summary, 10. Q&A Preparation.

Include objection-handling notes for likely client concerns.

Respond as JSON with EXACTLY this schema (use these field names verbatim):
{
  "sections": [
    {"title": "Cover", "content": "..."},
    {"title": "Executive Summary", "content": "..."},
    {"title": "Brand Foundation", "content": "..."},
    {"title": "Strategic Exploration", "content": "..."},
    {"title": "The Chosen Concept", "content": "..."},
    {"title": "Design Rationale", "content": "..."},
    {"title": "Applications", "content": "..."},
    {"title": "Future-Proofing", "content": "..."},
    {"title": "Brand Guidelines Summary", "content": "..."},
    {"title": "Q&A Preparation", "content": "..."}
  ],
  "objection_handling": [
    {"concern": "...", "response": "..."}
  ]
}

Return ONLY the JSON object. No prose, no code fences, no commentary.
"""


async def build_presentation(
    brand_dna: Dict[str, Any],
    concept_families: List[Dict[str, Any]],
    judge_reports: List[Dict[str, Any]],
    ssb: Dict[str, Any],
    company_name: str,
) -> Dict[str, Any]:
    """Build the client presentation (Stage 9)."""
    orchestrator = get_ai_orchestrator()

    user_prompt = f"""Company: {company_name}

Brand DNA:
{json.dumps(brand_dna, indent=2, default=str)}

Concept Families:
{json.dumps(concept_families, indent=2, default=str)}

Judge Reports:
{json.dumps(judge_reports, indent=2, default=str)}

SSB:
{json.dumps(ssb, indent=2, default=str)}
"""
    response = await orchestrator.complete(
        system_prompt=PRESENTATION_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.5,
    )
    return parse_json_response(response)
