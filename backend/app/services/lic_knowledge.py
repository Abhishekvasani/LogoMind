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


def _slice_between(md: str, start_anchor: str, end_anchors: tuple, max_chars: int = 3500) -> str:
    """Slice from `start_anchor` to the first `end_anchor` found after it.

    Falls back to a char-bounded slice if no end anchor matches. Returns "" if
    the start anchor isn't found (engine degrades gracefully).
    """
    start = md.find(start_anchor)
    if start == -1:
        return ""
    end = len(md)
    for anchor in end_anchors:
        pos = md.find(anchor, start + len(start_anchor))
        if pos != -1:
            end = min(end, pos)
    end = min(end, start + max_chars)
    return md[start:end].strip()


def _slice_bs001_positioning(md: str) -> str:
    """Positioning Statement template + Positioning Audit."""
    return _slice_between(
        md,
        "**The Positioning Statement.**",
        ("**The Sacrifice Test.**", "**Positioning Failure Modes.**", "## ", "---"),
    )


def _slice_bs002_differentiation(md: str) -> str:
    """Differentiation Audit (Three Tests) + Five Dimensions + False Differentiation Detector."""
    return _slice_between(
        md,
        "**The Differentiation Audit.**",
        ("**How It Passes the Three Tests.**", "**Case Study", "**Common False"),
        max_chars=4500,
    )


def _slice_ph003_simplicity(md: str) -> str:
    """Reduction Sequence + Four Tests of a Simple Mark."""
    return _slice_between(
        md,
        "**The Professional Reduction Sequence.**",
        ("**Simplicity Resolves Subjectivity.**", "**Professional Questions", "**The Four Failure"),
    )


def _slice_ph004_clarity(md: str) -> str:
    """Clarity Audit + Four Clarity Fixes."""
    return _slice_between(
        md,
        "**The Clarity Audit.**",
        ("**Clarity Resolves Subjectivity.**", "**Professional Questions", "**The Four Clarity Failures"),
    )


def _slice_color_volume(md: str) -> str:
    """Compact the 10 colour entries to one row each + the Colour Selection Framework.

    Per entry: psychology, variations, originality risk, best pairings, best
    for — the fields the Create engine cross-references to choose and justify a
    palette instead of defaulting to the sea-of-blue/green generic choice.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-CL-\d+) — (.+)$", md, re.MULTILINE):
        cid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 1500
        block = md[block_start:block_end]
        psych = _first_field(block, "Psychology")
        variations = _first_field(block, "Variations")
        risk = _first_field(block, "Originality Risk").replace("Originality Risk:", "").strip()
        pairings = _first_field(block, "Best Pairings")
        best_for = _first_field(block, "Best For")
        rows.append(
            f"- {name} ({cid}): psych=[{psych}]; variations=[{variations}]; "
            f"risk={risk}; pairings=[{pairings}]; best_for=[{best_for}]"
        )
    body = "\n".join(rows)
    framework = _slice_between(
        md,
        "## Colour Selection Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=2000,
    )
    accessibility = _slice_between(
        md,
        "## Colour Accessibility Standards",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=2200,
    )
    if not body:
        return ""
    parts = f"{body}\n\n--- Colour Selection Framework (apply when choosing palette) ---\n{framework}"
    if accessibility:
        parts += f"\n\n--- Colour Accessibility Standards (WCAG + colour-blind rules) ---\n{accessibility}"
    return parts


def _slice_type_volume(md: str) -> str:
    """Compact the 10 type categories to one row each + the Typography Selection Framework.

    Per entry: personality, industry fit, emotional associations, originality
    risk, best for — so the Create engine grounds its typography direction in
    letterform personality rather than the default Helvetica/Inter.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-TY-\d+) — (.+)$", md, re.MULTILINE):
        tid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 1500
        block = md[block_start:block_end]
        personality = _first_field(block, "Personality")
        fit = _first_field(block, "Industry Fit")
        emo = _first_field(block, "Emotional Associations")
        risk = _first_field(block, "Originality Risk").replace("Originality Risk:", "").strip()
        best_for = _first_field(block, "Best For")
        rows.append(
            f"- {name} ({tid}): personality=[{personality}]; fit=[{fit}]; "
            f"emotion=[{emo}]; risk={risk}; best_for=[{best_for}]"
        )
    body = "\n".join(rows)
    framework = _slice_between(
        md,
        "## Typography Selection Framework",
        ("## Weight, Case", "## Volume Metadata"),
        max_chars=2000,
    )
    semantics = _slice_between(
        md,
        "## Weight, Case & Tracking Semantics",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=2600,
    )
    if not body:
        return ""
    parts = f"{body}\n\n--- Typography Selection Framework (apply when choosing type) ---\n{framework}"
    if semantics:
        parts += f"\n\n--- Weight, Case & Tracking Semantics + Pairing Rules ---\n{semantics}"
    return parts


def _slice_identity_volume(md: str) -> str:
    """Compact the 10 identity concepts (name + definition) + the Logo Types table.

    Gives the Create engine the structural vocabulary (negative space, grids,
    stroke weight, symmetry, optical correction, scale behaviour) and the
    operational logo-type classification, so composition is a craft decision
    rather than a default centred-mark habit.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-ID-\d+) — (.+)$", md, re.MULTILINE):
        iid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 1500
        block = md[block_start:block_end]
        definition = _first_field(block, "Definition")
        rows.append(f"- {name} ({iid}): {definition}")
    body = "\n".join(rows)
    # The Five Types table + strategic-choice factors are the most operational part.
    logo_types = _slice_between(
        md,
        "**The Five Types:**",
        ("**Common Mistakes:**",),
        max_chars=2500,
    )
    if not body:
        return ""
    return f"{body}\n\n--- Logo Types classification (RS-LIC-ID-008) ---\n{logo_types}"


# The ten remaining LIC volumes share the 11-section textbook template: each
# carries one operational core (an audit/test/framework run) bracketed by
# "**The <Framework>.**" and "**Common Professional Mistakes.**". The slicers
# below pull exactly that run — the tables and questions an engine can apply —
# never the narrative galleries.


def _slice_ph001_meaning(md: str) -> str:
    """Professional Design Sequence + pre-sketching questions."""
    return _slice_between(
        md,
        "**The Professional Design Sequence.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph002_purpose(md: str) -> str:
    """Purpose-Discovery Sequence + pre-strategy questions."""
    return _slice_between(
        md,
        "**The Professional Purpose-Discovery Sequence.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph006_memorability(md: str) -> str:
    """Four Anchors of Memorability + Recall Test."""
    return _slice_between(
        md,
        "**The Four Anchors of Memorability.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph007_authenticity(md: str) -> str:
    """Authenticity Audit + Specificity Principle."""
    return _slice_between(
        md,
        "**The Authenticity Audit.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph008_timelessness(md: str) -> str:
    """Timelessness Audit + Trend Taxonomy + Timelessness Test.

    The Trend Taxonomy (timeless/emerging/short-lived/overused) is the Insight
    engine's trend-classification scheme.
    """
    return _slice_between(
        md,
        "**The Timelessness Audit.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph009_relevance(md: str) -> str:
    """Relevance Audit + Relevance Dial + Forced-Relevance Test.

    The Relevance Dial supplies the timeless↔trend-forward mix ratios the
    Insight engine cites.
    """
    return _slice_between(
        md,
        "**The Relevance Audit.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_ph010_consistency(md: str) -> str:
    """Consistency Audit + Coherence/Uniformity Spectrum + Consistency Test."""
    return _slice_between(
        md,
        "**The Consistency Audit.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_bs003_audience(md: str) -> str:
    """Audience Definition Framework + audience→identity calibration."""
    return _slice_between(
        md,
        "**The Audience Definition Framework.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_bs004_personality(md: str) -> str:
    """Personality Definition Framework + personality→identity mapping."""
    return _slice_between(
        md,
        "**The Personality Definition Framework.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
    )


def _slice_bs005_archetypes(md: str) -> str:
    """Archetype Audit + the Twelve Classical Archetypes diagnostic table +
    archetype→personality→identity mapping.

    The twelve-archetype table is the persona vocabulary the Client Fit engine
    models its client archetype against, so keep a generous cap.
    """
    return _slice_between(
        md,
        "**The Archetype Audit.**",
        ("**Common Professional Mistakes.**", "**Case Study", "## "),
        max_chars=4000,
    )


def _slice_industry_volume(md: str) -> str:
    """Compact the industry entries to one row each + the Industry Intelligence
    Framework.

    Per entry: core signal, symbol/colour/typography conventions, the cliché
    list, and the white-space opportunities — exactly the fields the Insight
    engine reports (conventions / cliché_avoidance / opportunities) and the
    Create engine deviates from with intent.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-IND-\d+) — (.+)$", md, re.MULTILINE):
        iid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 1500
        block = md[block_start:block_end]
        signal = _first_field(block, "Core Signal")
        symbols = _first_field(block, "Symbol Conventions")
        colours = _first_field(block, "Colour Conventions")
        typeconv = _first_field(block, "Typography Conventions")
        cliches = _first_field(block, "Clichés to Avoid")
        opportunities = _first_field(block, "Opportunities")
        rows.append(
            f"- {name} ({iid}): signal=[{signal}]; symbols=[{symbols}]; "
            f"colours=[{colours}]; type=[{typeconv}]; "
            f"AVOID clichés=[{cliches}]; opportunities=[{opportunities}]"
        )
    body = "\n".join(rows)
    framework = _slice_between(
        md,
        "## Industry Intelligence Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=2200,
    )
    if not body:
        return ""
    return f"{body}\n\n--- Industry Intelligence Framework (apply when working per-category) ---\n{framework}"


def _slice_client_psychology_volume(md: str) -> str:
    """Compact the decision-maker types to one row each + the Feedback Decoder,
    Objection Taxonomy, and Client Psychology Framework.

    The type rows carry aesthetic lean + boldness tolerance — the exact fields
    the Client Fit engine's persona predicts — plus recognition cues and how to
    win them. The two tables serve feedback interpretation (objection handling
    in the Presentation engine).
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-PSY-\d+) — (.+)$", md, re.MULTILINE):
        pid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 2000
        block = md[block_start:block_end]
        cues = _first_field(block, "Recognition Cues")
        if not cues:
            continue  # the decoder/taxonomy entries are appended as tables below
        values = _first_field(block, "What They Value")
        lean = _first_field(block, "Aesthetic Lean")
        boldness = _first_field(block, "Boldness Tolerance")
        feedback = _first_field(block, "Feedback Style")
        win = _first_field(block, "How to Win Them")
        watch = _first_field(block, "Watch Out")
        rows.append(
            f"- {name} ({pid}): cues=[{cues}]; values=[{values}]; lean={lean}; "
            f"boldness={boldness}; feedback=[{feedback}]; win=[{win}]; risk=[{watch}]"
        )
    body = "\n".join(rows)
    decoder = _slice_between(
        md,
        "## RS-LIC-PSY-009 — The Feedback Decoder",
        ("## RS-LIC-PSY-010",),
        max_chars=3200,
    )
    objections = _slice_between(
        md,
        "## RS-LIC-PSY-010 — The Objection Taxonomy",
        ("## Volume Metadata",),
        max_chars=3200,
    )
    framework = _slice_between(
        md,
        "## Client Psychology Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=1600,
    )
    rationale = _slice_between(
        md,
        "## RS-LIC-PSY-011 — The Rationale Narrative",
        ("## Volume Metadata",),
        max_chars=1800,
    )
    if not body:
        return ""
    return (
        f"{body}\n\n--- The Feedback Decoder (translate taste-language) ---\n{decoder}"
        f"\n\n--- The Objection Taxonomy (answer the armoured question) ---\n{objections}"
        f"\n\n--- The Rationale Narrative (Meaning → Evidence → Application → Consequence) ---\n{rationale}"
        f"\n\n--- Client Psychology Framework ---\n{framework}"
    )


def _slice_production_volume(md: str) -> str:
    """Compact the production entries to one row each + the Production Checklist.

    Scale/stroke craft, file formats, colour versions, clear space, and handoff
    standards — the constraints a concept must survive, used by Concept Prompt
    (scale-aware wireframes), Sketch Coach (production pitfalls), and SSB.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-PRD-\d+) — (.+)$", md, re.MULTILINE):
        pid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 2000
        block = md[block_start:block_end]
        definition = _first_field(block, "Definition")
        best_for = _first_field(block, "Best For")
        # Pull the concrete rule lines too — they are the operational core.
        rule_lines = [
            line.strip().lstrip("*") for line in block.split("\n")
            if line.strip().startswith("**At ") or line.strip().startswith("**Minimum")
            or line.strip().startswith("**Favicon") or line.strip().startswith("**Monochrome")
        ]
        rules = "; ".join(rule_lines)[:400]
        rows.append(f"- {name} ({pid}): {definition} {('| rules: ' + rules) if rules else ''} | feeds=[{best_for}]")
    body = "\n".join(rows)
    checklist = _slice_between(
        md,
        "## Production Checklist Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=1800,
    )
    if not body:
        return ""
    return f"{body}\n\n--- Production Checklist Framework (test every concept) ---\n{checklist}"


def _slice_contest_volume(md: str) -> str:
    """Compact the contest-dynamics entries to one row each + the Signal
    Framework.

    Formats, the brief reality, rating/elimination signals, reading the room,
    and iteration discipline — the interpretation layer for the Client Fit
    refine loop's contest feedback.
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-CON-\d+) — (.+)$", md, re.MULTILINE):
        cid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 2000
        block = md[block_start:block_end]
        definition = _first_field(block, "Definition")
        best_for = _first_field(block, "Best For")
        rows.append(f"- {name} ({cid}): {definition} | feeds=[{best_for}]")
    body = "\n".join(rows)
    signals = _slice_between(
        md,
        "## Contest Signal Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=1800,
    )
    if not body:
        return ""
    return f"{body}\n\n--- Contest Signal Framework (interpret ratings/eliminations/silence) ---\n{signals}"


def _slice_trademark_volume(md: str) -> str:
    """Compact the trademark entries to one row each + the Trademark Check.

    The distinctiveness spectrum, refusal grounds, clearance basics, and
    red flags — grounding the Judge engine's risk signalling with the legal
    axis under "is it different enough?".
    """
    rows = []
    for m in re.finditer(r"^## (RS-LIC-TM-\d+) — (.+)$", md, re.MULTILINE):
        tid, name = m.group(1), m.group(2)
        block_start = m.end()
        block_end = md.find("\n---\n", block_start)
        if block_end == -1:
            block_end = block_start + 2000
        block = md[block_start:block_end]
        definition = _first_field(block, "Definition")
        best_for = _first_field(block, "Best For")
        # The distinctiveness spectrum levels are TM-001's operational core —
        # keep them in the compacted row.
        spectrum = [
            line.strip() for line in block.split("\n")
            if re.match(r"\*\*(Generic|Descriptive|Suggestive|Arbitrary|Fanciful)", line.strip())
        ]
        spec_txt = (" spectrum=[" + " ".join(spectrum) + "]") if spectrum else ""
        rows.append(f"- {name} ({tid}): {definition}{spec_txt} | feeds=[{best_for}]")
    body = "\n".join(rows)
    check = _slice_between(
        md,
        "## Trademark Check Framework",
        ("*LogoMind Principle", "## Volume Metadata"),
        max_chars=1500,
    )
    if not body:
        return ""
    return f"{body}\n\n--- Trademark Check Framework (distinctiveness risk) ---\n{check}"


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
    ExtractSpec(
        lic_id="RS-LIC-BS-001",
        filename="RS-LIC-BS-001_Brand_Positioning.md",
        slicer=_slice_bs001_positioning,
    ),
    ExtractSpec(
        lic_id="RS-LIC-BS-002",
        filename="RS-LIC-BS-002_Brand_Differentiation.md",
        slicer=_slice_bs002_differentiation,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-003",
        filename="RS-LIC-PH-003_Simplicity.md",
        slicer=_slice_ph003_simplicity,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-004",
        filename="RS-LIC-PH-004_Clarity.md",
        slicer=_slice_ph004_clarity,
    ),
    ExtractSpec(
        lic_id="RS-LIC-CL-VOLUME",
        filename="RS-LIC-CL-VOLUME.md",
        slicer=_slice_color_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-TY-VOLUME",
        filename="RS-LIC-TY-VOLUME.md",
        slicer=_slice_type_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-ID-VOLUME",
        filename="RS-LIC-ID-VOLUME.md",
        slicer=_slice_identity_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-001",
        filename="RS-LIC-PH-001_Meaning.md",
        slicer=_slice_ph001_meaning,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-002",
        filename="RS-LIC-PH-002_Purpose.md",
        slicer=_slice_ph002_purpose,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-006",
        filename="RS-LIC-PH-006_Memorability.md",
        slicer=_slice_ph006_memorability,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-007",
        filename="RS-LIC-PH-007_Authenticity.md",
        slicer=_slice_ph007_authenticity,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-008",
        filename="RS-LIC-PH-008_Timelessness.md",
        slicer=_slice_ph008_timelessness,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-009",
        filename="RS-LIC-PH-009_Relevance.md",
        slicer=_slice_ph009_relevance,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PH-010",
        filename="RS-LIC-PH-010_Consistency.md",
        slicer=_slice_ph010_consistency,
    ),
    ExtractSpec(
        lic_id="RS-LIC-BS-003",
        filename="RS-LIC-BS-003_Target_Audience.md",
        slicer=_slice_bs003_audience,
    ),
    ExtractSpec(
        lic_id="RS-LIC-BS-004",
        filename="RS-LIC-BS-004_Brand_Personality.md",
        slicer=_slice_bs004_personality,
    ),
    ExtractSpec(
        lic_id="RS-LIC-BS-005",
        filename="RS-LIC-BS-005_Brand_Archetypes.md",
        slicer=_slice_bs005_archetypes,
    ),
    ExtractSpec(
        lic_id="RS-LIC-IND-VOLUME",
        filename="RS-LIC-IND-VOLUME.md",
        slicer=_slice_industry_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PSY-VOLUME",
        filename="RS-LIC-PSY-VOLUME.md",
        slicer=_slice_client_psychology_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-PRD-VOLUME",
        filename="RS-LIC-PRD-VOLUME.md",
        slicer=_slice_production_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-CON-VOLUME",
        filename="RS-LIC-CON-VOLUME.md",
        slicer=_slice_contest_volume,
    ),
    ExtractSpec(
        lic_id="RS-LIC-TM-VOLUME",
        filename="RS-LIC-TM-VOLUME.md",
        slicer=_slice_trademark_volume,
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
