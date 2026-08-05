"""
LogoMind API Routes.

The complete API surface for the LOGOS pipeline. Each route maps to
a stage of the user journey (PROD-JOURNEY-001) and calls the
corresponding engine service.
"""

import secrets
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User as UserModel, Project as ProjectModel, Sketch as SketchModel, DecisionLog as DecisionLogModel, ConceptFamily as ConceptFamilyModel
from ..schemas import (
    ProjectCreate, Project, ProjectSummary,
    BriefAnalysisResult, BrandDNA, InsightReport,
    CreateEngineResult, FamilyJudgeResult, SSB, CoachFeedback,
    WorkshopState, WorkshopAnswer,
    SketchUpload, SketchOut, DecisionLogEntry,
    ConceptPromptResult,
)
from ..services.discovery_engine import analyse_brief, extract_intent, synthesize_brief
from ..services.engines import (
    build_brand_dna, generate_insight, generate_concept_families,
    judge_family, compose_ssb, critique_sketch, build_presentation,
)
from ..services.concept_engine import compose_concept_prompt


router = APIRouter()


# ─── Helper ────────────────────────────────────────────────────────────

def _get_project(db: Session, project_id: int) -> ProjectModel:
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return project


def _log_decision(db: Session, project_id: int, decision: str, reason: str = None, stage: str = None):
    entry = DecisionLogModel(project_id=project_id, decision=decision, reason=reason, stage=stage)
    db.add(entry)
    db.commit()


# ─── Stage error handling ─────────────────────────────────────────────
#
# The LOGOS engines call live AI models that can transiently fail (timeouts,
# 5xx, rate limits) or emit output the schema can't validate. Rather than
# surfacing a bare 500, stage endpoints are wrapped with @with_stage_error
# so the frontend receives a structured, human-readable error it can present
# with a Retry action and an honest explanation. HTTP 503 (Service
# Unavailable) is semantically correct for a transient upstream-model failure
# and tells the client the request is safe to retry.

# Friendly per-stage names for user-facing copy.
_STAGE_NAMES = {
    "strategy": "Strategy",
    "insight": "Insight",
    "create": "Concept Families",
    "judge": "Judge",
    "concept_prompt": "Concept Prompt",
    "ssb": "Strategic Sketch Brief",
    "sketch": "Sketch Coach",
    "presentation": "Presentation",
}

# Typical wall-clock ranges (seconds) for each stage against a real model,
# so the UI can show an honest estimate instead of an indeterminate spinner.
_STAGE_ESTIMATES = {
    "strategy": (20, 90),
    "insight": (30, 120),
    "create": (60, 240),
    "judge": (180, 540),
    "concept_prompt": (180, 720),
    "ssb": (30, 120),
    "sketch": (20, 60),
    "presentation": (30, 90),
}


def with_stage_error(stage: str):
    """Decorator: catch engine/model failures and return a structured StageError.

    `stage` is the pipeline stage id (e.g. "insight"). Validation/guard
    HTTPExceptions (4xx) pass through unchanged; only unexpected engine
    failures become a 503 StageError.
    """
    import functools
    from pydantic import ValidationError

    def decorator(fn):
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs):
            try:
                return await fn(*args, **kwargs)
            except HTTPException:
                raise  # guard failures (missing prerequisites etc.) pass through
            except ValidationError as e:
                raise HTTPException(
                    status_code=503,
                    detail={
                        "stage": stage,
                        "stage_name": _STAGE_NAMES.get(stage, stage),
                        "kind": "validation",
                        "detail": (
                            f"The {_STAGE_NAMES.get(stage, stage)} engine produced a response "
                            f"we couldn't interpret. This is usually a momentary model hiccup — "
                            f"please retry. (Field: {e.errors()[0].get('loc') if e.errors() else '?'})"
                        ),
                        "retryable": True,
                        "estimate": _STAGE_ESTIMATES.get(stage),
                    },
                )
            except Exception as e:
                # Network/transient model errors (timeout, 5xx, rate limit)
                # already retry inside OpenAIProvider; reaching here means those
                # retries were exhausted. Treat as retryable — a later attempt
                # often succeeds.
                msg = str(e) or type(e).__name__
                raise HTTPException(
                    status_code=503,
                    detail={
                        "stage": stage,
                        "stage_name": _STAGE_NAMES.get(stage, stage),
                        "kind": "transient",
                        "detail": (
                            f"The {_STAGE_NAMES.get(stage, stage)} engine couldn't reach the "
                            f"model after several attempts. This is typically a temporary load "
                            f"or timeout issue — please retry in a moment."
                        ),
                        "retryable": True,
                        "technical": msg[:300],
                        "estimate": _STAGE_ESTIMATES.get(stage),
                    },
                )

        return wrapper

    return decorator



# ═══════════════════════════════════════════════════════════════════════
# PROJECTS
# ═══════════════════════════════════════════════════════════════════════

@router.get("/projects", response_model=List[ProjectSummary])
def list_projects(db: Session = Depends(get_db)):
    """Dashboard — list all projects (Stage 1 entry)."""
    return db.query(ProjectModel).order_by(ProjectModel.updated_at.desc()).all()


@router.post("/projects", response_model=Project, status_code=201)
def create_project(project_in: ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project (Stage 1 — PROD-SCREEN-001 Screen 2)."""
    # In production, get the authenticated user. For now, use user 1 if exists.
    user = db.query(UserModel).first()
    if not user:
        user = UserModel(email="demo@logomind.ai", name="Demo User")
        db.add(user)
        db.commit()
        db.refresh(user)

    project = ProjectModel(
        owner_id=user.id,
        company_name=project_in.company_name,
        industry=project_in.industry,
        client_brief=project_in.client_brief,
        client_contact=project_in.client_contact,
        stage="entry",
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.get("/projects/{project_id}", response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Get full project details."""
    return _get_project(db, project_id)


@router.delete("/projects/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = _get_project(db, project_id)
    db.delete(project)
    db.commit()


# ═══════════════════════════════════════════════════════════════════════
# STAGE 2: DISCOVERY ENGINE (LOG-DISC-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/analyse", response_model=BriefAnalysisResult)
async def analyse_project_brief(project_id: int, db: Session = Depends(get_db)):
    """Run the Discovery Engine on the project's brief (Stage 2)."""
    project = _get_project(db, project_id)

    result = await analyse_brief(
        company_name=project.company_name,
        industry=project.industry,
        client_brief=project.client_brief,
    )

    # Persist results
    project.brand_confidence_score = result.brand_confidence_score
    project.brand_confidence_level = result.brand_confidence_level
    project.discovery_summary = result.model_dump()
    project.stage = "discovery"
    db.commit()

    _log_decision(db, project_id, f"Brief analysed: score {result.brand_confidence_score}%", stage="discovery")
    return result


# ═══════════════════════════════════════════════════════════════════════
# STAGE 3: DISCOVERY WORKSHOP (LOG-DISC-001 Workshop Mode)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/workshop/share", response_model=dict)
def generate_workshop_link(project_id: int, db: Session = Depends(get_db)):
    """Generate a shareable link for the client to take the Workshop."""
    project = _get_project(db, project_id)
    token = secrets.token_urlsafe(16)
    project.workshop_share_token = token
    project.stage = "workshop"
    db.commit()
    return {"share_token": token, "url": f"/workshop/{token}"}


@router.get("/workshop/{token}", response_model=Project)
def get_workshop_by_token(token: str, db: Session = Depends(get_db)):
    """Client accesses the Workshop via share token."""
    project = db.query(ProjectModel).filter(ProjectModel.workshop_share_token == token).first()
    if not project:
        raise HTTPException(status_code=404, detail="Workshop link invalid or expired")
    return project


@router.post("/projects/{project_id}/workshop/answer", response_model=WorkshopState)
def submit_workshop_answer(project_id: int, answer: WorkshopAnswer, db: Session = Depends(get_db)):
    """Submit one Workshop answer (Stage 3)."""
    project = _get_project(db, project_id)

    state = WorkshopState(**(project.workshop_state or {"project_id": project_id}))
    state.answers.append(answer)
    if answer.stage not in state.completed_stages and answer.answer:
        state.completed_stages.append(answer.stage)

    # Advance stage
    if state.current_stage < 7:
        state.current_stage = max(state.current_stage + 1, answer.stage + 1)
        state.estimated_minutes_remaining = max(0, 15 - (state.current_stage - 1) * 2)

    project.workshop_state = state.model_dump()
    db.commit()
    return state


@router.post("/projects/{project_id}/workshop/complete", response_model=Project)
async def complete_workshop(project_id: int, db: Session = Depends(get_db)):
    """Finalise the Workshop; recalculate Brand Confidence and proceed to Strategy."""
    project = _get_project(db, project_id)

    # Synthesize the original brief + workshop answers into a richer, coherent
    # brief (workshop answers are often terse; weaving them in is what actually
    # raises a real, quality-based Brand Confidence score), then re-score it.
    state = project.workshop_state or {}
    answers = state.get("answers", [])

    enriched_brief = await synthesize_brief(
        company_name=project.company_name,
        industry=project.industry,
        client_brief=project.client_brief,
        workshop_answers=answers,
    )

    result = await analyse_brief(
        company_name=project.company_name,
        industry=project.industry,
        client_brief=enriched_brief,
    )
    project.brand_confidence_score = result.brand_confidence_score
    project.brand_confidence_level = result.brand_confidence_level
    project.discovery_summary = result.model_dump()
    project.stage = "discovery"  # ready for strategy
    db.commit()
    return project


# ═══════════════════════════════════════════════════════════════════════
# STAGE 4: STRATEGY ENGINE (LOG-STRAT-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/strategy", response_model=BrandDNA)
@with_stage_error("strategy")
async def run_strategy(project_id: int, db: Session = Depends(get_db)):
    """Run the Strategy Engine — produces Brand DNA (Stage 4)."""
    project = _get_project(db, project_id)

    if project.brand_confidence_score < 70:
        raise HTTPException(
            status_code=400,
            detail="Brand Confidence Score below 70%. Run Discovery Workshop first (DR-1)."
        )

    result = await build_brand_dna(discovery_summary=project.discovery_summary)
    project.brand_dna = result.model_dump()
    project.stage = "strategy"
    db.commit()

    _log_decision(db, project_id, "Brand DNA generated", stage="strategy")
    return result


# ═══════════════════════════════════════════════════════════════════════
# STAGE 5: INSIGHT ENGINE (LOG-INSIGHT-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/insight", response_model=InsightReport)
@with_stage_error("insight")
async def run_insight(project_id: int, db: Session = Depends(get_db)):
    """Run the Insight Engine — industry research + trends (Stage 5)."""
    project = _get_project(db, project_id)
    if not project.brand_dna:
        raise HTTPException(status_code=400, detail="Brand DNA required. Run Strategy first.")

    result = await generate_insight(
        industry=project.industry,
        brand_dna=project.brand_dna,
    )
    project.insight_report = result.model_dump()
    project.stage = "insight"
    db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════════
# STAGE 6: CREATE ENGINE (LOG-CREATE-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/create", response_model=CreateEngineResult)
@with_stage_error("create")
async def run_create(project_id: int, db: Session = Depends(get_db)):
    """Run the Create Engine — produces Concept Families (Stage 6)."""
    project = _get_project(db, project_id)
    if not project.brand_dna or not project.insight_report:
        raise HTTPException(status_code=400, detail="Brand DNA and Insight required.")

    result = await generate_concept_families(
        brand_dna=project.brand_dna,
        insight_report=project.insight_report,
    )

    # Store families
    project.concept_families = [f.model_dump() for f in result.families]
    project.stage = "create"

    # Persist as separate rows for queryability
    for family_data in project.concept_families:
        cf = ConceptFamilyModel(
            project_id=project_id,
            family_label=family_data.get("family_label", "?"),
            theme=family_data.get("theme", ""),
            core_meaning_served=family_data.get("core_meaning_served", ""),
            family_data=family_data,
        )
        db.add(cf)

    db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════════
# STAGE 7: JUDGE ENGINE (LOG-JUDGE-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/judge", response_model=List[FamilyJudgeResult])
@with_stage_error("judge")
async def run_judge(project_id: int, db: Session = Depends(get_db)):
    """Run the Judge Engine on all Concept Families (Stage 7)."""
    project = _get_project(db, project_id)
    if not project.concept_families:
        raise HTTPException(status_code=400, detail="Concept Families required. Run Create first.")

    results = []
    for family in project.concept_families:
        result = await judge_family(
            family=family,
            brand_dna=project.brand_dna,
            insight_report=project.insight_report,
        )
        results.append(result)

        # Update the ConceptFamily row
        cf = db.query(ConceptFamilyModel).filter(
            ConceptFamilyModel.project_id == project_id,
            ConceptFamilyModel.family_label == family.get("family_label"),
        ).first()
        if cf:
            cf.composite_score = result.composite
            cf.classification = result.classification
            cf.judge_detail = {k: v.model_dump() for k, v in result.jury_scores.items()}
            cf.concept_dna = result.concept_dna.model_dump()

    project.judge_report = [r.model_dump() for r in results]
    project.stage = "judge"
    db.commit()
    return results


@router.post("/projects/{project_id}/select-family/{family_label}")
def select_family(project_id: int, family_label: str, db: Session = Depends(get_db)):
    """Designer selects a Concept Family to develop."""
    project = _get_project(db, project_id)

    cf = db.query(ConceptFamilyModel).filter(
        ConceptFamilyModel.project_id == project_id,
        ConceptFamilyModel.family_label == family_label,
    ).first()
    if not cf:
        raise HTTPException(status_code=404, detail=f"Family {family_label} not found")

    # Clear previous selection
    db.query(ConceptFamilyModel).filter(ConceptFamilyModel.project_id == project_id).update({ConceptFamilyModel.is_selected: False})
    cf.is_selected = True
    db.commit()

    _log_decision(db, project_id, f"Selected Family {family_label}", stage="judge")
    return {"selected": family_label}


# ═══════════════════════════════════════════════════════════════════════
# STAGE: CONCEPT PROMPT ENGINE (LOG-CP-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/concept-prompts", response_model=List[ConceptPromptResult])
@with_stage_error("concept_prompt")
async def compose_project_concept_prompts(project_id: int, db: Session = Depends(get_db)):
    """Run the Concept Prompt Engine on all Concept Families (Stage: concept_prompt).

    Produces an executable concept (prompt variants + model adaptations +
    wireframe spec + rationale) per family. Generates no images; makes no
    creative decision (FD-015).
    """
    project = _get_project(db, project_id)
    if not project.concept_families or not project.judge_report:
        raise HTTPException(
            status_code=400,
            detail="Concept Families and Judge evaluation required first.",
        )

    # Pair each family with its own judge result by label so the engine can
    # honour per-family evaluation and refinements.
    judge_by_label = {j.get("family_label"): j for j in project.judge_report}

    results = []
    for family in project.concept_families:
        result = await compose_concept_prompt(
            family=family,
            judge_result=judge_by_label.get(family.get("family_label"), {}),
            brand_dna=project.brand_dna,
            insight_report=project.insight_report,
        )
        results.append(result)

    project.concept_prompts = [r.model_dump() for r in results]
    project.stage = "concept_prompt"

    db.commit()
    _log_decision(db, project_id, "Composed Concept Prompts for all families", stage="concept_prompt")
    return results


# ═══════════════════════════════════════════════════════════════════════
# STAGE 8: SSB + SKETCH (PROD-SSB-001, LOG-COACH-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/ssb", response_model=SSB)
@with_stage_error("ssb")
async def compose_project_ssb(project_id: int, db: Session = Depends(get_db)):
    """Compose the Strategic Sketch Brief (Stage 8)."""
    project = _get_project(db, project_id)
    if not project.judge_report:
        raise HTTPException(status_code=400, detail="Judge evaluation required first.")

    # Read the designer's family selection so the SSB headlines the chosen
    # territory. Falls back to auto-selection (highest composite) inside
    # compose_ssb if nothing was explicitly selected.
    selected = db.query(ConceptFamilyModel).filter(
        ConceptFamilyModel.project_id == project_id,
        ConceptFamilyModel.is_selected == True,  # noqa: E712
    ).first()
    selected_label = selected.family_label if selected else None

    result = await compose_ssb(
        brand_dna=project.brand_dna,
        insight_report=project.insight_report,
        concept_families=project.concept_families,
        judge_reports=project.judge_report,
        company_name=project.company_name,
        selected_family_label=selected_label,
    )
    if selected is None and result.selected_territory:
        _log_decision(
            db, project_id,
            f"SSB auto-selected Family {result.selected_territory.family_label} (no explicit selection)",
            stage="ssb",
        )
    project.ssb = result.model_dump()
    project.stage = "ssb"
    db.commit()
    return result


@router.post("/projects/{project_id}/sketches", response_model=CoachFeedback)
@with_stage_error("sketch")
async def upload_sketch(project_id: int, sketch: SketchUpload, db: Session = Depends(get_db)):
    """Upload a sketch and get Sketch Coach feedback (Stage 8 iteration)."""
    project = _get_project(db, project_id)

    # Count existing sketches for numbering
    existing = db.query(SketchModel).filter(SketchModel.project_id == project_id).count()
    sketch_number = existing + 1

    # Get Sketch Coach feedback
    linked_family = next(
        (f for f in (project.concept_families or []) if f.get("family_label") == sketch.linked_concept_family),
        {}
    )
    feedback = await critique_sketch(
        sketch_description=sketch.description or "",
        design_intent=sketch.design_intent or "",
        linked_family=linked_family,
        brand_dna=project.brand_dna or {},
    )

    # Persist the sketch
    sketch_record = SketchModel(
        project_id=project_id,
        sketch_number=sketch_number,
        description=sketch.description,
        design_intent=sketch.design_intent,
        linked_concept_family=sketch.linked_concept_family,
        image_url=sketch.image_url,
        coach_feedback=feedback.model_dump(),
        coach_confidence=feedback.confidence.value,
    )
    db.add(sketch_record)
    project.stage = "sketch"
    db.commit()

    return feedback


@router.get("/projects/{project_id}/sketches", response_model=List[SketchOut])
def list_sketches(project_id: int, db: Session = Depends(get_db)):
    """List a project's sketches and persisted coach feedback (Stage 8 iteration)."""
    _get_project(db, project_id)  # 404 if the project does not exist
    sketches = (
        db.query(SketchModel)
        .filter(SketchModel.project_id == project_id)
        .order_by(SketchModel.sketch_number)
        .all()
    )
    return sketches


# ═══════════════════════════════════════════════════════════════════════
# STAGE 9: PRESENTATION BUILDER (LOG-PRESENT-001)
# ═══════════════════════════════════════════════════════════════════════

@router.post("/projects/{project_id}/presentation")
@with_stage_error("presentation")
async def build_project_presentation(project_id: int, db: Session = Depends(get_db)):
    """Build the client presentation (Stage 9)."""
    project = _get_project(db, project_id)
    if not project.ssb:
        raise HTTPException(status_code=400, detail="SSB required first.")

    result = await build_presentation(
        brand_dna=project.brand_dna,
        concept_families=project.concept_families,
        judge_reports=project.judge_report,
        ssb=project.ssb,
        company_name=project.company_name,
    )
    project.presentation = result
    project.stage = "presentation"
    db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════════
# DECISION LOG
# ═══════════════════════════════════════════════════════════════════════

@router.get("/projects/{project_id}/decisions", response_model=List[DecisionLogEntry])
def get_decision_log(project_id: int, db: Session = Depends(get_db)):
    """Retrieve the project's decision log."""
    entries = db.query(DecisionLogModel).filter(DecisionLogModel.project_id == project_id).all()
    return [DecisionLogEntry(decision=e.decision, reason=e.reason, stage=e.stage, made_by=e.made_by) for e in entries]


@router.post("/projects/{project_id}/decisions", status_code=201)
def add_decision(project_id: int, entry: DecisionLogEntry, db: Session = Depends(get_db)):
    """Manually add a decision to the log."""
    _log_decision(db, project_id, entry.decision, entry.reason, entry.stage)
    return {"status": "recorded"}
