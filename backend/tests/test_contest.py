"""
Tests for the LOGOS Contest Reader (Contest Brief Decoder) and the
Client Fit refine loop — the two contest-intelligence inputs that sharpen
the Client Preference Predictor.

Two layers, matching the rest of the suite:
  - engine unit tests against the Mock provider (decode + normalize + enrich)
  - router integration tests via TestClient (decode, attach, refine)

Run: pytest backend/tests/test_contest.py   (from the repo root)
"""

import pytest
from fastapi.testclient import TestClient

from app.schemas import ContestBrief
from app.services.ai_orchestrator import MockAIProvider, set_ai_provider
from app.services.contest_engine import (
    contest_brief_to_enrichment,
    decode_contest_brief,
    _normalize_contest_brief,
)


# ─── Engine unit tests ───────────────────────────────────────────────


@pytest.mark.asyncio
async def test_decode_contest_brief_unit():
    """The decoder returns a well-formed ContestBrief against the mock."""
    set_ai_provider(MockAIProvider())
    brief = await decode_contest_brief("Company: Acme\nColors: blue\nAvoid: red")
    assert isinstance(brief, ContestBrief)
    assert "blue" in brief.colors_preferred
    assert "red" in brief.colors_avoided
    assert brief.decoded_summary  # never empty
    assert brief.confidence in {"C1", "C2", "C3", "C4", "C5"}


@pytest.mark.asyncio
async def test_decode_contest_brief_rejects_empty():
    """Empty input must raise rather than fabricate a brief."""
    set_ai_provider(MockAIProvider())
    with pytest.raises(ValueError):
        await decode_contest_brief("   ")


def test_normalize_contest_brief_coerces_strings_to_lists():
    """Comma/newline-separated strings become lists; empty nullables become None."""
    out = _normalize_contest_brief({
        "colors_preferred": "blue, white",
        "style_keywords": "modern\nminimal",
        "company_name": "",
        "industry": "Tech",
        "must_include": "shield",
    })
    assert out["colors_preferred"] == ["blue", "white"]
    assert out["style_keywords"] == ["modern", "minimal"]
    assert out["must_include"] == ["shield"]
    assert out["company_name"] is None  # empty string -> None
    assert out["industry"] == "Tech"


def test_contest_brief_to_enrichment_renders_block():
    """The enrichment helper renders the decoded summary + structured requirements."""
    brief = ContestBrief(
        decoded_summary="A modern identity.",
        colors_preferred=["blue"],
        colors_avoided=["red"],
        style_keywords=["minimal"],
        must_include=["keystone"],
    )
    block = contest_brief_to_enrichment(brief)
    assert "A modern identity." in block
    assert "Preferred colors" in block and "blue" in block
    assert "Colors to avoid" in block and "red" in block
    assert "Must include" in block and "keystone" in block


# ─── Router integration tests ────────────────────────────────────────


def _create_project(client: TestClient, brief: str = "x" * 600) -> dict:
    """Create a project. A long brief scores >= 70 on the mock heuristic."""
    response = client.post(
        "/api/projects",
        json={"company_name": "Test Co", "industry": "technology", "client_brief": brief},
    )
    assert response.status_code == 201, response.text
    return response.json()


def test_decode_contest_brief_route(client: TestClient):
    """POST /decode-contest-brief returns a structured ContestBrief."""
    r = client.post(
        "/api/decode-contest-brief",
        json={"raw_text": "Company: Acme. Colors: blue. Avoid: red."},
    )
    assert r.status_code == 200, r.text
    brief = r.json()
    assert "blue" in brief["colors_preferred"]
    assert brief["decoded_summary"]


def test_attach_contest_brief_route(client: TestClient):
    """POST /projects/{id}/contest-brief attaches, enriches the brief, persists."""
    project = _create_project(client)
    pid = project["id"]
    original_brief_len = len(project["client_brief"])

    r = client.post(
        f"/api/projects/{pid}/contest-brief",
        json={"raw_text": "Company: Decoded Co. Industry: finance. Colors: blue. Avoid: red."},
    )
    assert r.status_code == 200, r.text
    project = r.json()
    assert project["contest_brief"] is not None
    assert "blue" in project["contest_brief"]["colors_preferred"]
    # The client brief is enriched with the decoded requirements (not just raw prose).
    assert len(project["client_brief"]) > original_brief_len


def test_refine_client_fit_route(client: TestClient):
    """POST /projects/{id}/client-fit/refine accumulates signals and re-predicts."""
    project = _create_project(client)
    pid = project["id"]
    # Refine needs Concept Families.
    for stage in ("analyse", "strategy", "insight", "create"):
        r = client.post(f"/api/projects/{pid}/{stage}")
        assert r.status_code == 200, (stage, r.text)

    # Initial prediction (no feedback yet).
    r = client.post(f"/api/projects/{pid}/client-fit")
    assert r.status_code == 200, r.text
    project = client.get(f"/api/projects/{pid}").json()
    assert not project.get("contest_feedback")

    # Refine with a revealed in-contest preference.
    r = client.post(
        f"/api/projects/{pid}/client-fit/refine",
        json={"signals": [{"kind": "liked", "trait": "minimal layouts", "note": "the client praised it"}]},
    )
    assert r.status_code == 200, r.text
    assert r.json()["recommended_family"]

    project = client.get(f"/api/projects/{pid}").json()
    assert len(project["contest_feedback"]) == 1
    assert project["contest_feedback"][0]["trait"] == "minimal layouts"
    assert project["appeal_report"] is not None
