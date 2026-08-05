"""
LogoMind AI Orchestration Layer.

Model-independent interface for AI reasoning. Per CTO Decision #001
(Company Decision #001): LogoMind never depends on a single AI model.

This layer abstracts the model behind a clean interface, so the LOGOS
engines can be developed and tested regardless of which model is
plugged in at runtime.

Usage:
    orchestrator = get_ai_orchestrator()
    response = await orchestrator.complete(
        system_prompt="You are a brand strategist...",
        user_prompt="Analyse this brief: ...",
        response_format="json"
    )

In production, this calls the configured provider (OpenAI, Anthropic,
local model, etc.). In development/testing, a mock returns canned
responses for deterministic testing.
"""

import json
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..schemas import ConfidenceLevel


# ─── Response parsing helper ───────────────────────────────────────────


def parse_json_response(response: str) -> Any:
    """Parse a model response into JSON, tolerating prose and code fences.

    Mock and strict-JSON providers return clean JSON. Free / open models often
    wrap JSON in prose ("Here is the result:") or in a ```json ... ``` fence,
    append trailing commentary, or emit nested objects. This extracts the most
    likely intended JSON object/array so the LOGOS engines can keep doing
    ``Schema(**data)``.

    Strategy: fast-path strict parse; then a code-fence parse; then collect
    EVERY balanced {...} / [...] span and return the longest one that parses
    (the outermost/largest object is almost always the intended payload, not a
    nested sub-object or an incidental object in prose).

    Raises ValueError with a snippet of the response if no JSON is found.
    """
    import re

    text = response.strip()

    # Fast path: already valid JSON.
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strip a ```json ... ``` or ``` ... ``` code fence if present.
    fence = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1))
        except json.JSONDecodeError:
            text = fence.group(1)

    # Collect every balanced {...} and [...] span, keep the ones that parse,
    # and prefer the longest (outermost) one.
    candidates = []
    for opener, closer in (("{", "}"), ("[", "]")):
        depth = 0
        start = -1
        for i, ch in enumerate(text):
            if ch == opener:
                if depth == 0:
                    start = i
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0 and start != -1:
                    span = text[start : i + 1]
                    try:
                        json.loads(span)
                        candidates.append(span)
                    except json.JSONDecodeError:
                        pass
                    start = -1
                elif depth < 0:
                    # Unbalanced closer — bail this bracket type.
                    break

    if candidates:
        # Longest parseable span = the outermost intended payload.
        return json.loads(max(candidates, key=len))

    raise ValueError(
        "Model response did not contain parseable JSON. First 200 chars: "
        + repr(text[:200])
    )


class AIProvider(ABC):
    """Abstract base — any AI provider implements this interface."""

    @abstractmethod
    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: str = "text",  # "text" | "json"
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Return the model's completion as a string."""
        ...


class MockAIProvider(AIProvider):
    """
    Deterministic mock for development and testing.

    Returns canned responses based on prompt keywords. This lets us
    develop the full pipeline without an API key or model cost.
    """

    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: str = "text",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        # Detect engine from the system prompt's FIRST LINE (the identity
        # statement), not from keywords that might appear anywhere in
        # the prompt. Each engine's prompt starts with:
        #   "You are LOGOS <Name>, the <description>."
        # We match on that identity, which is unique per engine.
        first_line = system_prompt.lower().split("\n")[0]

        if "logos strategy" in first_line or "brand dna builder" in first_line:
            return self._mock_strategy(user_prompt)
        elif "logos create" in first_line or "concept families engine" in first_line:
            return self._mock_create(user_prompt)
        elif "logos concept prompt" in first_line or "executable concept engine" in first_line:
            return self._mock_concept_prompt(user_prompt)
        elif "logos judge" in first_line or "design jury" in first_line:
            return self._mock_judge(user_prompt)
        elif "logos insight" in first_line or "trend intelligence" in first_line:
            return self._mock_insight(user_prompt)
        elif "logos sketch coach" in first_line or "sketch coach" in first_line:
            return self._mock_coach(user_prompt)
        elif "logos presentation" in first_line or "presentation builder" in first_line:
            return self._mock_presentation(user_prompt)
        elif "ssb composer" in first_line or "strategic sketch brief" in first_line:
            return self._mock_ssb(user_prompt)
        elif "brief synthesis" in first_line:
            # Synthesize the enriched brief as prose (mock returns a deterministic
            # expanded version of the input brief).
            return self._mock_synthesize(user_prompt)
        elif "logos discover" in first_line or "discovery engine" in first_line or "brief analysis" in first_line:
            return self._mock_discovery(user_prompt)
        elif "intent extraction" in first_line:
            return json.dumps({"preference": "unknown", "intent": "unknown", "reasoning": "mock"})
        else:
            return json.dumps({"note": "Mock provider — no specific engine detected.", "first_line": first_line})

    def _mock_discovery(self, brief: str) -> str:
        # Naive heuristic: longer briefs score higher
        score = min(95, max(15, len(brief.strip()) // 5))
        level = "high" if score >= 90 else "medium" if score >= 60 else "low"
        mode = "expert" if score >= 90 else "guided" if score >= 60 else "workshop"
        return json.dumps({
            "brand_confidence_score": score,
            "brand_confidence_level": level,
            "recommended_mode": mode,
            "discovery_summary": f"This appears to be a brief about a company in an unspecified industry. The brief has {len(brief)} characters, suggesting a {level} level of strategic detail.",
            "missing_info": [
                {"field": "target_audience", "impact": "high", "suggested_question": "Who specifically is your ideal customer?"},
                {"field": "positioning", "impact": "high", "suggested_question": "If you had to describe how you're different from competitors in one sentence, what would it be?"},
            ],
            "next_action": f"Proceed with {mode} mode." if score >= 60 else "Run the Discovery Workshop.",
        })

    def _mock_synthesize(self, user_prompt: str) -> str:
        # Mock brief synthesis: return the ORIGINAL BRIEF portion plus the
        # discovery answers, lightly expanded. Enough prose that re-analysis
        # scores higher than the terse original — mirroring real synthesis.
        original = ""
        answers = ""
        if "ORIGINAL BRIEF:" in user_prompt:
            original = user_prompt.split("ORIGINAL BRIEF:", 1)[1].split("DISCOVERY ANSWERS:", 1)[0].strip()
        if "DISCOVERY ANSWERS:" in user_prompt:
            answers = user_prompt.split("DISCOVERY ANSWERS:", 1)[1].strip()
        return (
            f"{original}\n\n"
            f"Additional strategic context gathered via discovery workshop: {answers}. "
            f"This enriched brief reflects the client's clarified audience, positioning, "
            f"and creative direction, providing a thorough foundation for design work."
        )

    def _mock_strategy(self, brief: str) -> str:
        return json.dumps({
            "purpose": "To serve a specific need in the market that competitors underserve.",
            "purpose_confidence": "C3",
            "positioning_statement": "For [audience] who [need], [company] is the [category] that [distinctive], unlike [alternative], because [reason].",
            "positioning_confidence": "C3",
            "differentiation_primary": "Behavioural differentiation through service quality.",
            "differentiation_dimension": "behaviour",
            "differentiation_defensibility": "C3",
            "audience_configuration": {
                "concerns": ["quality", "trust"],
                "contexts": ["mobile", "in-store"],
                "vocabularies": ["plain language"],
            },
            "audience_confidence": "C3",
            "personality": "A confident, plain-spoken presence that treats newcomers as equals.",
            "personality_coherence": "C3",
            "archetype": None,
            "archetype_finding": "none",
            "emotional_goal": "Confidence and trust.",
            "contradictions_flagged": [],
        })

    def _mock_insight(self, brief: str) -> str:
        return json.dumps({
            "industry_analysis": {"common_symbols": ["generic iconography"], "common_palettes": ["blue"]},
            "competitor_map": [],
            "cliche_avoidance": [
                {"symbol": "Generic globe", "why_cliche": "Used by thousands of brands", "original_meaning": "Global reach", "refresh_possible": False, "alternatives": ["Network", "Nodes"]},
            ],
            "opportunities": ["Negative space", "Abstract geometry"],
            "trend_intelligence": [
                {"name": "Minimalism", "classification": "timeless", "context_assessment": "Always appropriate", "brand_fit": "high"},
            ],
            "trend_vs_timeless_balance": {"timeless": 0.75, "contemporary": 0.25},
            "confidence_summary": {"industry": "C3", "trends": "C3"},
        })

    def _mock_create(self, brief: str) -> str:
        return json.dumps({
            "families": [
                {
                    "family_label": "A",
                    "theme": "Trust + Precision",
                    "core_meaning_served": "Reliability",
                    "symbols": [
                        {"name": "Keystone", "meaning": "Stability", "originality": "C4", "abstraction_level": "metaphorical", "risk_level": "low"},
                        {"name": "Bridge", "meaning": "Connection", "originality": "C3", "abstraction_level": "metaphorical", "risk_level": "low"},
                    ],
                    "visual_language": {"forms": "geometric", "treatment": "minimal", "composition": "symmetric", "palette": "muted"},
                    "why_it_works": "Trust is the brand's core meaning; keystone and bridge carry it metaphorically.",
                    "pitfalls": "Risk of feeling too corporate.",
                    "creative_council_assessment": {"meaning_mind": "Strong", "boldness_mind": "Moderate"},
                    "confidence": "C4",
                    "recommendation_strength": "recommended",
                },
            ],
            "cliches_avoided": [],
            "client_request_notes": [],
        })

    def _mock_concept_prompt(self, brief: str) -> str:
        # Deterministic executable concept matching ConceptPromptResult.
        # Four variants (minimal/detailed/typographic-led/symbolic), five
        # model adaptations, and a renderable wireframe spec.
        return json.dumps({
            "family_label": "A",
            "core_concept": "A geometric keystone mark paired with a confident wordmark, expressing reliability through structural stability.",
            "variants": [
                {
                    "style": "minimal",
                    "prompt": "A minimalist logo: a single-weight geometric keystone symbol beside a clean sans-serif wordmark. One stroke weight, generous negative space, no gradients, no ornament. Centred, balanced, favicon-resilient.",
                    "intent": "Fewest elements; maximum clarity and small-size legibility.",
                },
                {
                    "style": "detailed",
                    "prompt": "A logo mark built from a keystone form constructed on a 1:root2 grid, with two secondary geometric accents suggesting a bridge span. Paired with a refined grotesque wordmark. Honours the full visual language: geometric forms, considered stroke weights, symmetric composition, muted palette of deep teal, warm sand, and ivory.",
                    "intent": "Richer treatment; the family's full visual language honoured.",
                },
                {
                    "style": "typographic-led",
                    "prompt": "A logo where the wordmark is the hero: a custom single-weight grotesque lockup, with a small keystone glyph integrated into the negative space of the first letter. Symbol is subordinate; the name carries the brand.",
                    "intent": "The wordmark leads; the symbol is a subtle integrated detail.",
                },
                {
                    "style": "symbolic",
                    "prompt": "A logo where the keystone mark is the hero: a bold geometric keystone constructed from two interlocking forms suggesting stability and connection. Minimal supporting wordmark set in a neutral sans beneath the mark. The symbol is the memorable asset.",
                    "intent": "The mark leads; typography is subordinate.",
                },
            ],
            "model_adaptations": [
                {"model_family": "midjourney", "notes": "Use raw style and square aspect for clean vector feel; avoid photoreal.", "example_suffix": "--ar 1:1 --style raw --no photo,realistic"},
                {"model_family": "ideogram", "notes": "Lead with explicit layout instruction; ideogram renders text reliably.", "example_suffix": "vector logo, flat, white background"},
                {"model_family": "stable-diffusion", "notes": "Weight 'vector, flat, minimalist' high; demote photoreal tokens.", "example_suffix": "(vector logo:1.3), (flat:1.2), white background"},
                {"model_family": "recraft", "notes": "Use the vector style preset; recraft excels at crisp geometry.", "example_suffix": "style: vector-art, resolution: 2k"},
                {"model_family": "general", "notes": "State 'vector logo, flat, two-tone, transparent or white background' to bias any model away from photorealism.", "example_suffix": "vector logo, flat, two-tone, white background"},
            ],
            "wireframe": {
                "orientation": "horizontal",
                "balance": "60/40 symbol-to-text",
                "alignment": "baseline-aligned",
                "safe_margin": "12% padding on all sides",
                "elements": [
                    {"kind": "symbol", "geometry": "hexagon", "position": "left-of-text", "relative_size": "dominant", "notes": "keystone-derived; sits on the optical centre of the lockup"},
                    {"kind": "wordmark", "geometry": "baseline-bar", "position": "center", "relative_size": "balanced", "notes": "single-weight grotesque, baseline-aligned with the symbol"},
                    {"kind": "negative-space", "geometry": "custom", "position": "integrated", "relative_size": "accent", "notes": "small keystone notch cut into the wordmark's first counter"},
                ],
                "favicon_note": "At favicon size the wordmark drops out; the hexagonal keystone alone remains legible and on-brand.",
            },
            "rationale": "All four variants trace to the brand's core meaning of reliability. The keystone carries stability metaphorically (not literally), honouring the Insight cliché list which flags shields and ticks as overused. The minimal and symbolic variants prioritise favicon resilience; the detailed variant exercises the full geometric visual language; the typographic-led variant covers the case where the name itself is the asset.",
            "cliches_avoided": [
                "shield silhouettes (overused for trust) — replaced with a keystone metaphor",
                "checkmark/tick motifs (overused for reliability) — replaced with structural geometry",
            ],
            "confidence": "C3",
        })

    def _mock_judge(self, brief: str) -> str:
        return json.dumps({
            "family_label": "A",
            "creative_council_verdict": {
                "meaning_mind": "Strong alignment.",
                "simplicity_mind": "Could be further reduced.",
                "differentiation_mind": "Distinctive for this category.",
                "context_mind": "Works across applications.",
                "memorability_mind": "Memorable silhouette.",
                "systems_mind": "Extends well.",
                "emotion_mind": "Evokes trust.",
                "longevity_mind": "Will age well.",
                "boldness_mind": "Appropriately bold.",
                "synthesised_verdict": "Recommended with minor refinement.",
            },
            "jury_scores": {
                "meaning": {"score": 8.5, "confidence": "C4", "justification": "Clearly serves the brand's meaning."},
                "simplicity": {"score": 8.0, "confidence": "C4", "justification": "Reduced appropriately."},
                "clarity": {"score": 7.5, "confidence": "C3", "justification": "Clear at scale; test at favicon."},
                "originality": {"score": 8.0, "confidence": "C4", "justification": "Distinctive combination."},
                "memorability": {"score": 7.0, "confidence": "C3", "justification": "Good silhouette; could be stronger."},
                "authenticity": {"score": 9.0, "confidence": "C4", "justification": "Authentic to the brand."},
                "timelessness": {"score": 8.5, "confidence": "C3", "justification": "Fundamental, not trendy."},
                "relevance": {"score": 8.0, "confidence": "C4", "justification": "Relevant to audience."},
                "consistency": {"score": 7.5, "confidence": "C2", "justification": "System not yet developed."},
                "brand_fit": {"score": 9.5, "confidence": "C5", "justification": "Serves positioning directly."},
            },
            "composite": 8.3,
            "classification": "develop",
            "concept_dna": {
                "concept_id": "C-001",
                "emotion": "Trust",
                "archetype": "Sage",
                "primary_symbol": "Keystone",
                "secondary_symbol": None,
                "shape_language": "Geometric",
                "typography_personality": "Modern Humanist",
                "complexity": "low",
                "originality": "high",
                "risk": "medium",
                "timelessness_score": 8.5,
                "strategic_confidence": 0.94,
            },
            "refinement_recommendations": ["Strengthen memorability — current silhouette not distinctive enough."],
        })

    def _mock_ssb(self, brief: str) -> str:
        return json.dumps({
            "project_essence": "A strategically grounded identity project with clear meaning, audience, and differentiation.",
            "brand_dna_snapshot": {
                "purpose": "To serve a specific need in the market that competitors underserve.",
                "positioning": "For [audience] who [need], [brand] is the [category] that [distinctive].",
                "differentiation": "Behavioural differentiation through service quality.",
                "personality": "A confident, plain-spoken presence that treats newcomers as equals.",
                "archetype": "None identified",
                "emotional_goal": "Confidence and trust.",
            },
            "creative_north_star": "The logo must make the audience feel confident and trusting by expressing the brand's core meaning through distinctive, simple, clear forms.",
            "creative_territories": [
                {"family_label": "A", "theme": "Trust + Precision", "recommendation": "recommended"},
            ],
            "opportunities_and_warnings": {
                "explore": ["Negative space", "Abstract geometry", "Hand-crafted signals"],
                "avoid": ["Generic globes", "Overused shields", "Trendy gradient effects"],
            },
            "creative_council_advice": {
                "meaning_mind": "Ensure every element serves the brand's core meaning.",
                "simplicity_mind": "Apply the Reduction Sequence before finalising.",
                "boldness_mind": "Be appropriately courageous, not reckless.",
            },
            "sketch_missions": [
                {
                    "mission_name": "Keystone + Monogram",
                    "core_idea": "Explore the keystone form integrated with the brand initial.",
                    "combine": ["Keystone", "Letter mark", "Negative space"],
                    "why_it_works": "Keystone signals stability; the monogram personalises it.",
                    "potential_pitfalls": ["Forced integration", "Illegibility at small scale"],
                    "start_with": "Begin with a circular grid. Sketch 10 keystone variations.",
                },
                {
                    "mission_name": "Abstract Horizon",
                    "core_idea": "Explore an abstract horizon line suggesting growth and direction.",
                    "combine": ["Horizon line", "Geometric form", "Open negative space"],
                    "why_it_works": "Horizon suggests forward movement and possibility.",
                    "potential_pitfalls": ["Too generic", "Lacks distinctiveness"],
                    "start_with": "Draw horizontal lines at various weights. Test which feel right.",
                },
                {
                    "mission_name": "Organic Form",
                    "core_idea": "Explore an organic, flowing form suggesting warmth and approachability.",
                    "combine": ["Curved line", "Natural form", "Soft geometry"],
                    "why_it_works": "Organic forms feel human and approachable.",
                    "potential_pitfalls": ["Too decorative", "Hard to reproduce"],
                    "start_with": "Sketch flowing lines from observation. Don't stylise yet.",
                },
            ],
            "selected_territory": {
                "family_label": "A",
                "theme": "Trust + Precision",
                "recommendation": "recommended",
                "core_meaning_served": "Reliability",
                "why_it_works": "Trust is the brand's core meaning; keystone and bridge carry it metaphorically.",
                "pitfalls": "Risk of feeling too corporate.",
                "composite": 8.3,
                "classification": "develop",
                "visual_language": {
                    "forms": "geometric — concentric circles on a 1:√2 grid",
                    "treatment": "single-weight 2u strokes, matte",
                    "composition": "centred mark, 1x clear-space on all sides",
                    "palette": "deep slate dominant, warm sand secondary, ivory accent",
                },
                "symbols": [
                    {"name": "Keystone", "meaning": "Stability", "originality": "C4", "abstraction_level": "metaphorical", "risk_level": "low"},
                    {"name": "Bridge", "meaning": "Connection", "originality": "C3", "abstraction_level": "metaphorical", "risk_level": "low"},
                ],
                "concept_dna": {
                    "concept_id": "C-001",
                    "emotion": "Trust",
                    "archetype": "Sage",
                    "primary_symbol": "Keystone",
                    "secondary_symbol": None,
                    "shape_language": "Geometric",
                    "typography_personality": "Modern Humanist",
                    "complexity": "low",
                    "originality": "high",
                    "risk": "medium",
                    "timelessness_score": 8.5,
                    "strategic_confidence": 0.94,
                },
                "refinement_recommendations": ["Strengthen memorability — current silhouette not distinctive enough."],
            },
            "council_advice": {
                "meaning_mind": "Strong — keystone serves reliability directly.",
                "simplicity_mind": "Reduce to a single weight before finalising.",
                "differentiation_mind": "Distinctive for this category.",
                "context_mind": "Works across digital and print.",
                "memorability_mind": "Memorable silhouette; could be stronger.",
                "systems_mind": "Extends well into a system.",
                "emotion_mind": "Evokes trust and stability.",
                "longevity_mind": "Fundamental, not trendy.",
                "boldness_mind": "Appropriately bold.",
                "synthesised_verdict": "Recommended with minor refinement to memorability.",
            },
        })

    def _mock_coach(self, brief: str) -> str:
        return json.dumps({
            "assessment": "Good starting direction. The form has a clear silhouette.",
            "suggestions": [
                "Have you considered removing the secondary outline?",
                "What does the negative space suggest?",
                "Test at favicon size — does the detail survive?",
            ],
            "pitfalls_to_watch": ["Line weight inconsistency", "Forced monogram integration"],
            "confidence": "C3",
        })

    def _mock_presentation(self, brief: str) -> str:
        return json.dumps({
            "sections": [
                {"title": "Cover", "content": "Project name and date"},
                {"title": "Executive Summary", "content": "One-page strategic summary"},
            ],
            "objection_handling": [
                {"concern": "Too simple", "response": "Reduction Sequence reasoning"},
            ],
        })


class OpenAIProvider(AIProvider):
    """
    OpenAI provider — production default.

    Uses the OpenAI Python SDK against the OpenAI API or any OpenAI-compatible
    endpoint (OpenRouter, Together, Groq, a local server, etc.). Requires
    OPENAI_API_KEY. For a non-OpenAI endpoint, set OPENAI_BASE_URL and a
    LOGOMIND_MODEL understood by that endpoint.
    """

    async def complete(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: str = "text",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise RuntimeError("openai package not installed. Run: pip install openai")

        import asyncio
        import logging

        from openai import APIError, APITimeoutError, RateLimitError

        log = logging.getLogger("logomind")

        client_kwargs: Dict[str, Any] = {"api_key": os.environ.get("OPENAI_API_KEY")}
        base_url = os.environ.get("OPENAI_BASE_URL")
        if base_url:
            client_kwargs["base_url"] = base_url

        client = AsyncOpenAI(**client_kwargs)
        model = os.environ.get("LOGOMIND_MODEL", "gpt-4o")

        kwargs: Dict[str, Any] = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        # Real model endpoints (NIM, OpenRouter, OpenAI) transiently time out,
        # rate-limit, or return 5xx — especially on the long JSON calls the
        # LOGOS engines make. Retry transient failures with a short backoff so
        # a momentary hiccup doesn't surface as a 500 to the designer.
        # Retries are bounded; a persistent failure still raises after the last
        # attempt (the caller/engine decides how to report it).
        max_attempts = 3
        last_exc: Optional[Exception] = None
        for attempt in range(1, max_attempts + 1):
            try:
                response = await client.chat.completions.create(**kwargs)
                return response.choices[0].message.content
            except (APITimeoutError, RateLimitError) as e:
                # Definitely transient.
                last_exc = e
            except APIError as e:
                # Retry only server-side / overload errors (5xx, 429 already
                # caught above). Client errors (4xx auth/bad-request) should
                # surface immediately — retrying won't help.
                status = getattr(e, "status_code", None) or getattr(
                    getattr(e, "response", None), "status_code", None
                )
                if status is not None and 500 <= int(status) < 600:
                    last_exc = e
                else:
                    raise

            if attempt < max_attempts:
                backoff = 2 ** (attempt - 1)  # 1s, then 2s
                log.warning(
                    "AI provider transient error (attempt %d/%d): %s — retrying in %ds",
                    attempt, max_attempts, type(e).__name__, backoff,
                )
                await asyncio.sleep(backoff)

        # All retries exhausted — surface the last transient error.
        raise last_exc  # type: ignore[misc]



# ─── Factory ───────────────────────────────────────────────────────────

_provider: Optional[AIProvider] = None


def get_ai_orchestrator() -> AIProvider:
    """
    Return the configured AI provider.

    Selection order:
    1. If LOGOMIND_AI_PROVIDER env var is set (mock | openai | openrouter | nim),
       use it. An explicit "mock" always wins, even if a key is present.
    2. If OPENAI_API_KEY is set, use OpenAI.
    3. Otherwise, use Mock (development mode).

    nim (NVIDIA build.nvidia.com) and openrouter route through the OpenAI-
    compatible provider with an auto-configured base URL + model; they accept
    the key via OPENAI_API_KEY (nim also accepts NVIDIA_API_KEY).
    """
    global _provider
    if _provider is not None:
        return _provider

    provider_name = os.environ.get("LOGOMIND_AI_PROVIDER", "").lower()

    # OpenRouter routes through the existing OpenAI-compatible provider; the
    # base URL is provider-specific so we set it authoritatively when openrouter
    # is selected. The model is defaulted only if unset.
    if provider_name == "openrouter":
        os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"
        # Free models on OpenRouter fluctuate in availability; this one is
        # currently active and reliably returns parseable JSON. Override with
        # LOGOMIND_MODEL if you prefer a different one.
        os.environ.setdefault("LOGOMIND_MODEL", "nvidia/nemotron-3-super-120b-a12b:free")

    # NVIDIA NIM (build.nvidia.com API catalog) is also OpenAI-compatible.
    # For an explicit nim selection the base URL is authoritative, and the key
    # is taken from NVIDIA_API_KEY when present (preferred over a leftover
    # OPENAI_API_KEY from a different provider).
    if provider_name == "nim":
        os.environ["OPENAI_BASE_URL"] = "https://integrate.api.nvidia.com/v1"
        if os.environ.get("NVIDIA_API_KEY"):
            os.environ["OPENAI_API_KEY"] = os.environ["NVIDIA_API_KEY"]
        # A capable instruct model on the catalog; override with LOGOMIND_MODEL.
        os.environ.setdefault("LOGOMIND_MODEL", "nvidia/llama-3.1-nemotron-70b-instruct")

    # Any real provider requires an API key. Surface that explicitly instead of
    # silently falling back to the mock, which would hide a misconfiguration.
    needs_key = provider_name in ("openai", "openrouter", "nim") or (
        provider_name == "" and bool(os.environ.get("OPENAI_BASE_URL"))
    )
    if needs_key and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            f"LOGOMIND_AI_PROVIDER={provider_name or '(unset)'} requires OPENAI_API_KEY, "
            "but it is not set. Either provide a key or set LOGOMIND_AI_PROVIDER=mock."
        )

    # An explicit provider request always wins. In particular, LOGOMIND_AI_PROVIDER=mock
    # must be honoured even when an API key is present in the environment (e.g. in .env),
    # so development with the deterministic mock is never silently overridden.
    if provider_name == "mock":
        _provider = MockAIProvider()
    elif provider_name in ("openai", "openrouter", "nim") or os.environ.get("OPENAI_API_KEY"):
        _provider = OpenAIProvider()
    else:
        # Default: development mode, no key configured → deterministic mock.
        _provider = MockAIProvider()

    return _provider


def set_ai_provider(provider: AIProvider):
    """Override the provider (for testing)."""
    global _provider
    _provider = provider
