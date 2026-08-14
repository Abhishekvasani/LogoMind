"""
LOGOS Client Insight — the Client Preference Predictor.

Answers the question LogoMind previously couldn't: "what will THIS client
love?" Given a brief, the strategy/insight context, and the generated Concept
Families, it (1) builds a model of the specific decision-maker's taste and
(2) predicts how strongly each family will resonate with THAT persona, then
ranks them.

HONESTY BOUND (structural, not cosmetic): this is reasoning-based preference
prediction via LLM persona-simulation. It is NOT a measurement of literal
neural / brain response, and nothing here claims to be. Every prediction
carries explicit confidence, and the report's `caveat` states plainly how much
signal a brief alone provides (it improves markedly once contest feedback is
folded in — Stage 4).

It deliberately diverges from the Judge engine: the Judge scores design
excellence; this scores client appeal. A family can be design-excellent yet
misaligned with a conservative client — and the predictor says so.
"""

from typing import Any, Dict, List, Optional

from pydantic import ValidationError

from .ai_orchestrator import get_ai_orchestrator, parse_json_response
from . import lic_knowledge
from ..schemas import AppealReport, ClientPersona, FamilyAppeal, ConfidenceLevel

CLIENT_FIT_SYSTEM_PROMPT = """You are LOGOS Client Insight, the Client Preference Predictor of LogoMind.

Your role: predict which creative direction THIS specific client will love —
not which is the best design in the abstract. You build a model of the
decision-maker's taste, then score each Concept Family for predicted resonance
with THAT persona.

HONESTY BOUND (critical): You perform reasoning-based preference prediction.
You are NOT measuring a literal neural or brain response, and you must never
claim to. Frame every score as an inference with explicit confidence. A brief
alone limits certainty — say so plainly in `caveat`.

CONTEST SIGNALS (when provided): If a decoded contest brief and/or revealed
in-contest preferences are included, treat them as the HIGHEST-signal input —
they are the client's explicit requirements and actual revealed taste, and they
OVERRIDE inferences drawn from the prose brief alone. Reflect them in the persona
(must_haves, must_avoids, aesthetic_lean, colors) and in every family's appeal.

STEP 1 — BUILD THE PERSONA from the brief + discovery + brand DNA + insight:
- Infer the decision-maker's archetype and aesthetic lean from WHAT they
  emphasise and the words they choose. A brief saying "trustworthy, established,
  premium" signals a very different taste from one saying "bold, disruptive, fun".
- Decode stated preferences to the strategic intent behind them
  ("blue" -> trust; "shield" -> security; "modern" -> wants to feel current).
- Rate boldness_tolerance from how conventional vs adventurous the brief reads.
- Lift explicit must-haves and must-avoids verbatim where present.

STEP 2 — PREDICT APPEAL for EACH family by simulating THIS client's reaction:
- Score 0-100 for how strongly THIS client (not a generic audience) responds.
- A design-excellent family misaligned with the client's lean scores LOWER than
  a slightly less original one that nails their taste. You are predicting THEIR
  choice, not the jury's — use the judge_report as context, not as the answer.
- predicted_response is ONE vivid line in the client's own emotional vocabulary
  ("will read as premium and trustworthy to them" / "will feel too playful for a
  serious finance buyer").
- appeal_drivers and appeal_risks must be relative to THIS persona, not abstract
  design criteria.

BIAS TOWARD WINNING: in a contest the client picks what feels right, fast. favour
families matching the client's aesthetic_lean and decoded_intents. The most
original option is NOT always what THIS client will choose — predict their pick.

Respond as JSON with EXACTLY this schema (use these field names verbatim):
{
  "persona": {
    "one_line": "...",
    "archetype": "...",
    "taste_signals": ["..."],
    "decoded_intents": [{"stated": "...", "intent": "..."}],
    "aesthetic_lean": "minimal | bold | elegant | playful | technical | heritage | organic",
    "boldness_tolerance": "conservative | moderate | adventurous",
    "must_haves": ["..."],
    "must_avoids": ["..."],
    "references": ["..."],
    "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
  },
  "family_appeal": [
    {
      "family_label": "A",
      "client_appeal_score": 0.0,
      "rank": 1,
      "predicted_response": "...",
      "appeal_drivers": ["..."],
      "appeal_risks": ["..."],
      "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
    }
  ],
  "recommended_family": "A",
  "reasoning": "2-3 sentences: why the top family is the safest bet to win THIS client",
  "caveat": "honest limit of this prediction",
  "confidence": "C1" | "C2" | "C3" | "C4" | "C5"
}

Include one family_appeal entry for EVERY family provided. Return ONLY the JSON
object. No prose, no code fences, no commentary.
""" + lic_knowledge.knowledge_block([
    # Ground the persona's decoded intents and taste in the canonical volumes:
    # colour psychology (decoding "blue" -> trust), symbol meanings (decoding
    # "a shield" -> security), type personality (aesthetic lean), the
    # twelve-archetype vocabulary the persona's `archetype` field draws from,
    # and the decision-maker types (whose aesthetic-lean/boldness-tolerance
    # profiles are literally the persona's predicted fields — priors, never
    # verdicts; the brief's evidence overrides).
    "RS-LIC-CL-VOLUME", "RS-LIC-TY-VOLUME", "RS-LIC-SY-VOLUME", "RS-LIC-BS-005",
    "RS-LIC-PSY-VOLUME",
])


def _normalize_appeal_report(data: Dict[str, Any], family_labels: List[str]) -> Dict[str, Any]:
    """Defensively repair common model drift before validation.

    - Ensures every provided family has an appeal entry (drops entries for
      unknown labels, fills missing labels with a low-confidence placeholder).
    - Re-ranks by client_appeal_score desc and forces rank/recommended_family
      to match, so a model that mis-sorts still yields a consistent report.
    - Defaults caveat/confidence if absent.
    """
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object, got {type(data).__name__}.")

    data = dict(data)

    # Normalize persona into a dict if the model emitted it oddly.
    persona = data.get("persona")
    if not isinstance(persona, dict):
        persona = {}
    persona.setdefault("one_line", "Client taste inferred from the brief.")
    persona.setdefault("archetype", "Unknown")
    persona.setdefault("taste_signals", [])
    persona.setdefault("decoded_intents", [])
    persona.setdefault("aesthetic_lean", "minimal")
    persona.setdefault("boldness_tolerance", "moderate")
    persona.setdefault("must_haves", [])
    persona.setdefault("must_avoids", [])
    persona.setdefault("references", [])
    persona.setdefault("confidence", "C3")
    data["persona"] = persona

    # Build a clean appeal list keyed to the known family labels.
    raw_appeal = data.get("family_appeal") or []
    if isinstance(raw_appeal, dict):
        raw_appeal = [raw_appeal]
    by_label: Dict[str, Dict[str, Any]] = {}
    for entry in raw_appeal:
        if not isinstance(entry, dict):
            continue
        label = str(entry.get("family_label", "")).strip()
        if not label:
            continue
        by_label[label] = entry

    clean: List[Dict[str, Any]] = []
    for label in family_labels:
        entry = by_label.get(label, {})
        score = entry.get("client_appeal_score", 50.0)
        try:
            score = float(score)
        except (TypeError, ValueError):
            score = 50.0
        score = max(0.0, min(100.0, score))
        clean.append({
            "family_label": label,
            "client_appeal_score": score,
            "rank": 0,  # assigned after sorting
            "predicted_response": entry.get("predicted_response") or "No prediction provided.",
            "appeal_drivers": entry.get("appeal_drivers") or ["Matches the brief's core intent."],
            "appeal_risks": entry.get("appeal_risks") or ["Limited brief signal."],
            "confidence": entry.get("confidence", "C3"),
        })

    # Sort by score desc and assign deterministic ranks.
    clean.sort(key=lambda e: e["client_appeal_score"], reverse=True)
    for idx, entry in enumerate(clean, start=1):
        entry["rank"] = idx

    data["family_appeal"] = clean
    data["recommended_family"] = clean[0]["family_label"] if clean else (family_labels[0] if family_labels else "")
    data.setdefault("reasoning", "No reasoning provided.")
    data.setdefault(
        "caveat",
        "This is a brief-only inference. Fold in the client's contest ratings and "
        "comments (Client Fit → Refine) to sharpen the prediction.",
    )
    data.setdefault("confidence", "C3")
    return data


def _contest_signals_block(
    contest_brief: Optional[Dict[str, Any]],
    contest_feedback: Optional[List[Dict[str, Any]]],
) -> str:
    """Render decoded contest brief + revealed preferences as a high-signal block.

    Returns "" when neither is present, so the no-contest path is unchanged.
    These signals are the client's explicit requirements and actual revealed
    taste — framed to the model as overriding inferences from prose.
    """
    if not contest_brief and not contest_feedback:
        return ""

    lines = ["", "CONTEST SIGNALS (HIGHEST signal — the client's explicit + revealed taste):"]
    if contest_brief:
        cb = contest_brief
        def _join(key):
            vals = cb.get(key) or []
            return ", ".join(vals) if isinstance(vals, list) else str(vals)
        if cb.get("colors_preferred"):
            lines.append(f"  preferred colors: {_join('colors_preferred')}")
        if cb.get("colors_avoided"):
            lines.append(f"  colors to AVOID: {_join('colors_avoided')}")
        if cb.get("style_keywords"):
            lines.append(f"  style wanted: {_join('style_keywords')}")
        if cb.get("must_include"):
            lines.append(f"  must include: {_join('must_include')}")
        if cb.get("must_avoid"):
            lines.append(f"  must AVOID: {_join('must_avoid')}")
        if cb.get("dos"):
            lines.append(f"  do: {_join('dos')}")
        if cb.get("donts"):
            lines.append(f"  don't: {_join('donts')}")
        if cb.get("decoded_summary"):
            lines.append(f"  decoded intent: {cb['decoded_summary']}")

    if contest_feedback:
        liked = [s.get("trait") for s in contest_feedback if s.get("kind") == "liked" and s.get("trait")]
        disliked = [s.get("trait") for s in contest_feedback if s.get("kind") == "disliked" and s.get("trait")]
        comments = [s.get("trait") for s in contest_feedback if s.get("kind") == "comment" and s.get("trait")]
        if liked:
            lines.append(f"  REVEALED — client LIKED: {', '.join(liked)}")
        if disliked:
            lines.append(f"  REVEALED — client DISLIKED: {', '.join(disliked)}")
        if comments:
            lines.append(f"  REVEALED — client comments: {', '.join(comments)}")
        lines.append("  (Update the persona and re-rank to reflect these REVEALED preferences above all.)")

    lines.append("")
    return "\n".join(lines)


async def predict_client_appeal(
    company_name: str,
    industry: str,
    client_brief: str,
    discovery_summary: Optional[Dict[str, Any]],
    brand_dna: Optional[Dict[str, Any]],
    insight_report: Optional[Dict[str, Any]],
    concept_families: List[Dict[str, Any]],
    judge_report: Optional[List[Dict[str, Any]]] = None,
    contest_brief: Optional[Dict[str, Any]] = None,
    contest_feedback: Optional[List[Dict[str, Any]]] = None,
) -> AppealReport:
    """Build the client persona and rank families by predicted appeal (Client Fit stage).

    Single LLM call: persona + per-family appeal in one structured response. The
    normalizer repairs drift and re-ranks deterministically before validation.

    ``contest_brief`` (Stage 3 decoded brief) and ``contest_feedback`` (Stage 4
    revealed preferences) are the highest-signal inputs when present — they
    represent the client's explicit requirements and actual mid-contest taste,
    and override inferences from the prose brief alone.
    """
    if not concept_families:
        raise ValueError("Concept Families are required to predict client appeal.")

    orchestrator = get_ai_orchestrator()
    family_labels = [str(f.get("family_label", "?")) for f in concept_families]

    # Compact family summaries so the model scores real content, not labels.
    family_summaries = []
    for f in concept_families:
        family_summaries.append({
            "family_label": f.get("family_label"),
            "theme": f.get("theme"),
            "core_meaning_served": f.get("core_meaning_served"),
            "visual_language": f.get("visual_language"),
            "symbols": [
                {"name": s.get("name"), "meaning": s.get("meaning")}
                for s in (f.get("symbols") or [])
            ],
            "why_it_works": f.get("why_it_works"),
            "recommendation_strength": f.get("recommendation_strength"),
        })

    # Judge composites as context only — the predictor must diverge where the
    # client's taste differs from jury excellence.
    jury_context = []
    if judge_report:
        for j in judge_report:
            jury_context.append({
                "family_label": j.get("family_label"),
                "composite": j.get("composite"),
                "classification": j.get("classification"),
            })

    signals_block = _contest_signals_block(contest_brief, contest_feedback)

    import json
    user_prompt = f"""Company: {company_name}
Industry: {industry}

CLIENT BRIEF:
{client_brief}
{signals_block}
Discovery summary:
{json.dumps(discovery_summary or {}, indent=2, default=str)}

Brand DNA:
{json.dumps(brand_dna or {}, indent=2, default=str)}

Insight Report (clichés + competitor context):
{json.dumps(insight_report or {}, indent=2, default=str)}

Concept Families to score (one appeal entry EACH — labels: {family_labels}):
{json.dumps(family_summaries, indent=2, default=str)}

Judge composites (CONTEXT ONLY — predict the CLIENT's preference, which may differ):
{json.dumps(jury_context, indent=2, default=str)}
"""

    response = await orchestrator.complete(
        system_prompt=CLIENT_FIT_SYSTEM_PROMPT,
        user_prompt=user_prompt,
        response_format="json",
        temperature=0.4,  # mostly analytical; mild creativity for vivid phrasing
    )

    try:
        return AppealReport(**_normalize_appeal_report(parse_json_response(response), family_labels))
    except (ValidationError, ValueError) as first_err:
        # One retry with a compliance nudge — handles truncation / renames.
        import logging
        logging.getLogger("logomind").warning(
            "Client Fit first attempt failed (%s); retrying.", first_err.__class__.__name__
        )
        retry_prompt = user_prompt + (
            "\nIMPORTANT: return the COMPLETE JSON object in one go with EXACTLY these "
            "top-level keys: persona, family_appeal, recommended_family, reasoning, "
            "caveat, confidence. Include one family_appeal entry for every family label. "
            "Keep each predicted_response to one sentence so the whole object fits."
        )
        response = await orchestrator.complete(
            system_prompt=CLIENT_FIT_SYSTEM_PROMPT,
            user_prompt=retry_prompt,
            response_format="json",
            temperature=0.3,
        )
        return AppealReport(**_normalize_appeal_report(parse_json_response(response), family_labels))
