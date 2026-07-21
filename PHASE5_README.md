# LogoMind — Phase 5: Technical Build

> **Reason. Create. Refine.**

This directory contains the **runnable software** implementing the LOGOS pipeline — LogoMind's strategic design intelligence platform for logo designers.

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) OpenAI API key for real AI responses

### 1. Backend (FastAPI)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment config (defaults to mock AI — no API key needed)
cp .env.example .env

# Run the server
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

### 2. Frontend (Next.js)

```bash
cd frontend
npm install

# Copy environment config
cp .env.example .env.local

# Run the dev server
npm run dev
```

Frontend runs at `http://localhost:3000`.

### 3. Use LogoMind

1. Open `http://localhost:3000`
2. Click "+ New Project"
3. Enter a company name, industry, and brief (any completeness level)
4. Walk through the pipeline: Discovery → Strategy → Insight → Create → Judge → SSB → Sketch → Presentation

## Using Real AI (instead of mock)

In `backend/.env`:
```bash
LOGOMIND_AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-key-here
LOGOMIND_MODEL=gpt-4o
```

Without a key, the backend uses a deterministic mock that returns sensible placeholder responses — letting you experience the full pipeline flow without cost.

## Architecture

```
backend/
  app/
    __init__.py          # SQLAlchemy models (Project, Sketch, ConceptFamily, etc.)
    main.py              # FastAPI app + CORS + lifespan
    database.py          # Engine + session + init_db()
    schemas/__init__.py  # Pydantic API contracts (all pipeline stages)
    routers/__init__.py  # API routes (one per pipeline stage)
    services/
      ai_orchestrator.py # Model-independent AI provider (Mock / OpenAI)
      discovery_engine.py# LOG-DISC-001 implementation
      engines.py         # Strategy, Insight, Create, Judge, SSB, Coach, Present
    prompts/             # (future: externalised system prompts)

frontend/
  src/
    app/
      layout.tsx         # Root layout with header/footer
      page.tsx           # Dashboard (Screen 1)
      projects/new/      # New Project (Screen 2)
      projects/[id]/     # Project workspace (Screens 3-8, stage-routed)
    components/
      WorkshopView.tsx   # Discovery Workshop (Screen 3)
      StrategyView.tsx   # Brand DNA (Screen 4)
      InsightView.tsx    # Insight Report (Screen 5)
      ConceptFamiliesView.tsx  # Create + Judge (Screens 6-7)
      SSBView.tsx        # SSB + Sketch (Screen 7)
      PresentationView.tsx     # Presentation (Screen 8)
    lib/
      api.ts             # API client (one function per pipeline stage)
```

## The Pipeline

```
Client Brief → Discovery → Strategy → Insight → Create → Judge → SSB → Coach → Presentation
```

Each stage:
1. Calls the corresponding LOGOS engine service
2. Persists the result to the Project record
3. Advances the project's `stage` field
4. Surfaces the result in the frontend

## Key Design Decisions

| Decision | Why |
|----------|-----|
| **Mock AI provider** | Full pipeline testable without API key or cost |
| **SQLite default** | Zero-config dev; switch to PostgreSQL for production |
| **Model-independent orchestration** | LogoMind never depends on a single AI model (Company Decision #001) |
| **JSON columns for pipeline outputs** | Each stage's output is a document, not normalised relational data |
| **Stage-routed frontend** | One project page routes to the right component based on `stage` |
| **Confidence levels everywhere** | LM-STD-003 — never fake certainty |

## Status

**Phase 5 v1.0** — complete codebase with:
- ✅ All 9 pipeline stages implemented (backend)
- ✅ All 8 frontend screens implemented
- ✅ Mock AI provider (deterministic, no API key needed)
- ✅ OpenAI provider (production-ready, requires key)
- ✅ Full API surface documented at `/docs`

**Not yet implemented (deferred):**
- ⬜ Authentication (currently single-demo-user)
- ⬜ File upload (sketches — currently description-based)
- ⬜ Alembic migrations (using auto-create-all for dev)
- ⬜ Production deployment scripts
- ⬜ Test suite
- ⬜ Symbol Intelligence volume integration (Create Engine uses general knowledge until built)

## Connection to the Knowledge Base

This software *implements* the specifications in the parent repository:
- `01_Foundation/` — the Charter, Constitution, and Philosophy govern every decision
- `03_LKOS_Standards/` — LM-STD-001..006 are embedded in the schemas and models
- `04_LOGOS_Engines/` — each service file maps 1:1 to an engine spec
- `05_RS_LICs/` — the LICs inform the system prompts and evaluation criteria
- `07_Product/` — the screens map 1:1 to PROD-SCREEN-001

---

*LogoMind will never make a creative decision for the designer.*
