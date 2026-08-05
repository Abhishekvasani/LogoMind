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
