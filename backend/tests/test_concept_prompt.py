"""
Tests for the LOGOS Concept Prompt Engine (LOG-CP-001).

Two layers, matching test_pipeline.py:
  - test_compose_concept_prompt_unit: the engine function against the Mock
    provider — asserts the ConceptPromptResult shape (four variants, five
    model adaptations, a renderable wireframe spec, honest confidence).
  - test_*_router: the /concept-prompts endpoint via TestClient — asserts
    stage gating, per-family output count, persistence, and that the guard
    rejects calls before Judge has run.

Run: pytest backend/tests/test_concept_prompt.py   (from the repo root)
"""

import json

import pytest
from fastapi.testclient import TestClient

from app.schemas import ConceptPromptResult
from app.services.ai_orchestrator import AIProvider, MockAIProvider, set_ai_provider
from app.services.concept_engine import compose_concept_prompt


# ─── Engine unit test ─────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_compose_concept_prompt_unit():
    """The engine returns a well-formed ConceptPromptResult against the mock."""
    set_ai_provider(MockAIProvider())

    family = {
        "family_label": "A",
        "theme": "Trust + Precision",
        "core_meaning_served": "Reliability",
        "symbols": [{"name": "Keystone", "meaning": "Stability"}],
        "visual_language": {"forms": "geometric", "treatment": "minimal"},
        "why_it_works": "Trust is the core meaning.",
    }
    judge_result = {"family_label": "A", "composite": 8.5, "classification": "recommended"}
    brand_dna = {"purpose": "Be reliable.", "positioning_statement": "Trusted partner."}
    insight_report = {"cliches": [{"symbol": "shield", "reason": "overused"}]}

    result = await compose_concept_prompt(
        family=family,
        judge_result=judge_result,
        brand_dna=brand_dna,
        insight_report=insight_report,
    )

    # Shape: it must validate as the schema.
    assert isinstance(result, ConceptPromptResult)

    # Exactly four variants with the canonical styles.
    styles = [v.style for v in result.variants]
    assert styles == ["minimal", "detailed", "typographic-led", "symbolic"], styles
    for v in result.variants:
        assert v.prompt and v.intent  # no empty prompts/intents

    # All five model families addressed.
    families = {a.model_family for a in result.model_adaptations}
    assert families == {"midjourney", "ideogram", "stable-diffusion", "recraft", "general"}, families
    for a in result.model_adaptations:
        assert a.notes and a.example_suffix

    # Wireframe is a renderable structured spec (closed vocabulary).
    wf = result.wireframe
    assert wf.orientation in {"horizontal", "stacked", "lockup", "emblem"}
    assert wf.alignment in {"center", "left", "baseline-aligned"}
    assert 1 <= len(wf.elements) <= 4
    for el in wf.elements:
        assert el.kind in {"symbol", "wordmark", "tagline", "container", "negative-space"}
        assert el.geometry in {"circle", "hexagon", "rectangle", "monogram", "baseline-bar", "custom"}
        assert el.position in {"center", "left-of-text", "above", "below", "integrated"}
        assert el.relative_size in {"dominant", "balanced", "accent", "small"}
    assert wf.favicon_note  # mandatory honest small-size story

    # Rationale + clichés + honest confidence present.
    assert result.rationale
    assert isinstance(result.cliches_avoided, list)
    assert result.confidence in {"C1", "C2", "C3", "C4", "C5"}


# ─── Router integration tests ─────────────────────────────────────────


def _create_project(client: TestClient, brief: str = "x" * 600) -> dict:
    """Create a project. A long brief scores >= 70 on the mock heuristic."""
    response = client.post(
        "/api/projects",
        json={"company_name": "Test Co", "industry": "technology", "client_brief": brief},
    )
    assert response.status_code == 201, response.text
    return response.json()


def _run_to_judge(client: TestClient) -> dict:
    """Walk the pipeline forward through Create + Judge; return the project."""
    project = _create_project(client)
    pid = project["id"]
    for stage in ("analyse", "strategy", "insight", "create", "judge"):
        r = client.post(f"/api/projects/{pid}/{stage}")
        assert r.status_code == 200, (stage, r.text)
    return client.get(f"/api/projects/{pid}").json()


def test_concept_prompts_guard_rejects_before_judge(client: TestClient):
    """Calling /concept-prompts before Judge has run must 400."""
    project = _create_project(client)
    pid = project["id"]
    # Only run through Create, not Judge.
    for stage in ("analyse", "strategy", "insight", "create"):
        r = client.post(f"/api/projects/{pid}/{stage}")
        assert r.status_code == 200, (stage, r.text)

    r = client.post(f"/api/projects/{pid}/concept-prompts")
    assert r.status_code == 400
    assert "Judge" in r.json()["detail"]


def test_concept_prompts_after_judge(client: TestClient):
    """After Judge, /concept-prompts produces one concept per family."""
    project = _run_to_judge(client)
    pid = project["id"]
    family_count = len(project["concept_families"])

    r = client.post(f"/api/projects/{pid}/concept-prompts")
    assert r.status_code == 200, r.text
    results = r.json()
    assert isinstance(results, list)
    assert len(results) == family_count, (len(results), family_count)

    # Each result validates against the schema and has the four styles.
    for item in results:
        cp = ConceptPromptResult(**item)  # validates shape
        styles = [v.style for v in cp.variants]
        assert styles == ["minimal", "detailed", "typographic-led", "symbolic"]

    # Stage advanced + output persisted on the project.
    project = client.get(f"/api/projects/{pid}").json()
    assert project["stage"] == "concept_prompt"
    assert project["concept_prompts"] is not None
    assert len(project["concept_prompts"]) == family_count


def test_concept_prompts_pairs_each_family_with_own_judge(client: TestClient):
    """The mock is label-stable, so family_label round-trips per family."""
    project = _run_to_judge(client)
    pid = project["id"]
    family_labels = [f["family_label"] for f in project["concept_families"]]

    r = client.post(f"/api/projects/{pid}/concept-prompts")
    assert r.status_code == 200, r.text
    result_labels = [cp["family_label"] for cp in r.json()]
    assert result_labels == family_labels


# ─── Client-persona steering + chunked two-pass fallback ──────────────


# Reusable engine inputs (mirror the unit-test fixtures above).
_FAMILY = {
    "family_label": "A",
    "theme": "Trust + Precision",
    "core_meaning_served": "Reliability",
    "symbols": [{"name": "Keystone", "meaning": "Stability"}],
    "visual_language": {"forms": "geometric", "treatment": "minimal"},
    "why_it_works": "Trust is the core meaning.",
}
_JUDGE = {"family_label": "A", "composite": 8.5, "classification": "recommended"}
_DNA = {"purpose": "Be reliable.", "positioning_statement": "Trusted partner."}
_INSIGHT = {"cliches": [{"symbol": "shield", "reason": "overused"}]}
_PERSONA = {
    "one_line": "A pragmatic founder who prizes clarity over cleverness.",
    "archetype": "The Pragmatist",
    "taste_signals": ["plain-spoken language", "trust emphasis"],
    "aesthetic_lean": "minimal",
    "boldness_tolerance": "moderate",
}


@pytest.mark.asyncio
async def test_compose_concept_prompt_with_persona_steer():
    """Steering with a client_persona + is_recommended still yields a valid result."""
    set_ai_provider(MockAIProvider())
    result = await compose_concept_prompt(
        family=_FAMILY,
        judge_result=_JUDGE,
        brand_dna=_DNA,
        insight_report=_INSIGHT,
        client_persona=_PERSONA,
        is_recommended=True,
    )
    assert isinstance(result, ConceptPromptResult)
    assert [v.style for v in result.variants] == [
        "minimal", "detailed", "typographic-led", "symbolic"
    ]


@pytest.mark.asyncio
async def test_compose_concept_prompt_two_pass_fallback():
    """When both single-shot attempts fail validation, the chunked two-pass
    fallback still produces a valid ConceptPromptResult.

    This path is unreachable with the Mock provider (it never malforms), so it
    is live production code with zero coverage unless exercised directly. A stub
    provider returns an incomplete object for single-shot calls and valid split
    payloads for the FALLBACK PASS 1 / PASS 2 calls.
    """
    pass1 = {
        "family_label": "A",
        "core_concept": "A geometric keystone mark expressing reliability.",
        "variants": [
            {"style": "minimal", "prompt": "Minimal keystone + wordmark.", "intent": "Max clarity."},
            {"style": "detailed", "prompt": "Gridded keystone with accents.", "intent": "Full visual language."},
            {"style": "typographic-led", "prompt": "Wordmark leads; keystone in negative space.", "intent": "Name carries brand."},
            {"style": "symbolic", "prompt": "Bold keystone mark leads.", "intent": "Mark is the asset."},
        ],
    }
    pass2 = {
        "family_label": "A",
        "core_concept": "A geometric keystone mark expressing reliability.",
        "model_adaptations": [
            {"model_family": "midjourney", "notes": "raw style", "example_suffix": "--ar 1:1"},
            {"model_family": "ideogram", "notes": "layout lead", "example_suffix": "vector logo"},
            {"model_family": "stable-diffusion", "notes": "weight vector", "example_suffix": "(vector:1.3)"},
            {"model_family": "recraft", "notes": "vector preset", "example_suffix": "style: vector-art"},
            {"model_family": "general", "notes": "flat two-tone", "example_suffix": "vector, flat"},
        ],
        "wireframe": {
            "orientation": "horizontal",
            "balance": "60/40 symbol-to-text",
            "alignment": "baseline-aligned",
            "safe_margin": "12% padding on all sides",
            "elements": [
                {"kind": "symbol", "geometry": "hexagon", "position": "left-of-text", "relative_size": "dominant", "notes": "keystone"},
                {"kind": "wordmark", "geometry": "baseline-bar", "position": "center", "relative_size": "balanced", "notes": "grotesque"},
            ],
            "favicon_note": "Keystone alone remains legible at favicon size.",
        },
        "rationale": "The keystone carries stability metaphorically, avoiding shield/tick cliches.",
        "cliches_avoided": ["shield silhouettes", "checkmark motifs"],
        "confidence": "C3",
    }

    class _TwoPassStub(AIProvider):
        async def complete(self, system_prompt, user_prompt, response_format="text", temperature=0.7, max_tokens=None):
            if "FALLBACK PASS 1" in system_prompt:
                return json.dumps(pass1)
            if "FALLBACK PASS 2" in system_prompt:
                return json.dumps(pass2)
            # Single-shot attempts: a valid JSON object missing required fields,
            # so ConceptPromptResult(**...) raises ValidationError and forces the fallback.
            return json.dumps({"family_label": "A"})

    set_ai_provider(_TwoPassStub())
    try:
        result = await compose_concept_prompt(
            family=_FAMILY, judge_result=_JUDGE, brand_dna=_DNA, insight_report=_INSIGHT
        )
        assert isinstance(result, ConceptPromptResult)
        assert [v.style for v in result.variants] == [
            "minimal", "detailed", "typographic-led", "symbolic"
        ]
        families = {a.model_family for a in result.model_adaptations}
        assert families == {"midjourney", "ideogram", "stable-diffusion", "recraft", "general"}
        assert result.wireframe.favicon_note
        assert result.rationale
    finally:
        # Restore the mock for any router tests that run after this in the session.
        set_ai_provider(MockAIProvider())
