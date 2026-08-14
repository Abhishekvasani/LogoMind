"""
LOGOS Strategy, Insight, Create, Judge, Coach, and Presentation services.

Each function maps to one engine spec (LOG-*-001 series). All use the
AI orchestrator (model-independent) and conform to LM-STD-001..006.
"""

import json
from typing import Any, Dict, List, Optional

from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from . import lic_knowledge
from . import _exemplars
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
""" + lic_knowledge.knowledge_block([
    "RS-LIC-BS-001", "RS-LIC-BS-002", "RS-LIC-BS-003", "RS-LIC-BS-004", "RS-LIC-BS-005",
])


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
""" + lic_knowledge.knowledge_block([
    "RS-LIC-PH-008", "RS-LIC-PH-009", "RS-LIC-SY-VOLUME", "RS-LIC-IND-VOLUME",
])


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
    return InsightReport(**_normalize_insight_output(parse_json_response(response)))


def _normalize_insight_output(data: Dict[str, Any]) -> Dict[str, Any]:
    """Defensively repair common real-model drift in an Insight response.

    Real models occasionally (a) rename ``trend_vs_timeless_balance`` to a
    near-synonym or (b) omit it entirely while still producing the rest of the
    report. ``trend_vs_timeless_balance`` is the only *required* field without a
    default, so a missing/emitted-under-an-alias value fails validation. This
    maps known aliases back and, if still absent, derives a balanced default
    from ``trend_intelligence`` classifications so the report validates.

    Precedent: ``_normalize_judge_output`` does the same for the Judge engine.
    """
    if not isinstance(data, dict):
        return data
    data = dict(data)

    # Map common aliases for the required balance field.
    balance_aliases = (
        "trend_balance",
        "timeless_vs_trend_balance",
        "trend_timeless_balance",
        "balance",
        "timelessness_balance",
    )
    if "trend_vs_timeless_balance" not in data:
        for alias in balance_aliases:
            if alias in data and isinstance(data[alias], dict):
                data["trend_vs_timeless_balance"] = data.pop(alias)
                break

    # If still missing, derive a neutral balance from trend classifications.
    if "trend_vs_timeless_balance" not in data:
        trends = data.get("trend_intelligence") or []
        timeless = sum(1 for t in trends if isinstance(t, dict) and t.get("classification") == "timeless")
        contemporary = sum(
            1 for t in trends
            if isinstance(t, dict) and t.get("classification") in ("emerging", "short_lived", "overused")
        )
        total = timeless + contemporary
        if total > 0:
            data["trend_vs_timeless_balance"] = {
                "timeless": round(timeless / total, 2),
                "contemporary": round(contemporary / total, 2),
            }
        else:
            # No trend data to derive from — use a balanced neutral default.
            data["trend_vs_timeless_balance"] = {"timeless": 0.5, "contemporary": 0.5}

    return data



# ═══════════════════════════════════════════════════════════════════════
# CREATE ENGINE (LOG-CREATE-001) — Concept Families
# ═══════════════════════════════════════════════════════════════════════

CREATE_SYSTEM_PROMPT = (
    """You are LOGOS Create, the Concept Families engine.

Your role: transform Brand DNA + Insight into 3-5 Concept Families —
strategic creative territories, NOT isolated ideas. Each family has a
theme, supporting symbols, a CONCRETE visual language, and rationale.

METHOD (apply the injected knowledge literally):
- Use the Combination Method: establish meaning → gather inputs from the
  meaning's domain AND adjacent domains → cross-pollinate → combine → test.
- Use the Cross-Pollination table to reach PAST the obvious domain. For each
  meaning, prefer adjacent-domain inputs (higher originality) over obvious ones.
- Filter every symbol against the Symbol Library: an 🟠/🔴 originality risk
  REQUIRES an explicit refresh/abstraction justification. Do NOT propose a
  symbol the library says to "Avoid When" the category matches — unless you
  explicitly reframe it (and say how).
- Each family must pass the 5 Originality Tests (Meaning, Distinctiveness,
  Clarity, Inevitability, Non-Arbitrary); state which adjacent inputs combine.
- Eliminate clichés (consult the Insight Report's cliche_avoidance).

ANTI-GENERIC DIRECTIVE — the difference between forgettable and memorable:
- BEFORE generating, name the 3 most generic/obvious solutions for THIS brief
  (e.g. "a leaf for eco", "a shield for security", "blue for tech"). Every
  family MUST visibly depart from all three; state how.
- Each family must commit to ONE distinctive memory hook — the single detail a
  viewer recalls an hour later (a negative-space reveal, an unexpected
  proportion, a material treatment, a bespoke letterform quirk). Name it.
- Choose colour and typography FROM the injected Color and Typography volumes,
  not from habit. A 🔴/🟠 originality-risk choice (sea-of-blue, default
  Helvetica/Inter, eco-leaf-green) requires an explicit refresh justification.
- Write in sensory/material language, never vague adjectives. "Single-weight 2u
  strokes, matte, on warm sand; wordmark set in a customised old-style serif" —
  NOT "clean, modern, professional". Adjective-only descriptions are failure.

VISUAL LANGUAGE must be concrete, not one-word:
- forms: name a geometric/organic system (e.g. "concentric circles on a 1:√2 grid")
- treatment: stroke weight / finish logic (e.g. "single-weight 2u strokes, matte")
- composition: layout + clear space (e.g. "centred mark, 1x clear-space on all sides")
- palette: 3-4 named colours with a dominant/secondary split (e.g. "deep teal dominant, warm sand secondary, ivory accent")

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
    + lic_knowledge.knowledge_block([
        "RS-LIC-PH-005", "RS-LIC-SY-VOLUME",
        "RS-LIC-CL-VOLUME", "RS-LIC-TY-VOLUME", "RS-LIC-ID-VOLUME",
        "RS-LIC-IND-VOLUME",
    ])
    + "\n\n" + _exemplars.CREATE_STYLE_ANCHOR
)


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

JUDGE_SYSTEM_PROMPT = (
    """You are LOGOS Judge, the Design Jury + Creative Council.

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

For the `originality` dimension, score against the 5 Originality Tests injected
below (Meaning, Distinctiveness, Clarity, Inevitability, Non-Arbitrary): the
justification must state which tests the concept passes/fails.

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
    # Ground the craft dimensions with their canonical audits/tests: originality
    # (PH-005), simplicity (PH-003), clarity (PH-004), memorability (PH-006),
    # timelessness (PH-008). The remaining dimensions are judged from context.
    + lic_knowledge.knowledge_block([
        "RS-LIC-PH-005", "RS-LIC-PH-003", "RS-LIC-PH-004", "RS-LIC-PH-006", "RS-LIC-PH-008",
    ])
)


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
6. Creative Council Advice (9-mind table + synthesised verdict)
7. Sketch Missions (5-10 specific starting points)

GROUNDING RULES (critical):
- The chosen territory is GIVEN to you in the user prompt (SELECTED TERRITORY).
  Populate selected_territory from it — carry its visual_language, symbols,
  composite, classification, and concept_dna through verbatim. Do NOT invent a
  different chosen territory.
- Every sketch_mission.combine[] entry MUST be a symbol drawn from the selected
  territory's symbols. Do not introduce symbols the family does not own.
- Ground each mission's why_it_works in the jury's refinement_recommendations
  and the concept_dna fingerprint for the selected territory.
- creative_council_advice.synthesised_verdict MUST come from the selected
  territory's judge verdict.

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
  ],
  "selected_territory": {
    "family_label": "A", "theme": "...", "recommendation": "...", "core_meaning_served": "...",
    "why_it_works": "...", "pitfalls": "...", "composite": 0.0, "classification": "...",
    "visual_language": {"forms": "...", "treatment": "...", "composition": "...", "palette": "..."},
    "symbols": [{"name": "...", "meaning": "..."}],
    "concept_dna": {"emotion": "...", "primary_symbol": "...", "shape_language": "..."},
    "refinement_recommendations": ["..."]
  },
  "council_advice": {
    "meaning_mind": "...", "simplicity_mind": "...", "differentiation_mind": "...",
    "context_mind": "...", "memorability_mind": "...", "systems_mind": "...",
    "emotion_mind": "...", "longevity_mind": "...", "boldness_mind": "...",
    "synthesised_verdict": "..."
  }
}

Include 5-7 sketch_missions. start_with must be concrete, actionable guidance
(e.g. "Begin with a circular grid; sketch 10 keystone variations; test at 16px").
Return ONLY the JSON object. No prose, no code fences, no commentary.
""" + lic_knowledge.knowledge_block(["RS-LIC-ID-VOLUME"])


def _select_chosen_family(
    concept_families: List[Dict[str, Any]],
    judge_reports: List[Dict[str, Any]],
    selected_family_label: Optional[str],
) -> tuple:
    """Resolve the chosen family + its judge result + the alternatives.

    Selection order: explicit label → highest-composite family → first.
    Returns (chosen_family, chosen_judge, alternative_families).
    """
    def _label_of(fam):
        return fam.get("family_label") if isinstance(fam, dict) else None

    chosen = None
    if selected_family_label:
        chosen = next((f for f in concept_families if _label_of(f) == selected_family_label), None)
    if chosen is None and judge_reports:
        # Pick the highest-composite family.
        ranked = sorted(
            judge_reports,
            key=lambda j: j.get("composite", 0) if isinstance(j, dict) else 0,
            reverse=True,
        )
        if ranked:
            top_label = ranked[0].get("family_label") if isinstance(ranked[0], dict) else None
            chosen = next((f for f in concept_families if _label_of(f) == top_label), None)
    if chosen is None and concept_families:
        chosen = concept_families[0]

    chosen_label = _label_of(chosen)
    chosen_judge = next((j for j in judge_reports if isinstance(j, dict) and j.get("family_label") == chosen_label), None)
    alternatives = [f for f in concept_families if _label_of(f) != chosen_label]
    return chosen or {}, chosen_judge or {}, alternatives


def _anchor_selected_territory(data: Dict[str, Any], chosen_family: Dict[str, Any], chosen_judge: Dict[str, Any]) -> Dict[str, Any]:
    """Force selected_territory to carry the ACTUAL persisted family/judge data.

    The model may paraphrase; this guarantees truthfulness by overlaying the
    real visual_language, symbols, composite, classification, concept_dna, and
    refinement_recommendations from the persisted Create/Judge output.
    """
    territory = data.get("selected_territory") or {}
    territory["family_label"] = chosen_family.get("family_label", territory.get("family_label"))
    territory["theme"] = chosen_family.get("theme", territory.get("theme"))
    territory.setdefault("recommendation", chosen_family.get("recommendation_strength", "alternative"))
    territory["core_meaning_served"] = chosen_family.get("core_meaning_served", territory.get("core_meaning_served"))
    territory["why_it_works"] = chosen_family.get("why_it_works", territory.get("why_it_works"))
    territory["pitfalls"] = chosen_family.get("pitfalls", territory.get("pitfalls"))
    territory["visual_language"] = chosen_family.get("visual_language", territory.get("visual_language") or {})
    territory["symbols"] = chosen_family.get("symbols", territory.get("symbols") or [])
    if chosen_judge:
        territory["composite"] = chosen_judge.get("composite", territory.get("composite"))
        territory["classification"] = chosen_judge.get("classification", territory.get("classification"))
        territory["concept_dna"] = chosen_judge.get("concept_dna", territory.get("concept_dna"))
        territory["refinement_recommendations"] = chosen_judge.get("refinement_recommendations", territory.get("refinement_recommendations") or [])
    data["selected_territory"] = territory
    return data


async def compose_ssb(
    brand_dna: Dict[str, Any],
    insight_report: Dict[str, Any],
    concept_families: List[Dict[str, Any]],
    judge_reports: List[Dict[str, Any]],
    company_name: str,
    selected_family_label: Optional[str] = None,
) -> SSB:
    """Compose the Strategic Sketch Brief (Stage 8)."""
    orchestrator = get_ai_orchestrator()

    chosen, chosen_judge, alternatives = _select_chosen_family(
        concept_families, judge_reports, selected_family_label
    )

    # Focused context — NOT a raw full-list dump. The chosen family + its judge
    # result are inlined so the model grounds missions in them; alternatives are
    # summarised to one line each to keep the prompt small.
    alt_summary = [
        f"{f.get('family_label', '?')} — {f.get('theme', '')} — {f.get('recommendation_strength', '')}"
        for f in alternatives
    ]

    user_prompt = f"""Company: {company_name}

Brand DNA:
{json.dumps(brand_dna, indent=2, default=str)}

Insight Report (clichés + opportunities):
{json.dumps(insight_report, indent=2, default=str)}

SELECTED TERRITORY (the designer chose this — populate selected_territory from it):
{json.dumps(chosen, indent=2, default=str)}

SELECTED TERRITORY JUDGE RESULT (carry composite, classification, concept_dna,
council verdict, and refinement_recommendations into the SSB):
{json.dumps(chosen_judge, indent=2, default=str)}

ALTERNATIVE TERRITORIES (list under creative_territories with reduced detail):
{chr(10).join(alt_summary) or '(none)'}

Compose the SSB. selected_territory and council_advice MUST be populated from
the SELECTED TERRITORY + its judge result above. Every sketch_mission.combine[]
entry MUST be a symbol from the selected territory's symbols. Include 5-7
Sketch Missions with concrete, actionable start_with guidance.
"""
    response = await orchestrator.complete(
        system_prompt=SSB_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.5,
    )
    data = parse_json_response(response)
    data = _anchor_selected_territory(data, chosen, chosen_judge)
    return SSB(**data)


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
""" + lic_knowledge.knowledge_block(["RS-LIC-PH-003", "RS-LIC-PH-004"])


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
