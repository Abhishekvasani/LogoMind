---
doc_id: LM-HANDOVER-001
title: LogoMind Complete Handover Document
version: 1.0
status: Living Document
last_reviewed: 2026-08-18
purpose: Single source of truth for resuming work on LogoMind with zero prior context
---

# LogoMind — Complete Handover Document

> **Read this file top to bottom and you know everything needed to continue working on LogoMind.** It covers the product, architecture, knowledge system, live deployment, decisions made (and why), known gotchas, and the exact commands for every workflow.

---

## 1. What LogoMind Is

**LogoMind is a Strategic Design Intelligence platform for logo designers.** It transforms an incomplete client brief into a complete creative strategy (the *Strategic Sketch Brief*) using a pipeline of LLM engines grounded in a curated, proprietary knowledge corpus (LICs).

Core promises (non-negotiable product philosophy):
- **"LogoMind will never make a creative decision for the designer."** The designer is sovereign; engines reason, suggest, and critique.
- **Intellectual honesty everywhere** — every output carries a confidence level (C1–C5 per LM-STD-003); nothing fakes certainty.
- Motto: **Reason. Create. Refine.**

The founder is Abhishek (GitHub `Abhishekvasani`). The repo lives at `https://github.com/Abhishekvasani/LogoMind` (public, default branch `main`).

---

## 2. The Product in One Picture — 13-Stage Pipeline

```
entry → discovery → workshop → strategy → insight → create → judge
      → client_fit → concept_prompt → ssb → sketch → presentation → complete
```

| Stage | What happens | Engine (spec) |
|---|---|---|
| entry | Designer submits client brief | — |
| discovery | Brief analysed; Brand Confidence Score 0–100 | Discovery (LOG-DISC-001) |
| workshop | If score < 70: question flow enriches the brief | Discovery (Workshop mode) |
| strategy | Brand DNA synthesised (purpose, positioning, archetype…) | Strategy (LOG-STRAT-001) |
| insight | Category conventions, cliché map, trend taxonomy | Insight (LOG-INSIGHT-001) |
| create | 3–5 Concept Families (strategic territories, not ideas) | Create (LOG-CREATE-001) |
| judge | 10-dimension design jury + Creative Council verdict | Judge (LOG-JUDGE-001) |
| **client_fit** | Predicts which family THIS client will love (persona + appeal ranking); optional contest-brief decode + revealed-preference refine loop | **Client Fit (LOG-CFP-001)** |
| **concept_prompt** | Executable concepts: 4 prompt variants, 5 model adaptations, deterministic wireframe spec | **Concept Prompt (LOG-CP-001)** |
| ssb | Strategic Sketch Brief (the flagship output) | SSB Composer |
| sketch | Designer uploads sketches (image or description); coach critiques | Sketch Coach (LOG-COACH-001) |
| presentation | 10-section client deck + objection handling | Presentation (LOG-PRESENT-001) |
| complete | Terminal | — |

`client_fit` and `concept_prompt` are **skippable** — the critical path allows judge → ssb directly.

---

## 3. Architecture & Repository Layout

**Stack:** FastAPI (Python 3.11+) backend · Next.js 14 + Tailwind frontend · SQLite (dev) / PostgreSQL (prod, Neon) · AI via a provider abstraction (Mock / OpenAI / OpenRouter / **NVIDIA NIM**).

```
LogoMind/
├── backend/                  # FastAPI app
│   ├── app/
│   │   ├── main.py           # App factory; dual-mounts router at /api and /api/backend;
│   │   │                     #   /health self-diagnoses (db + knowledge state)
│   │   ├── database.py       # Engine + init_db (resilient: DB failure ≠ boot failure)
│   │   ├── models/           # SQLAlchemy: Project, User, Sketch, DecisionLog…
│   │   ├── schemas/          # Pydantic contracts for every stage
│   │   ├── routers/          # ALL endpoints (single router file)
│   │   └── services/         # THE BRAIN
│   │       ├── engines.py            # Strategy/Insight/Create/Judge/SSB/Coach/Presentation
│   │       ├── discovery_engine.py   # Brief analysis + intent extraction
│   │       ├── concept_engine.py     # Concept Prompt engine (+ two-pass fallback)
│   │       ├── client_fit_engine.py  # Client Preference Predictor
│   │       ├── contest_engine.py     # Contest Brief Decoder (extraction-only)
│   │       ├── ai_orchestrator.py    # Providers, retry, tolerant JSON parsing, mocks
│   │       ├── lic_knowledge.py      # LIC loader (see §4)
│   │       └── _exemplars.py         # Style anchors injected into Create/Concept prompts
│   ├── alembic/              # Migrations (initial + image columns)
│   ├── 05_RS_LICs/           # VENDORED COPY of the knowledge corpus (serverless bundle)
│   └── tests/                # 31 tests: pipeline walks, contest, knowledge guards
├── frontend/
│   ├── src/app/              # Next.js App Router: dashboard, /projects/[id] (13-stage switch)
│   ├── src/components/       # One view per stage + StageStatus, Wireframe, ThemeToggle
│   ├── src/lib/api.ts        # API client (StageApiError handling) + uploadSketchImage
│   └── tailwind.config.js    # Theme tokens → CSS vars (dark default + light)
├── 05_RS_LICs/               # THE knowledge corpus (source of truth, 24 volumes)
├── 04_LOGOS_Engines/         # Engine specs (LOG-*) + LOGOS_ENGINE_SUMMARY.md
├── 07_Product/               # Vision, personas, journey, screens, backlog
├── scripts/sync_backend_lics.py  # Syncs 05_RS_LICs → backend/05_RS_LICs
├── vercel.json               # Multi-service deploy config (frontend + backend services)
├── DEPLOYMENT.md             # Deploy guide (matches shipped reality)
├── ROADMAP.md                # v5.1 — phases 0–5 complete, phase 6 (launch) next
└── HANDOVER.md               # ← this file
```

**Theme:** Claude-inspired dark theme is the **default** ("studio at night": `#262524` charcoal + `#D97757` coral), with the original warm-paper light theme via a header sun/moon toggle. All colors flow through CSS variables (`globals.css`) referenced by Tailwind tokens (`paper/stock/ink/graphite/rule/accent/ok/warn/bad/info/stamp.*`).

---

## 4. The Knowledge System (LogoMind's moat)

**24 LIC volumes across 11 domains**, loaded and sliced at startup by `backend/app/services/lic_knowledge.py`, injected into engine system prompts as "CANONICAL LOGOMIND KNOWLEDGE" blocks.

### Volume inventory
| Series | Volumes | Notes |
|---|---|---|
| Philosophy PH-001…010 | 10 deep textbook LICs | Meaning, Purpose, Simplicity, Clarity, Originality, Memorability, Authenticity, Timelessness, Relevance, Consistency |
| Brand Strategy BS-001…005 | 5 | Positioning, Differentiation, Audience, Personality, Archetypes (12-type table) |
| `RS-LIC-SY-VOLUME` | **50 symbols** | meanings, originality risk, avoid-when, cultural notes |
| `RS-LIC-CL-VOLUME` | **25 colours** + WCAG/colour-blind standards | psychology, pairings, accessibility |
| `RS-LIC-TY-VOLUME` | 15 type categories + weight/case/tracking semantics + pairing rules | |
| `RS-LIC-ID-VOLUME` | 10 identity concepts | grids, logo types, optical correction, scale test |
| `RS-LIC-IND-VOLUME` | 20 industries | conventions, cliché maps, opportunities |
| `RS-LIC-PSY-VOLUME` | **12 decision-maker types** + Feedback Decoder (12 phrases) + Objection Taxonomy (9) + Rationale Narrative | target reached |
| `RS-LIC-PRD-VOLUME` | Production & Deliverables | scale test, file formats, clear space, handoff |
| `RS-LIC-CON-VOLUME` | Contest Dynamics | rating/elimination signals, no-feedback loops |
| `RS-LIC-TM-VOLUME` | Trademark & Distinctiveness | spectrum, refusal grounds, clearance |

### Engine → knowledge wiring (9 of 11 LLM engines grounded)
| Engine | Injects |
|---|---|
| Strategy | BS-001…005 |
| Insight | PH-008, PH-009, SY, IND |
| Create | PH-005, SY, CL, TY, ID, IND + style anchors |
| Judge | PH-005/003/004/006/008, TM |
| Client Fit | CL, SY, BS-005, PSY, CON |
| Concept Prompt | PH-005, ID, PRD + style anchors |
| SSB | ID, PRD |
| Sketch Coach | PH-003, PH-004, PRD |
| Presentation | PSY |

Deliberately **ungrounded**: Contest Decoder (extraction purity) and Discovery (no design canon needed).

### ⚠️ CRITICAL maintenance rule
The corpus source of truth is root `05_RS_LICs/`. The serverless bundle only includes `backend/`, so a **vendored copy lives at `backend/05_RS_LICs/`**. **After editing any LIC volume, run `python scripts/sync_backend_lics.py` and commit both copies.** The loader resolves: `LOGOMIND_LIC_DIR` env → repo root → `backend/05_RS_LICs` (first existing wins).

**Guard tests** (`backend/tests/test_knowledge.py`): every registry entry resolves non-empty; every wiring claim above is asserted against the actual prompts; expansion milestones (SY-050, CL-025, TY-015, IND-020, PSY-015) asserted. If a slicer anchor drifts, tests catch it.

---

## 5. AI Providers

Config via env (`backend/.env` locally; Vercel project env vars in prod):
- `LOGOMIND_AI_PROVIDER` = `mock` | `openai` | `openrouter` | `nim` — **production uses `nim`**
- `NVIDIA_API_KEY` — the NVIDIA key
- `LOGOMIND_MODEL` = `nvidia/nemotron-3-ultra-550b-a55b` (big/slow; swap to a smaller model if serverless timeouts bite)

**NIM gotcha (fixed, do not regress):** NVIDIA's endpoint rejects `response_format={"type":"json_object"}`. `OpenAIProvider.complete` omits `response_format` for NIM base URLs and relies on prompts + `parse_json_response` (tolerant: fences, prose, nested objects). Engines also retry with compliance nudges; Concept Prompt has a chunked two-pass fallback.

**Mock provider** dispatches on the system prompt's first line ("You are LOGOS …") — every engine needs its mock branch or the no-key pipeline breaks. All 31 tests run on mock.

**Long-stage reality:** Judge/Concept Prompt can run minutes on nemotron-ultra. The frontend shows elapsed progress + retry (`useStageAction` + `StageStatus`); backend retries transient failures 3×.

---

## 6. Running Locally

```bash
# Backend (http://127.0.0.1:8000, docs at /docs)
cd backend
pip install -r requirements.txt
# backend/.env already exists with NIM creds; add LOGOMIND_AI_PROVIDER=mock to override
uvicorn app.main:app --reload

# Frontend (http://localhost:3000, proxies /api → :8000)
cd frontend
npm install && npm run dev

# Tests (31, hermetic: in-memory SQLite + mock provider)
pytest backend/tests

# Typecheck
cd frontend && npx tsc --noEmit
```

Dev DB is `backend/logomind.db` (gitignored). `.env` is gitignored — never commit it.

---

## 7. Live Deployment (free tier, fully working)

**URL: https://logo-mind-two.vercel.app** — verify anytime: `GET /api/health` →
`{"status":"healthy","db":{"scheme":"postgresql","ok":true},"knowledge":{"loaded":true,"available":[…24 ids…]}}`

### Topology — ONE multi-service Vercel project
- Project `logo-mind` in Vercel team **`abhishek-d40d`** (Hobby plan)
- **frontend service** ← `frontend/` (Next.js) — serves the UI
- **backend service** ← `backend/` (FastAPI, entrypoint `app/main.py`) — answers `/api/*` and `/api/backend/*` (router dual-mounted; `/health` aliased under both prefixes)
- Rewrites in root `vercel.json` send `/api/*` → backend, everything else → frontend. Same origin → **no CORS config needed in prod**
- **Database:** Neon free Postgres `neon-apricot-door` (Neon ID `crimson-pine-19201066`), created via Vercel Storage marketplace; `DATABASE_URL` (pooled, with `DATABASE_URL_UNPOOLED` etc.) injected into the project for Production+Preview. Schema was created by `init_db()`'s `create_all` on first boot (running `alembic stamp head` against it is optional bookkeeping)
- GitHub App access scoped to **only** the LogoMind repo (founder requirement)
- Auth: **none, by founder decision (2026-08-14)** — single shared workspace; anyone with the URL can use it

### Env vars set in Vercel (Production + Preview)
`DATABASE_URL` (from Neon) · `LOGOMIND_AI_PROVIDER=nim` · `NVIDIA_API_KEY` · `LOGOMIND_MODEL`

### Deploy / redeploy
1. Push to `main` → auto-deploy (usually).
2. **If the webhook ever misses** (it did during setup): project Settings → Git → **`zap-deploy`** deploy hook — POST its URL to trigger a production deploy of `main`. This hook is the reliable manual channel. (Hook URL is visible in the dashboard; deliberately not pasted here since the repo is public.)
3. Watch build in Vercel dashboard; runtime errors in **Logs** tab (filter Error, expand a row for the traceback).

### Serverless constraints baked into the code
- **Read-only filesystem** → SQLite default would crash; `init_db` failures now degrade to `/health`'s `db.error` instead of crashing boot
- **4 MB request body** → sketch image uploads capped at 3.5 MB (`LOGOMIND_MAX_IMAGE_BYTES`); images stored **in the DB** (`sketches.image_data` + content type), served via `GET /api/projects/{id}/sketches/{sketch_id}/image`
- **Bundles exclude files outside the service root** → hence vendored `backend/05_RS_LICs`
- `postgres://` URLs normalised to `postgresql://`; `pool_pre_ping` on for Neon

### Debugging playbook (earned the hard way)
| Symptom | Cause | Check |
|---|---|---|
| `/api/*` → 500 `FUNCTION_INVCATION_FAILED` | lifespan crash | Logs tab; `/api/health` after fix |
| `sqlite3.OperationalError: unable to open database file` in traceback | `DATABASE_URL` not present at runtime (deployment predates env var) | redeploy so the build snapshots current env |
| Every path 404 with `{"detail":"Not Found"}` (FastAPI body) | route lives on app, not router; or prefix mismatch | `/api/projects` is the canonical probe |
| Deploy didn't start after push | GitHub webhook miss | fire the `zap-deploy` hook |

---

## 8. Key Decisions Log (why things are the way they are)

| Decision | Date | Rationale |
|---|---|---|
| **No auth / no sign-up** | 2026-08-14 | Founder decision; shared workspace. Revisit only if multi-user isolation becomes real |
| Free-tier Vercel + Neon | 2026-08-17 | Zero-cost hosting |
| GitHub App scoped to LogoMind repo only | 2026-08-17 | Founder security requirement — no other repo authorised |
| Single multi-service project (not two projects) | 2026-08-17 | Same-origin (no CORS), one project slot, Vercel detected the monorepo natively |
| DB-stored sketch images | 2026-08-17 | Serverless has no persistent FS |
| Dark theme default + light toggle | 2026-08-17 | Founder chose "Claude's dark theme" after seeing rendered mockups |
| Client Fit drops TY volume | 2026-08-16 | Token budget; Create owns type choice |
| Contest Decoder stays knowledge-light | 2026-08-16 | Extraction purity — creativity is a defect there |
| Big prompts accepted (Create ~15.8k tok, Client Fit ~13.6k tok) | 2026-08-16 | Generative core needs the vocabulary; 128k contexts handle it |

---

## 9. Current State & What's Next

**Done (Phases 0–5 of ROADMAP v5.1):** 13-stage pipeline live; 24 knowledge volumes wired into 9 engines; 31 backend tests; Alembic migrations; real sketch image upload; Claude-dark theme; deployed and verified end-to-end on the free tier (a real NIM Discovery run succeeded on the live site).

**Open backlog (priority order):**
1. **Catalog expansion toward declared targets** — symbols 50/150+, industries 20/30+, type 15/40+, colours 25/50+ (each volume's metadata table records its target; update `test_knowledge.py` milestones as you go)
2. **Original 23 backlog gaps:** #7 Brand DNA editing (no PATCH endpoint), #16 SSB export (PDF/Markdown), #19 Progressive Disclosure (LM-STD-005 Layer A)
3. **Phase 6 launch items:** beta with real designers, marketing, pricing
4. Optional hardening: 2FA on the Vercel account, Web Analytics/Speed Insights toggles (checklist 1/5), `alembic stamp head` on Neon

**Known minor states:** one test project ("Deploy Check") exists in prod as an artifact; local `backend/uploads/` is vestigial (images now DB-stored); `PHASE5_README`/docs were refreshed in the Tier-3 pass — keep them honest when things change.

---

## 10. Handover Card (pin this)

```
LIVE APP      https://logo-mind-two.vercel.app   (no login, shared workspace)
HEALTH        GET /api/health  → db + knowledge self-diagnosis
REPO          github.com/Abhishekvasani/LogoMind  (main; public)
VERCEL        team abhishek-d40d → project logo-mind (Hobby, 2 services)
DATABASE      Neon neon-apricot-door (free; env injected as DATABASE_URL)
REDEPLOY      push to main; fallback hook "zap-deploy" (Settings → Git)
RUN LOCALLY   backend: uvicorn app.main:app --reload  |  frontend: npm run dev
TESTS         pytest backend/tests  (31/31 green)
AFTER LIC EDIT python scripts/sync_backend_lics.py && commit both copies
MODEL         NIM nemotron-3-ultra (slow for judge/concept — UI has retry)
```

### Session history at a glance (this arc, oldest → newest)
Contest Intelligence UI (backend done prior) → NIM JSON-mode fix → Claude dark theme + toggle → knowledge audit → Tier 1 wiring (all volumes into engines) → Tier 2 volumes (IND/PSY/PRD/CON/TM + catalog expansion) → Tier 3 docs (ROADMAP v5.1, LOG-CFP-001, LOG-CBD-001) → forward work (catalogs to milestone, sketch upload, Alembic) → Vercel deploy (fixing: entrypoint, env-snapshot, LIC bundling, health aliasing, webhook via deploy hook) → live & verified.

---

*Reason. Create. Refine.*
