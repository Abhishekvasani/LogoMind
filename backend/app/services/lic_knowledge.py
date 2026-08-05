"""
LIC Knowledge Loader — embeds curated operational extracts into engine prompts.

LogoMind's knowledge base (05_RS_LICs/) is deep, but the engines used to only
NAME the LICs by id ("Apply RS-LIC-PH-005 Originality") and trust the model's
training-data memory of what those frameworks contain. This module fixes that:
it reads the OPERATIONAL sections of the relevant LICs (the tables, tests,
symbol rows — not the prose) ONCE at startup, caches them, and exposes them as
minimum-token strings the engines interpolate into system prompts.

Design (Approach 1, minimal):
  - One module. A registry maps LIC id -> an ExtractSpec (file + slicer).
  - load() runs once at startup (idempotent); extracts cached in _EXTRACTS.
  - get(lic_id) returns the cached text, or "" if missing/unloaded (engines
    degrade gracefully to the old named-reference behaviour).
  - No RAG, no embeddings, no DB. Curated, deterministic, minimum-token.

The slicer targets specific markdown anchors so we pull only the operational
core (e.g. the Cross-Pollination table + 5 Originality Tests, ~250 tokens),
not the whole 450-line LIC (~4500 tokens).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Dict, Optional, Tuple

# 05_RS_LICs lives at the repo root, three parents up from this file:
#   backend/app/services/lic_knowledge.py -> app -> backend -> repo root
_LIC_DIR = Path(__file__).resolve().parents[3] / "05_RS_LICs"


# ─── Slicers ────────────────────────────────────────────────────────────
# A slicer takes the full markdown text of a LIC and returns the operational
# extract as a compact string. Each is tailored to that LIC's structure.


def _slice_ph005_originality(md: str) -> str:
    """The Combination Method + Cross-Pollination table + 5 Originality Tests.

    These are the Create/Judge engine's actual tools. Pulls lines 133-172
    region by anchor so it survives minor edits to surrounding prose.
    """
    # From "**The Combination Method.**" through the end of the Originality
    # Test explanation (the line after the 5-tests table summary).
    start = md.find("**The Combination Method.**")
    if start == -1:
        return ""
    # End at the next "**...**" section header after the Originality Test table,
    # or 60 lines after start as a safety bound.
    end_anchor = md.find("**Originality vs. Tradition.**", start)
    if end_anchor == -1:
        end_anchor = start + 4000
    return md[start:end_anchor].strip()


def _slice_symbol_volume(md: str) -> str:
    """Compact the 15 symbol entries into one row each.

    Each symbol block starts with "## RS-LIC-SY-NNN — <Name>". We extract the
    name, primary/secondary meanings, originality risk, and "Avoid When" — the
    fields the Create engine cross-pollinates against.
    """
    rows = []
    # Match each symbol header.
    for m in re.finditer(r"^## (RS-LIC-SY-\d+) — (.+)$", md, re.MULTILINE):
        sid, name = m.group(1), m.group(2)
        # Capture the block until the next "---" separator.
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 1500
        block = md[block_start:block_end]

        primary = _first_field(block, "Primary Meanings")
        secondary = _first_field(block, "Secondary Meanings")
        risk = _first_field(block, "Originality Risk")
        avoid = _first_field(block, "Avoid When")

        risk_short = risk.replace("Originality Risk:", "").strip()
        rows.append(
            f"- {name} ({sid}): meanings=[{primary}]; "
            f"secondary=[{secondary}]; risk={risk_short}; avoid={avoid}"
        )
    return "\n".join(rows) if rows else ""


def _first_field(block: str, label: str) -> str:
    """Extract the text after '**<label>:**' in a symbol block."""
    m = re.search(rf"\*?\*?{re.escape(label)}\*?\*?:\s*\*?\*?(.+)", block)
    if not m:
        return ""
    # Take up to the end of the line.
    line = m.group(1).split("\n")[0].strip().strip("*")
    return line


# ─── Registry ───────────────────────────────────────────────────────────


@dataclass(frozen=True)
class ExtractSpec:
    lic_id: str
    filename: str
    slicer: Callable[[str], str]


_REGISTRY: Tuple[ExtractSpec, ...] = (
    ExtractSpec(
        lic_id="RS-LIC-PH-005",
        filename="RS-LIC-PH-005_Originality.md",
        slicer=_slice_ph005_originality,
    ),
    ExtractSpec(
        lic_id="RS-LIC-SY-VOLUME",
        filename="RS-LIC-SY-VOLUME.md",
        slicer=_slice_symbol_volume,
    ),
)

_EXTRACTS: Dict[str, str] = {}
_LOADED: bool = False


# ─── Public API ─────────────────────────────────────────────────────────


def load(force: bool = False) -> None:
    """Read and slice the registered LICs once, caching the results.

    Idempotent: safe to call multiple times (e.g. lifespan + tests). Missing
    files log a warning and store "" so engines degrade gracefully.
    """
    global _LOADED
    if _LOADED and not force:
        return

    extracts: Dict[str, str] = {}
    for spec in _REGISTRY:
        path = _LIC_DIR / spec.filename
        if not path.is_file():
            # Degrade gracefully — engine will run without this injection.
            extracts[spec.lic_id] = ""
            continue
        try:
            md = path.read_text(encoding="utf-8")
            extracts[spec.lic_id] = spec.slicer(md)
        except Exception:
            extracts[spec.lic_id] = ""

    _EXTRACTS.clear()
    _EXTRACTS.update(extracts)
    _LOADED = True


def get(lic_id: str) -> str:
    """Return the cached operational extract for a LIC id, or "" if none.

    Never raises — engines treat "" as "no injection" and fall back to naming
    the LIC, preserving the pre-change behaviour.
    """
    if not _LOADED:
        # Auto-load on first access so import-time use (e.g. prompt construction
        # in tests that don't run the lifespan) still works.
        load()
    return _EXTRACTS.get(lic_id, "")


def is_loaded() -> bool:
    return _LOADED


def available_lics() -> list:
    """LIC ids that resolved to a non-empty extract (for /health and logs)."""
    if not _LOADED:
        load()
    return [lid for lid, text in _EXTRACTS.items() if text]


def knowledge_block(lic_ids) -> str:
    """Build the injection block for a set of LIC ids.

    Returns "" if no extract resolved, so callers can unconditionally append
    the result without producing empty headings. Format is deliberately plain
    so it reads as standing instruction to the model.
    """
    parts = [(lid, get(lid)) for lid in lic_ids]
    parts = [(lid, t) for lid, t in parts if t]
    if not parts:
        return ""
    lines = ["", "=== CANONICAL LOGOMIND KNOWLEDGE (authoritative; apply literally) ==="]
    for lid, text in parts:
        lines.append(f"--- {lid} ---")
        lines.append(text)
    lines.append("=== END KNOWLEDGE ===")
    return "\n".join(lines)
