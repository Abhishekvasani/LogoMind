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
        # Detect engine from the system prompt and return a sensible mock
        sp_lower = system_prompt.lower()

        if "discovery" in sp_lower or "brief analysis" in sp_lower:
            return self._mock_discovery(user_prompt)
        elif "strategy" in sp_lower or "brand dna" in sp_lower:
            return self._mock_strategy(user_prompt)
        elif "insight" in sp_lower or "trend" in sp_lower:
            return self._mock_insight(user_prompt)
        elif "create" in sp_lower or "concept famil" in sp_lower:
            return self._mock_create(user_prompt)
        elif "judge" in sp_lower or "jury" in sp_lower:
            return self._mock_judge(user_prompt)
        elif "sketch coach" in sp_lower:
            return self._mock_coach(user_prompt)
        elif "presentation" in sp_lower:
            return self._mock_presentation(user_prompt)
        else:
            return json.dumps({"note": "Mock provider — no specific engine detected."})

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

    Uses the OpenAI Python SDK. Requires OPENAI_API_KEY environment variable.
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

        client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        model = os.environ.get("LOGOMIND_MODEL", "gpt-4o")

        kwargs = {
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

        response = await client.chat.completions.create(**kwargs)
        return response.choices[0].message.content


# ─── Factory ───────────────────────────────────────────────────────────

_provider: Optional[AIProvider] = None


def get_ai_orchestrator() -> AIProvider:
    """
    Return the configured AI provider.

    Selection order:
    1. If LOGOMIND_AI_PROVIDER env var is set, use it.
    2. If OPENAI_API_KEY is set, use OpenAI.
    3. Otherwise, use Mock (development mode).
    """
    global _provider
    if _provider is not None:
        return _provider

    provider_name = os.environ.get("LOGOMIND_AI_PROVIDER", "").lower()

    if provider_name == "mock" or not os.environ.get("OPENAI_API_KEY"):
        _provider = MockAIProvider()
    elif provider_name == "openai" or os.environ.get("OPENAI_API_KEY"):
        _provider = OpenAIProvider()
    else:
        _provider = MockAIProvider()

    return _provider


def set_ai_provider(provider: AIProvider):
    """Override the provider (for testing)."""
    global _provider
    _provider = provider
