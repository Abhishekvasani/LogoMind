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
    CLIENT_FIT = "client_fit"
    CONCEPT_PROMPT = "concept_prompt"
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


class SketchOut(BaseModel):
    """A persisted sketch and its coach feedback (Stage 8 iteration).

    Defined before Project so Project can reference it; it only depends on
    the top-level imports (no other schema types).
    """
    id: int
    sketch_number: int
    description: Optional[str] = None
    design_intent: Optional[str] = None
    linked_concept_family: Optional[str] = None
    image_url: Optional[str] = None
    coach_feedback: Optional[Dict[str, Any]] = None
    coach_confidence: Optional[str] = None
    revision_status: str = "draft"
    created_at: datetime

    class Config:
        from_attributes = True


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
    judge_report: Optional[List[Dict[str, Any]]] = None
    concept_prompts: Optional[List[Dict[str, Any]]] = None
    ssb: Optional[Dict[str, Any]] = None
    presentation: Optional[Dict[str, Any]] = None
    client_persona: Optional[Dict[str, Any]] = None      # Client Preference Predictor — persona
    appeal_report: Optional[Dict[str, Any]] = None       # Client Preference Predictor — ranked appeal
    contest_brief: Optional[Dict[str, Any]] = None       # Decoded contest brief (Stage 3)
    contest_feedback: Optional[List[Dict[str, Any]]] = None  # Revealed in-contest preferences (Stage 4)
    workshop_state: Optional[Dict[str, Any]] = None
    workshop_share_token: Optional[str] = None
    sketches: List[SketchOut] = []

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


class IntentExtractionRequest(BaseModel):
    """Input to the Intent Extraction sub-engine (LOG-DISC-001)."""
    preference: str  # a client's stated preference, e.g. "I want blue"


class IntentExtraction(BaseModel):
    """Decoded strategic intent behind a stated preference.

    "I want blue" -> "I want trust"; "I want a shield" -> "I want security".
    """
    preference: str
    intent: str
    reasoning: str


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


# ─── Concept Prompt Engine (LOG-CP-001) ────────────────────────────────

class PromptVariant(BaseModel):
    """One of the four model-agnostic concept prompts for a family.

    Styles are a fixed set (PROD-CP-001 §4): minimal, detailed,
    typographic-led, symbolic. The engine does NOT rank variants — they are
    parallel starting points the designer chooses between.
    """
    style: str  # minimal | detailed | typographic-led | symbolic
    prompt: str  # complete natural-language concept prompt
    intent: str  # one line: what this variant emphasises


class ModelAdaptation(BaseModel):
    """How to tune the concept prompt for one image-model family.

    Model behaviour lives here, NOT in the variants — variants stay
    model-agnostic (PROD-CP-001 §6).
    """
    model_family: str  # midjourney | ideogram | stable-diffusion | recraft | general
    notes: str  # how to tune for this family
    example_suffix: str  # concrete copy-pasteable tunable, e.g. "--ar 1:1 --style raw"


class WireframeElement(BaseModel):
    """One element of a composition wireframe spec.

    Geometry/position/size are from a closed vocabulary (PROD-CP-001 §5.2)
    so the spec is deterministically renderable to SVG — never freeform
    imagery (LOG-CP-001 §3).
    """
    kind: str  # symbol | wordmark | tagline | container | negative-space
    geometry: str  # circle | hexagon | rectangle | monogram | baseline-bar | custom
    position: str  # center | left-of-text | above | below | integrated
    relative_size: str  # dominant | balanced | accent | small
    notes: str = ""


class WireframeSpec(BaseModel):
    """The composition blueprint — structured data, rendered to SVG.

    The LLM describes layout; it never draws pixels (LOG-CP-001 §3).
    """
    orientation: str  # horizontal | stacked | lockup | emblem
    balance: str  # e.g. "60/40 symbol-to-text" | "centered"
    alignment: str  # center | left | baseline-aligned
    safe_margin: str  # e.g. "12% padding"
    elements: List[WireframeElement] = []
    favicon_note: str  # how the composition degrades at favicon size


class ConceptPromptResult(BaseModel):
    """Concept Prompt Engine output for ONE Concept Family (LOG-CP-001)."""
    family_label: str
    core_concept: str  # one-sentence distillation of the family as a visual
    variants: List[PromptVariant]  # exactly four
    model_adaptations: List[ModelAdaptation]  # five model families
    wireframe: WireframeSpec
    rationale: str  # trace to Brand DNA + visual_language
    cliches_avoided: List[str] = []
    confidence: ConfidenceLevel = ConfidenceLevel.C3



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
    archetype: Optional[str] = None  # may be None — "no clean archetype" is valid
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


# ─── Client Preference Predictor (Client Fit) ──────────────────────────
#
# LogoMind's answer to "what will THIS client love?" — a reasoning-based
# preference model, NOT a literal neural/brain-response measurement. It builds
# a persona of the specific decision-maker from their brief, then predicts how
# strongly each Concept Family will resonate with THAT persona and ranks them.
# Honesty is structural: every prediction carries explicit confidence and a
# caveat about how much signal a brief alone provides.

class ClientPersona(BaseModel):
    """A model of THIS client's likely taste, inferred from the brief + context.

    Predicts aesthetic lean and boldness tolerance so downstream stages can aim
    at the client's taste rather than a generic 'good design' average.
    """
    one_line: str  # "A pragmatic fintech founder who prizes clarity over cleverness"
    archetype: str  # e.g. "The Pragmatist" | "The Bold Disruptor" | "The Heritage Guardian"
    taste_signals: List[str]  # concrete signals observed in the brief
    decoded_intents: List[Dict[str, str]] = []  # [{stated, intent}] e.g. "blue" -> "trust"
    aesthetic_lean: str  # minimal | bold | elegant | playful | technical | heritage | organic
    boldness_tolerance: str  # conservative | moderate | adventurous
    must_haves: List[str] = []
    must_avoids: List[str] = []
    references: List[str] = []
    confidence: ConfidenceLevel = ConfidenceLevel.C3


class FamilyAppeal(BaseModel):
    """One Concept Family scored for predicted resonance with THIS client."""
    family_label: str
    client_appeal_score: float = Field(ge=0, le=100)  # predicted resonance for THIS client
    rank: int  # 1 = strongest predicted
    predicted_response: str  # one vivid line in the client's emotional vocabulary
    appeal_drivers: List[str]  # why it resonates with THIS client (persona-relative)
    appeal_risks: List[str]  # why it might miss for THIS client
    confidence: ConfidenceLevel = ConfidenceLevel.C3


class AppealReport(BaseModel):
    """Client Preference Predictor output — ranks families by predicted client appeal.

    The decision screen: which direction is the safest bet to win THIS client,
    and why. Designed to differ from the Judge (design excellence) — a family
    can score high with the jury but lower with a conservative client, and the
    predictor says so explicitly.
    """
    persona: ClientPersona
    family_appeal: List[FamilyAppeal]  # ranked by client_appeal_score desc
    recommended_family: str  # family_label of rank 1
    reasoning: str  # 2-3 sentences: why the top family is the safest bet to win
    caveat: str  # honest limit, e.g. "brief-only; refine with contest feedback"
    confidence: ConfidenceLevel = ConfidenceLevel.C3


# ─── Contest Intelligence (Stage 3 + 4) ─────────────────────────────────
#
# Two contest-specific inputs that sharpen the Client Preference Predictor:
# (3) a decoded contest brief — messy freelancer.com text -> structured signals,
# and (4) revealed preferences — what the client actually liked/disliked mid-contest.

class ContestBrief(BaseModel):
    """A contest brief decoded into structured, usable signals.

    Freelancer.com briefs are semi-structured free text. This normalises them so
    the persona engine gets clean must-haves/avoids/colors instead of prose.
    """
    company_name: Optional[str] = None
    industry: Optional[str] = None
    tagline: Optional[str] = None
    dos: List[str] = []
    donts: List[str] = []
    colors_preferred: List[str] = []
    colors_avoided: List[str] = []
    style_keywords: List[str] = []
    must_include: List[str] = []
    must_avoid: List[str] = []
    references: List[str] = []
    decoded_summary: str  # readable synthesis of the contest intent
    confidence: ConfidenceLevel = ConfidenceLevel.C3


class ContestBriefDecodeRequest(BaseModel):
    """Raw contest text to decode (Stage 3)."""
    raw_text: str


class ContestSignal(BaseModel):
    """One observed in-contest preference signal (Stage 4)."""
    kind: str  # liked | disliked | comment
    trait: str  # what was liked/disliked/commented, e.g. "minimal layouts"
    note: Optional[str] = None


class ContestRefineRequest(BaseModel):
    """Add revealed-preference signals and re-run the prediction (Stage 4)."""
    signals: List[ContestSignal]


# ─── SSB (PROD-SSB-001) ────────────────────────────────────────────────

class SketchMission(BaseModel):
    mission_name: str
    core_idea: str
    combine: List[str]
    why_it_works: str
    potential_pitfalls: List[str]
    start_with: str  # specific guidance


class SSBTerritory(BaseModel):
    """A Creative Territory in the SSB — the chosen family plus its judge fingerprint.

    Carries the rich judge/visual data the SSB previously discarded. All new
    fields are optional so older SSB JSON (and the mock) still validate.
    """
    family_label: str
    theme: str
    recommendation: str = "alternative"  # recommended | alternative | exploratory
    core_meaning_served: Optional[str] = None
    why_it_works: Optional[str] = None
    pitfalls: Optional[str] = None
    # Judge fingerprint carried forward (from FamilyJudgeResult):
    composite: Optional[float] = None
    classification: Optional[str] = None  # recommended | develop | reject
    # Create-stage richness:
    visual_language: Dict[str, str] = {}      # forms, treatment, composition, palette
    symbols: List[Dict[str, Any]] = []        # [{name, meaning, originality, abstraction_level, risk_level}]
    concept_dna: Optional[Dict[str, Any]] = None
    refinement_recommendations: List[str] = []


class CouncilAdvice(BaseModel):
    """The Creative Council's advice for the SSB.

    Mirrors CreativeCouncilVerdict. Fields optional so older dict-shaped advice
    still validates.
    """
    meaning_mind: str = ""
    simplicity_mind: str = ""
    differentiation_mind: str = ""
    context_mind: str = ""
    memorability_mind: str = ""
    systems_mind: str = ""
    emotion_mind: str = ""
    longevity_mind: str = ""
    boldness_mind: str = ""
    synthesised_verdict: str = ""


class SSB(BaseModel):
    """Strategic Sketch Brief — LogoMind's flagship output (PROD-SSB-001)."""
    project_essence: str
    brand_dna_snapshot: Dict[str, Any]
    creative_north_star: str
    creative_territories: List[Dict[str, Any]]
    opportunities_and_warnings: Dict[str, List[str]]
    creative_council_advice: Dict[str, str]
    sketch_missions: List[SketchMission]
    # Rich additions (all optional — backward compatible with older SSB JSON):
    selected_territory: Optional[SSBTerritory] = None
    council_advice: Optional[CouncilAdvice] = None


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
