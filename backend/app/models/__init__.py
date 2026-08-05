"""
LogoMind Database Models.

SQLAlchemy models implementing the data layer for the LOGOS pipeline.
Each model maps to a stage of the user journey (PROD-JOURNEY-001)
and is consumed by the corresponding engine (LOG-* series).

Data model principles (per PROD-SCREEN-001 and Architecture Freeze):
- Project is the root entity; everything descends from it.
- Each pipeline stage produces a JSON document stored on the project.
- Confidence levels (LM-STD-003) are explicit; never fake certainty.
- Contradictions are surfaced, never silently resolved (DR-2 of Strategy Engine).
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column, String, Text, Integer, Float, DateTime, ForeignKey, JSON, Boolean, Enum
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    """A LogoMind user (Maya, Marcus, or Elena personas — PROD-PERSONA-001)."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)  # nullable for OAuth-only users
    role = Column(String, default="designer")  # designer | studio_lead | entrepreneur
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")


class Project(Base):
    """
    A LogoMind project — the root entity of the user journey.

    Maps to Stage 1 (Start) of PROD-JOURNEY-001. Contains the raw client brief
    and progresses through the pipeline stages, each updating this record.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Stage 1 inputs (PROD-SCREEN-001 Screen 2)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    client_brief = Column(Text, nullable=False)  # any completeness level
    client_contact = Column(String, nullable=True)  # for Workshop link sharing

    # Pipeline status (which stage the project is in — PROD-JOURNEY-001)
    # entry | discovery | workshop | strategy | insight | create | judge | concept_prompt | ssb | sketch | presentation | complete
    stage = Column(String, default="entry", nullable=False, index=True)

    # The Brand Confidence Score (0-100) from LOG-DISC-001
    brand_confidence_score = Column(Float, default=0.0)
    brand_confidence_level = Column(String, default="unknown")  # unknown | low | medium | high

    # Pipeline outputs (JSON documents, one per stage)
    discovery_summary = Column(JSON, nullable=True)       # LOG-DISC-001 output
    brand_dna = Column(JSON, nullable=True)               # LOG-STRAT-001 output
    insight_report = Column(JSON, nullable=True)          # LOG-INSIGHT-001 output
    concept_families = Column(JSON, nullable=True)        # LOG-CREATE-001 output
    judge_report = Column(JSON, nullable=True)            # LOG-JUDGE-001 output
    concept_prompts = Column(JSON, nullable=True)         # LOG-CP-001 output
    ssb = Column(JSON, nullable=True)                     # PROD-SSB-001 output
    presentation = Column(JSON, nullable=True)            # LOG-PRESENT-001 output

    # Workshop state (LOG-DISC-001 Workshop Mode)
    workshop_state = Column(JSON, nullable=True)  # current stage, answers, etc.
    workshop_share_token = Column(String, nullable=True, index=True)  # client link

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="projects")
    sketches = relationship("Sketch", back_populates="project", cascade="all, delete-orphan")
    decision_log = relationship("DecisionLog", back_populates="project", cascade="all, delete-orphan")


class Sketch(Base):
    """
    A designer-uploaded sketch for Sketch Coach critique (LOG-COACH-001).

    Maps to Stage 8 (Sketch) of PROD-JOURNEY-001.
    """
    __tablename__ = "sketches"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    sketch_number = Column(Integer, nullable=False)  # 1, 2, 3...
    description = Column(Text, nullable=True)        # designer's notes
    design_intent = Column(Text, nullable=True)      # what they were exploring
    linked_concept_family = Column(String, nullable=True)

    # Storage (in v1: URL to cloud storage; in dev: file path)
    image_url = Column(String, nullable=True)
    image_path = Column(String, nullable=True)

    # Sketch Coach output (LOG-COACH-001)
    coach_feedback = Column(JSON, nullable=True)
    coach_confidence = Column(String, nullable=True)  # C-level per LM-STD-003

    # Client feedback (per Project Memory — FD-007)
    client_feedback = Column(Text, nullable=True)
    revision_status = Column(String, default="draft")  # draft | presented | approved | rejected

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="sketches")


class DecisionLog(Base):
    """
    An entry in the project's Decision Log.

    Records WHY decisions were made — per the Founder's Charter tradition
    and the Strategy Engine's Decision Rules (surface, don't silently resolve).
    """
    __tablename__ = "decision_log"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    decision = Column(String, nullable=False)  # what was decided
    reason = Column(Text, nullable=True)        # why
    stage = Column(String, nullable=True)       # which pipeline stage
    made_by = Column(String, default="system")  # system | user | client

    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="decision_log")


class LMKCEntry(Base):
    """
    A LogoMind Knowledge Core entry (RS-LIC-* and future Symbol/Color/etc.).

    In v1, this stores the LICs as structured documents the engines can query.
    Maps to the LMKC/LKG spec (CTO Decision #027).
    """
    __tablename__ = "lmkc_entries"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True, nullable=False)  # e.g., RS-LIC-PH-001
    category = Column(String, nullable=False, index=True)              # Philosophy, Brand Strategy, etc.
    title = Column(String, nullable=False)
    version = Column(String, default="1.0")
    status = Column(String, default="approved")  # draft | approved | reference_standard

    # Full LIC content (parsed markdown or structured JSON)
    content = Column(JSON, nullable=False)

    # Knowledge Graph relationships (CTO Decision #027 — typed edges)
    relationships = Column(JSON, nullable=True)  # [{type, target_doc_id, weight}]

    # Confidence and consensus (LM-STD-003)
    confidence = Column(String, default="C3")  # C1-C5
    consensus = Column(String, default="medium")  # low | medium | high | expert

    last_reviewed = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConceptFamily(Base):
    """
    A single Concept Family from the Create Engine (LOG-CREATE-001).

    Stored separately from the project's concept_families JSON for queryability.
    """
    __tablename__ = "concept_families"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    family_label = Column(String, nullable=False)        # "A", "B", "C"
    theme = Column(String, nullable=False)
    core_meaning_served = Column(Text, nullable=True)

    # Full family structure (symbols, visual language, reasoning)
    family_data = Column(JSON, nullable=False)

    # Judge evaluation (LOG-JUDGE-001)
    composite_score = Column(Float, nullable=True)
    classification = Column(String, nullable=True)  # recommended | develop | reject
    judge_detail = Column(JSON, nullable=True)      # 10-dimension breakdown
    concept_dna = Column(JSON, nullable=True)       # the Creative Genome fingerprint

    # Designer's selection state
    is_selected = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
