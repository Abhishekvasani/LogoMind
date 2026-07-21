"""
LogoMind Pydantic Schemas (API contracts).

These schemas define the wire format between frontend and backend,
and between the FastAPI layer and the AI orchestration layer.

Every schema maps to an engine input or output (LOG-* series) and
conforms to LM-STD-001 through LM-STD-006:
- Confidence levels are explicit (LM-STD-003)
- Statement types are typed (LM-STD-002)
- Terminology is canonical (LM-STD-004)
"""

from datetime import datetime
from typing import Optional, List, Any, Dict
from enum import Enum

from pydantic import BaseModel, Field


# ─── Enums (per LM-STD-003 Confidence Framework) ──────────────────────

class ConfidenceLevel(str, Enum):
    """LM-STD-003 — Confidence measures how strongly supported a claim is."""
    C5 = "C5"  # Foundational — 🟢
    C4 = "C4"  # Strong — 🔵
    C3 = "C3"  # Moderate — 🟠
    C2 = "C2"  # Emerging — 🟣
    C1 = "C1"  # Exploratory — ⚪


class PipelineStage(str, Enum):
    """The 9 stages of the user journey (PROD-JOURNEY-001)."""
    ENTRY = "entry"
    DISCOVERY = "discovery"
    WORKSHOP = "workshop"
    STRATEGY = "strategy"
    INSIGHT = "insight"
    CREATE = "create"
    JUDGE = "judge"
    SSB = "ssb"
    SKETCH = "sketch"
    PRESENTATION = "presentation"
    COMPLETE = "complete"


class DiscoveryMode(str, Enum):
    """The three Discovery Engine modes (LOG-DISC-001)."""
    EXPERT = "expert"          # score >= 90%
    GUIDED = "guided"          # score 60-89%
    WORKSHOP = "workshop"      # score < 60%
    INSPIRATION = "inspiration"  # extremely thin brief


# ─── User ──────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None


class UserCreate(UserBase):
    password: Optional[str] = None


class User(UserBase):
    id: int
    role: str = "designer"
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Project ───────────────────────────────────────────────────────────

class ProjectCreate(BaseModel):
    """Stage 1 input — PROD-SCREEN-001 Screen 2."""
    company_name: str
    industry: str
    client_brief: str
    client_contact: Optional[str] = None


class ProjectSummary(BaseModel):
    """Dashboard card representation."""
    id: int
    company_name: str
    industry: str
    stage: str  # stored as string; PipelineStage enum values
    brand_confidence_score: float = 0.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Project(ProjectSummary):
    """Full project representation."""
    owner_id: int
    client_brief: str
    client_contact: Optional[str] = None
    brand_confidence_level: str = "unknown"
    discovery_summary: Optional[Dict[str, Any]] = None
    brand_dna: Optional[Dict[str, Any]] = None
    insight_report: Optional[Dict[str, Any]] = None
    concept_families: Optional[List[Dict[str, Any]]] = None
    judge_report: Optional[Dict[str, Any]] = None
    ssb: Optional[Dict[str, Any]] = None
    presentation: Optional[Dict[str, Any]] = None
    workshop_state: Optional[Dict[str, Any]] = None
    workshop_share_token: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Discovery Engine (LOG-DISC-001) ───────────────────────────────────

class BriefAnalysisRequest(BaseModel):
    """Input to the Discovery Engine."""
    project_id: int
    client_brief: str
    company_name: str
    industry: str


class MissingInfo(BaseModel):
    """An identified gap in the brief (Missing Information Detector)."""
    field: str
    impact: str  # high | medium | low — how much it would change the creative direction
    suggested_question: Optional[str] = None


class BriefAnalysisResult(BaseModel):
    """Discovery Engine output — Stage 2 (PROD-JOURNEY-001)."""
    brand_confidence_score: float = Field(ge=0, le=100)
    brand_confidence_level: str  # low | medium | high
    recommended_mode: DiscoveryMode
    discovery_summary: str  # one-paragraph synthesis
    missing_info: List[MissingInfo] = []
    next_action: str  # human-readable guidance


class WorkshopAnswer(BaseModel):
    """A single answer in the Discovery Workshop (LOG-DISC-001)."""
    stage: int  # 1-7
    question_id: str
    answer: Any  # string, list of strings, etc.
    answer_type: str  # text | selection | multi_select | upload


class WorkshopState(BaseModel):
    """The current state of an in-progress Workshop."""
    project_id: int
    current_stage: int = 1  # 1-7
    completed_stages: List[int] = []
    answers: List[WorkshopAnswer] = []
    intent_extractions: List[Dict[str, str]] = []  # {preference, intent}
    estimated_minutes_remaining: float = 15.0


# ─── Strategy Engine (LOG-STRAT-001) ───────────────────────────────────

class BrandDNA(BaseModel):
    """The Strategy Engine's primary output — the strategic foundation."""
    purpose: str
    purpose_confidence: ConfidenceLevel = ConfidenceLevel.C3

    positioning_statement: str
    positioning_confidence: ConfidenceLevel = ConfidenceLevel.C3

    differentiation_primary: str
    differentiation_dimension: str  # product | behaviour | audience | voice | identity
    differentiation_defensibility: ConfidenceLevel = ConfidenceLevel.C3

    audience_configuration: Dict[str, Any]  # concerns, contexts, vocabularies, behaviours
    audience_confidence: ConfidenceLevel = ConfidenceLevel.C3

    personality: str  # character description, not adjective list
    personality_coherence: ConfidenceLevel = ConfidenceLevel.C3

    archetype: Optional[str] = None  # may be None — "no clean archetype" is valid
    archetype_finding: str = "none"  # clean | mixed | none

    emotional_goal: str

    contradictions_flagged: List[Dict[str, str]] = []  # never silently resolved


# ─── Insight Engine (LOG-INSIGHT-001) ──────────────────────────────────

class ClicheEntry(BaseModel):
    symbol: str
    why_cliche: str
    original_meaning: str
    refresh_possible: bool
    alternatives: List[str] = []


class TrendEntry(BaseModel):
    name: str
    classification: str  # timeless | emerging | short_lived | overused
    context_assessment: str
    brand_fit: str  # high | medium | low


class InsightReport(BaseModel):
    industry_analysis: Dict[str, Any]
    competitor_map: List[Dict[str, Any]] = []
    cliche_avoidance: List[ClicheEntry] = []
    opportunities: List[str] = []
    trend_intelligence: List[TrendEntry] = []
    trend_vs_timeless_balance: Dict[str, float]  # {timeless: 0.75, contemporary: 0.25}
    cultural_considerations: List[Dict[str, str]] = []
    confidence_summary: Dict[str, str] = {}  # element -> C-level


# ─── Create Engine (LOG-CREATE-001) ────────────────────────────────────

class SymbolCandidate(BaseModel):
    name: str
    meaning: str
    originality: ConfidenceLevel = ConfidenceLevel.C3
    abstraction_level: str  # literal | abstract | metaphorical
    risk_level: str  # low | medium | high


class ConceptFamilySchema(BaseModel):
    family_label: str  # "A", "B", "C"
    theme: str
    core_meaning_served: str
    symbols: List[SymbolCandidate] = []
    visual_language: Dict[str, str]  # forms, treatment, composition, palette
    why_it_works: str
    pitfalls: str
    creative_council_assessment: Dict[str, str] = {}  # mind -> assessment
    confidence: ConfidenceLevel = ConfidenceLevel.C3
    recommendation_strength: str  # recommended | alternative | exploratory


class CreateEngineResult(BaseModel):
    families: List[ConceptFamilySchema]
    cliches_avoided: List[Dict[str, str]] = []
    client_request_notes: List[Dict[str, str]] = []


# ─── Judge Engine (LOG-JUDGE-001) ──────────────────────────────────────

class JuryScore(BaseModel):
    score: float = Field(ge=0, le=10)
    confidence: ConfidenceLevel
    justification: str


class CreativeCouncilVerdict(BaseModel):
    meaning_mind: str
    simplicity_mind: str
    differentiation_mind: str
    context_mind: str
    memorability_mind: str
    systems_mind: str
    emotion_mind: str
    longevity_mind: str
    boldness_mind: str
    synthesised_verdict: str


class ConceptDNA(BaseModel):
    """The Creative Genome fingerprint for objective comparison."""
    concept_id: str
    emotion: str
    archetype: str
    primary_symbol: str
    secondary_symbol: Optional[str] = None
    shape_language: str
    typography_personality: str
    complexity: str  # low | medium | high
    originality: str
    risk: str
    timelessness_score: float
    strategic_confidence: float


class FamilyJudgeResult(BaseModel):
    family_label: str
    creative_council_verdict: CreativeCouncilVerdict
    jury_scores: Dict[str, JuryScore]  # 10 dimensions
    composite: float
    classification: str  # recommended | develop | reject
    concept_dna: ConceptDNA
    refinement_recommendations: List[str] = []


# ─── SSB (PROD-SSB-001) ────────────────────────────────────────────────

class SketchMission(BaseModel):
    mission_name: str
    core_idea: str
    combine: List[str]
    why_it_works: str
    potential_pitfalls: List[str]
    start_with: str  # specific guidance


class SSB(BaseModel):
    """Strategic Sketch Brief — LogoMind's flagship output (PROD-SSB-001)."""
    project_essence: str
    brand_dna_snapshot: Dict[str, Any]
    creative_north_star: str
    creative_territories: List[Dict[str, Any]]
    opportunities_and_warnings: Dict[str, List[str]]
    creative_council_advice: Dict[str, str]
    sketch_missions: List[SketchMission]


# ─── Sketch Coach (LOG-COACH-001) ──────────────────────────────────────

class SketchUpload(BaseModel):
    project_id: int
    sketch_number: int
    description: Optional[str] = None
    design_intent: Optional[str] = None
    linked_concept_family: Optional[str] = None
    image_url: Optional[str] = None


class CoachFeedback(BaseModel):
    """Sketch Coach output — conversational, never prescriptive."""
    assessment: str
    suggestions: List[str]  # framed as questions where possible
    pitfalls_to_watch: List[str] = []
    confidence: ConfidenceLevel = ConfidenceLevel.C3


# ─── Generic ───────────────────────────────────────────────────────────

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class StageAdvanceRequest(BaseModel):
    """Request to advance the project to the next pipeline stage."""
    confirm: bool = True


class DecisionLogEntry(BaseModel):
    decision: str
    reason: Optional[str] = None
    stage: Optional[str] = None
    made_by: str = "system"
