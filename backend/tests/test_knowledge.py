"""
Tests for the LIC knowledge loader.

The loader reads curated operational sections from the LIC markdown files at
startup and exposes them as minimum-token strings. These tests guard:
  - the extracts actually load and contain the operational tools (tables/tests)
  - unknown ids degrade gracefully (engine keeps working without injection)
  - the prompt-builder helper wraps extracts correctly
"""

from app.services import lic_knowledge as lk


def test_loads_operational_extracts():
    """The PH-005 and Symbol Volume extracts resolve to real content."""
    lk.load(force=True)
    ph = lk.get("RS-LIC-PH-005")
    assert "Cross-Pollination" in ph or "Trust (finance)" in ph, "PH-005 missing Cross-Pollination table"
    assert "Meaning Test" in ph and "Non-Arbitrary Test" in ph, "PH-005 missing 5 Originality Tests"

    sy = lk.get("RS-LIC-SY-VOLUME")
    assert "Circle" in sy, "Symbol volume missing Circle"
    # At least 10 of the 15 symbol rows resolved.
    rows = [l for l in sy.split("\n") if l.startswith("- ")]
    assert len(rows) >= 10, f"Expected >=10 symbol rows, got {len(rows)}"


def test_unknown_lic_returns_empty():
    """Unknown ids return '' so engines degrade to the old named-reference behaviour."""
    lk.load(force=True)
    assert lk.get("RS-LIC-DOES-NOT-EXIST") == ""
    assert lk.knowledge_block(["NOPE", "ALSO-NOPE"]) == ""


def test_knowledge_block_formats_extracts():
    """knowledge_block wraps resolved extracts in the canonical heading."""
    lk.load(force=True)
    block = lk.knowledge_block(["RS-LIC-PH-005"])
    assert "CANONICAL LOGOMIND KNOWLEDGE" in block
    assert "RS-LIC-PH-005" in block
    assert "END KNOWLEDGE" in block


def test_load_is_idempotent():
    """Calling load() twice is safe (lifespan + tests both call it)."""
    lk.load(force=True)
    first = lk.get("RS-LIC-PH-005")
    lk.load()  # no force — should be a no-op
    assert lk.get("RS-LIC-PH-005") == first


def test_added_slicers_resolve():
    """The added slicers each resolve to non-empty content.

    Guards against silent breakage: if a source markdown shifts or a slicer
    regex drifts, the engine would inject an empty knowledge block instead of
    catching it. These ids back the Create + Concept Prompt anti-generic
    directives, so an empty extract degrades output quality with no error.
    """
    lk.load(force=True)
    for lic_id in (
        "RS-LIC-BS-001",       # Brand Positioning
        "RS-LIC-BS-002",       # Brand Differentiation
        "RS-LIC-PH-003",       # Simplicity
        "RS-LIC-PH-004",       # Clarity
        "RS-LIC-CL-VOLUME",    # Color volume
        "RS-LIC-TY-VOLUME",    # Typography volume
        "RS-LIC-ID-VOLUME",    # Identity volume
    ):
        content = lk.get(lic_id)
        assert content, f"{lic_id} resolved empty — slicer or source file may have shifted"


def test_every_registered_lic_resolves():
    """ALL registry entries (19 volumes) resolve to a non-empty extract.

    An empty extract silently degrades the engine that injects it, so the full
    registry is guarded here, not just hand-picked ids.
    """
    lk.load(force=True)
    assert lk._REGISTRY, "registry is empty"
    for spec in lk._REGISTRY:
        content = lk.get(spec.lic_id)
        assert content, f"{spec.lic_id} ({spec.filename}) resolved empty"


def test_engine_prompts_carry_knowledge():
    """Every knowledge-injecting engine prompt actually contains a block.

    Guards the wiring itself: a dropped knowledge_block() call (e.g. during a
    prompt refactor) would silently return the engine to ungrounded behaviour.
    """
    from app.services import engines, client_fit_engine, concept_engine

    lk.load(force=True)
    cases = [
        (engines.STRATEGY_SYSTEM_PROMPT, "RS-LIC-BS-001"),      # 5 BS frameworks
        (engines.INSIGHT_SYSTEM_PROMPT, "RS-LIC-PH-008"),       # Trend Taxonomy
        (engines.INSIGHT_SYSTEM_PROMPT, "RS-LIC-SY-VOLUME"),    # cliché detection
        (engines.CREATE_SYSTEM_PROMPT, "RS-LIC-SY-VOLUME"),
        (engines.JUDGE_SYSTEM_PROMPT, "RS-LIC-PH-003"),         # simplicity dim
        (engines.SSB_SYSTEM_PROMPT, "RS-LIC-ID-VOLUME"),        # grids / logo types
        (engines.COACH_SYSTEM_PROMPT, "RS-LIC-PH-004"),         # clarity audit
        (client_fit_engine.CLIENT_FIT_SYSTEM_PROMPT, "RS-LIC-BS-005"),  # archetypes
        (concept_engine.CONCEPT_PROMPT_SYSTEM_PROMPT, "RS-LIC-ID-VOLUME"),
    ]
    for prompt, marker in cases:
        assert "CANONICAL LOGOMIND KNOWLEDGE" in prompt, "knowledge block missing"
        assert f"--- {marker} ---" in prompt, f"{marker} not injected"
