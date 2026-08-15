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
        (engines.INSIGHT_SYSTEM_PROMPT, "RS-LIC-IND-VOLUME"),   # industry conventions
        (engines.CREATE_SYSTEM_PROMPT, "RS-LIC-SY-VOLUME"),
        (engines.CREATE_SYSTEM_PROMPT, "RS-LIC-IND-VOLUME"),    # per-category clichés
        (engines.JUDGE_SYSTEM_PROMPT, "RS-LIC-PH-003"),         # simplicity dim
        (engines.JUDGE_SYSTEM_PROMPT, "RS-LIC-TM-VOLUME"),      # distinctiveness risk
        (engines.SSB_SYSTEM_PROMPT, "RS-LIC-ID-VOLUME"),        # grids / logo types
        (engines.SSB_SYSTEM_PROMPT, "RS-LIC-PRD-VOLUME"),       # production notes
        (engines.COACH_SYSTEM_PROMPT, "RS-LIC-PH-004"),         # clarity audit
        (engines.COACH_SYSTEM_PROMPT, "RS-LIC-PRD-VOLUME"),     # production constraints
        (client_fit_engine.CLIENT_FIT_SYSTEM_PROMPT, "RS-LIC-BS-005"),  # archetypes
        (client_fit_engine.CLIENT_FIT_SYSTEM_PROMPT, "RS-LIC-PSY-VOLUME"),  # decider types
        (client_fit_engine.CLIENT_FIT_SYSTEM_PROMPT, "RS-LIC-CON-VOLUME"),  # contest signals
        (engines.PRESENTATION_SYSTEM_PROMPT, "RS-LIC-PSY-VOLUME"),  # objection taxonomy
        (concept_engine.CONCEPT_PROMPT_SYSTEM_PROMPT, "RS-LIC-ID-VOLUME"),
        (concept_engine.CONCEPT_PROMPT_SYSTEM_PROMPT, "RS-LIC-PRD-VOLUME"),  # scale-aware wireframes
    ]
    for prompt, marker in cases:
        assert "CANONICAL LOGOMIND KNOWLEDGE" in prompt, "knowledge block missing"
        assert f"--- {marker} ---" in prompt, f"{marker} not injected"


def test_industry_volume_content():
    """The Industry Intelligence slice carries the fields the engines consume.

    Insight reports conventions/clichés/opportunities per industry and Create
    avoids the per-category clichés — the slice must expose both, for several
    industries, or it degrades to a decorative injection.
    """
    lk.load(force=True)
    extract = lk.get("RS-LIC-IND-VOLUME")
    assert "RS-LIC-IND-001" in extract and "RS-LIC-IND-014" in extract
    # Field markers the engines read the slice for.
    for marker in ("signal=", "AVOID clichés=", "opportunities=", "Industry Intelligence Framework"):
        assert marker in extract, f"industry slice missing '{marker}'"
    # A known cliché map must survive the compaction (sample check).
    assert "Dumbbell" in extract or "dumbbell" in extract


def test_client_psychology_volume_content():
    """The Client Psychology slice carries its three systems.

    Client Fit predicts personas from the type rows (which must carry the
    aesthetic-lean / boldness-tolerance fields); Presentation answers
    objections from the taxonomy; the decoder must keep its key phrases.
    """
    lk.load(force=True)
    extract = lk.get("RS-LIC-PSY-VOLUME")
    assert "RS-LIC-PSY-001" in extract and "RS-LIC-PSY-008" in extract
    for marker in (
        "lean=", "boldness=",                      # persona-prediction fields
        "The Feedback Decoder",                    # taste-language table
        "The Objection Taxonomy",                  # presentation objection source
        "Client Psychology Framework",
    ):
        assert marker in extract, f"psychology slice missing '{marker}'"
    # Signature decoded phrases must survive the slice (sample check).
    assert "Make it pop" in extract and "too simple" in extract.lower()


def test_expanded_volumes_carry_new_content():
    """The Tier-2 expansions survive slicing with their new payload intact.

    Symbols (33 rows incl. the new cliché-heavy creatures/emblems), colours
    (18 rows + WCAG accessibility), typography (weight/case/tracking +
    pairing), production (checklist), contest (signal framework), trademark
    (distinctiveness spectrum).
    """
    lk.load(force=True)
    sy = lk.get("RS-LIC-SY-VOLUME")
    assert "RS-LIC-SY-050" in sy, "symbol expansion (50 entries) missing"
    assert "Lion" in sy and "Shield" in sy and "Wolf" in sy and "Speech Bubble" in sy
    cl = lk.get("RS-LIC-CL-VOLUME")
    assert "RS-LIC-CL-025" in cl, "colour expansion (25 entries) missing"
    assert "Colour Accessibility Standards" in cl and "WCAG" in cl
    ty = lk.get("RS-LIC-TY-VOLUME")
    assert "RS-LIC-TY-015" in ty, "type expansion (15 categories) missing"
    assert "Weight, Case & Tracking Semantics" in ty and "Pairing" in ty
    ind = lk.get("RS-LIC-IND-VOLUME")
    assert "RS-LIC-IND-020" in ind, "industry expansion (20 categories) missing"
    prd = lk.get("RS-LIC-PRD-VOLUME")
    assert "Production Checklist Framework" in prd and "16px" in prd
    con = lk.get("RS-LIC-CON-VOLUME")
    assert "Contest Signal Framework" in con and "RS-LIC-CON-006" in con
    tm = lk.get("RS-LIC-TM-VOLUME")
    assert "Trademark Check Framework" in tm and "Fanciful" in tm
    psy = lk.get("RS-LIC-PSY-VOLUME")
    assert "RS-LIC-PSY-015" in psy, "psychology expansion (12 types) missing"
    assert "Rationale Narrative" in psy
