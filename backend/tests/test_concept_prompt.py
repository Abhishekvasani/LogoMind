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
from app.services.ai_orchestrator import MockAIProvider, set_ai_provider
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
