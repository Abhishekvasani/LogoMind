"""
End-to-end tests for the LogoMind LOGOS pipeline.

Two layers:
  - test_app_boots: guards against the auth-import / startup regressions
    (the original cause of the app not starting).
  - test_*_stage: walk the full 9-stage pipeline against the Mock AI provider
    and assert each stage advances the project and persists its output.

Run: pytest backend/tests   (from the repo root)
"""

from fastapi.testclient import TestClient


# ─── Boot / regression guard ───────────────────────────────────────────


def test_app_boots(client: TestClient):
    """The FastAPI app must import and answer /health.

    This directly guards against the original failure: the half-built auth
    layer importing packages (jwt, passlib) that were not installed.
    """
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "healthy"
    # Knowledge extracts must also have resolved (engines inject them).
    assert body["knowledge"]["loaded"] is True
    assert "RS-LIC-PH-005" in body["knowledge"]["available"]


# ─── Helpers ───────────────────────────────────────────────────────────


def _create_project(client: TestClient, brief: str = "x" * 600) -> dict:
    """Create a project. A long brief scores >= 70 on the mock heuristic."""
    response = client.post(
        "/api/projects",
        json={
            "company_name": "Test Co",
            "industry": "technology",
            "client_brief": brief,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


# ─── Full pipeline walk ────────────────────────────────────────────────


def test_pipeline_direct_path(client: TestClient):
    """Long brief → score >= 70 → straight through to Presentation, no workshop."""
    project = _create_project(client)
    project_id = project["id"]

    # Stage 2: Discovery (analyse) — long brief should score high.
    r = client.post(f"/api/projects/{project_id}/analyse")
    assert r.status_code == 200, r.text
    analysis = r.json()
    assert analysis["brand_confidence_score"] >= 70
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "discovery"
    assert project["discovery_summary"] is not None

    # Stage 4: Strategy — Brand DNA.
    r = client.post(f"/api/projects/{project_id}/strategy")
    assert r.status_code == 200, r.text
    assert r.json()["positioning_statement"]
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "strategy"
    assert project["brand_dna"] is not None

    # Stage 5: Insight.
    r = client.post(f"/api/projects/{project_id}/insight")
    assert r.status_code == 200, r.text
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "insight"
    assert project["insight_report"] is not None

    # Stage 6: Create — Concept Families.
    r = client.post(f"/api/projects/{project_id}/create")
    assert r.status_code == 200, r.text
    families = r.json()["families"]
    assert len(families) >= 1
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "create"
    assert project["concept_families"] is not None

    # Stage 7: Judge.
    r = client.post(f"/api/projects/{project_id}/judge")
    assert r.status_code == 200, r.text
    assert isinstance(r.json(), list)
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "judge"
    assert project["judge_report"] is not None

    # Select a family (mock returns family label "A").
    family_label = families[0]["family_label"]
    r = client.post(f"/api/projects/{project_id}/select-family/{family_label}")
    assert r.status_code == 200, r.text
    assert r.json() == {"selected": family_label}

    # Stage 8: SSB.
    r = client.post(f"/api/projects/{project_id}/ssb")
    assert r.status_code == 200, r.text
    ssb = r.json()
    assert ssb["creative_north_star"]
    # The selected territory is anchored from the chosen family + judge result.
    assert ssb["selected_territory"] is not None, "SSB must carry the selected territory"
    assert ssb["selected_territory"]["family_label"] == family_label
    assert ssb["selected_territory"]["composite"] is not None, "selected territory must carry the judge composite"
    assert ssb["selected_territory"]["visual_language"], "selected territory must carry visual language"
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "ssb"
    assert project["ssb"] is not None

    # Stage 8 iteration: Sketch upload → coach feedback.
    r = client.post(
        f"/api/projects/{project_id}/sketches",
        json={
            "project_id": project_id,
            "sketch_number": 1,
            "description": "A geometric keystone mark.",
            "design_intent": "Convey stability.",
            "linked_concept_family": family_label,
        },
    )
    assert r.status_code == 200, r.text
    assert r.json()["assessment"]
    # The persisted sketch is now reachable via the project + the list route.
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "sketch"
    assert len(project["sketches"]) == 1
    assert project["sketches"][0]["coach_feedback"] is not None
    r = client.get(f"/api/projects/{project_id}/sketches")
    assert r.status_code == 200
    assert len(r.json()) == 1

    # Stage 9: Presentation.
    r = client.post(f"/api/projects/{project_id}/presentation")
    assert r.status_code == 200, r.text
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "presentation"
    assert project["presentation"] is not None


def test_pipeline_client_fit_and_concept_prompt(client: TestClient):
    """After Judge, the Client Fit and Concept Prompt stages advance + persist.

    Closes the coverage gap where the direct-path walk skipped the two stages
    added on this branch (judge -> client_fit -> concept_prompt).
    """
    project = _create_project(client)
    pid = project["id"]

    # Walk forward through Judge (prerequisite for both new stages).
    for stage in ("analyse", "strategy", "insight", "create", "judge"):
        r = client.post(f"/api/projects/{pid}/{stage}")
        assert r.status_code == 200, (stage, r.text)

    # Client Fit — predicts which family THIS client will prefer.
    r = client.post(f"/api/projects/{pid}/client-fit")
    assert r.status_code == 200, r.text
    appeal = r.json()
    assert appeal["recommended_family"]
    assert appeal["persona"]["archetype"]
    project = client.get(f"/api/projects/{pid}").json()
    assert project["stage"] == "client_fit"
    assert project["appeal_report"] is not None
    assert project["client_persona"] is not None

    # Concept Prompt — one executable concept per family, steered by the persona.
    r = client.post(f"/api/projects/{pid}/concept-prompts")
    assert r.status_code == 200, r.text
    concepts = r.json()
    assert isinstance(concepts, list)
    assert len(concepts) == len(project["concept_families"])
    project = client.get(f"/api/projects/{pid}").json()
    assert project["stage"] == "concept_prompt"
    assert project["concept_prompts"] is not None


def test_pipeline_workshop_path(client: TestClient):
    """Short brief → score < 70 → workshop enriches the brief → proceed to Strategy."""
    # A very short brief scores low on the mock heuristic.
    project = _create_project(client, brief="make a logo")
    project_id = project["id"]

    r = client.post(f"/api/projects/{project_id}/analyse")
    assert r.status_code == 200, r.text
    assert r.json()["brand_confidence_score"] < 70

    # Enter the workshop (designer-facing flow): share → answer → complete.
    r = client.post(f"/api/projects/{project_id}/workshop/share")
    assert r.status_code == 200, r.text
    assert "share_token" in r.json()
    project = client.get(f"/api/projects/{project_id}").json()
    assert project["stage"] == "workshop"

    # Submit a couple of answers (enriches the brief on completion).
    for stage, qid in [(1, "target_audience"), (2, "positioning")]:
        r = client.post(
            f"/api/projects/{project_id}/workshop/answer",
            json={"stage": stage, "question_id": qid, "answer": "Some detail " * 20, "answer_type": "text"},
        )
        assert r.status_code == 200, r.text

    # Completing re-analyses the enriched brief and resets stage to discovery.
    r = client.post(f"/api/projects/{project_id}/workshop/complete")
    assert r.status_code == 200, r.text
    project = r.json()
    # The enriched brief is longer, so the mock score should now be >= 70.
    assert project["brand_confidence_score"] >= 70
    assert project["stage"] == "discovery"

    # Strategy should now be permitted.
    r = client.post(f"/api/projects/{project_id}/strategy")
    assert r.status_code == 200, r.text


def test_strategy_requires_confidence(client: TestClient):
    """A low-confidence brief must be blocked from Strategy (DR-1 gate)."""
    project = _create_project(client, brief="tiny")
    project_id = project["id"]

    client.post(f"/api/projects/{project_id}/analyse")
    r = client.post(f"/api/projects/{project_id}/strategy")
    assert r.status_code == 400
    assert "Brand Confidence" in r.json()["detail"]


def test_sketch_image_upload(client: TestClient, tmp_path, monkeypatch):
    """Multipart sketch upload stores the image and serves it back (Stage 8)."""
    import app.routers as routers

    # Redirect storage into the test's tmp dir so the suite stays hermetic.
    monkeypatch.setattr(routers, "_UPLOAD_DIR", tmp_path)

    project = _create_project(client)
    pid = project["id"]

    # A minimal valid 1x1 PNG.
    png = bytes.fromhex(
        "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
        "0000000d49444154789c626001000000050001a5f645400000000049454e44ae426082"
    )
    r = client.post(
        f"/api/projects/{pid}/sketches/upload",
        files={"image": ("sketch.png", png, "image/png")},
        data={"description": "A geometric keystone mark.", "design_intent": "Convey stability."},
    )
    assert r.status_code == 200, r.text
    sketch = r.json()
    assert sketch["sketch_number"] == 1
    assert sketch["image_url"] == f"/api/projects/{pid}/sketches/{sketch['id']}/image"

    # The stored file exists and the serving endpoint returns it.
    stored = list((tmp_path / str(pid)).glob("sketch-*.png"))
    assert len(stored) == 1 and stored[0].read_bytes() == png
    r = client.get(f"/api/projects/{pid}/sketches/{sketch['id']}/image")
    assert r.status_code == 200
    assert r.content == png

    # It appears in the sketch list with feedback, and the stage advanced.
    r = client.get(f"/api/projects/{pid}/sketches")
    assert r.status_code == 200
    listed = r.json()
    assert len(listed) == 1 and listed[0]["image_url"]
    assert listed[0]["coach_feedback"] is not None


def test_sketch_image_upload_rejects_bad_type(client: TestClient, tmp_path, monkeypatch):
    """Non-image content types must be rejected with a clear 400."""
    import app.routers as routers

    monkeypatch.setattr(routers, "_UPLOAD_DIR", tmp_path)
    project = _create_project(client)
    pid = project["id"]

    r = client.post(
        f"/api/projects/{pid}/sketches/upload",
        files={"image": ("notes.txt", b"not an image", "text/plain")},
    )
    assert r.status_code == 400
    assert "Unsupported image type" in r.json()["detail"]


def test_provider_guard_rejects_openai_without_key(client: TestClient):
    """LOGOMIND_AI_PROVIDER=openai without a key must raise, not silently mock."""
    import os

    import app.services.ai_orchestrator as orch

    saved = os.environ.get("LOGOMIND_AI_PROVIDER")
    orch._provider = None
    os.environ["LOGOMIND_AI_PROVIDER"] = "openai"
    os.environ.pop("OPENAI_API_KEY", None)
    try:
        raised = False
        try:
            orch.get_ai_orchestrator()
        except RuntimeError:
            raised = True
        assert raised, "Expected RuntimeError for openai provider without a key"
    finally:
        # Restore mock for the rest of the session.
        os.environ["LOGOMIND_AI_PROVIDER"] = "mock"
        orch._provider = None
        orch.get_ai_orchestrator()
        if saved is not None:
            os.environ["LOGOMIND_AI_PROVIDER"] = saved
