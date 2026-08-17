"""
LogoMind FastAPI application.

The complete backend — wires together database, AI orchestration,
and the full pipeline of stages (PROD-JOURNEY-001).

Run: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load variables from backend/.env so configuration is honoured.
load_dotenv()

from .database import init_db
from .routers import router
from .services import lic_knowledge


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise database and load LIC knowledge on startup."""
    init_db()
    lic_knowledge.load()  # cache curated operational extracts for the engines
    yield


app = FastAPI(
    title="LogoMind API",
    description="""
    LogoMind — Strategic Design Intelligence Platform.

    LogoMind helps logo designers think like world-class creative directors
    by transforming an incomplete client brief into a complete creative
    strategy (the Strategic Sketch Brief).

    **LogoMind will never make a creative decision for the designer.**

    Pipeline: Brief → Discovery → Workshop → Strategy → Insight → Create → Judge →
    Client Fit → Concept Prompt → SSB → Sketch → Presentation
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS for the Next.js frontend.
# CORS_ORIGINS may be a comma-separated list; defaults to the local dev origins.
_default_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
_cors_env = os.environ.get("CORS_ORIGINS", "").strip()
_cors_origins = (
    [o.strip() for o in _cors_env.split(",") if o.strip()] if _cors_env else _default_origins
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routes under /api
# Mount the router twice so the backend answers on /api/* regardless of how
# the hosting layer routes to it: directly (single-service deploys, dev) and
# under the /api/backend service prefix (Vercel multi-service rewrites).
app.include_router(router, prefix="/api", tags=["logomind"])
app.include_router(router, prefix="/api/backend", tags=["logomind"], include_in_schema=False)


@app.get("/")
async def root():
    return {
        "name": "LogoMind API",
        "version": "1.0.0",
        "motto": "Reason. Create. Refine.",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        # Which LIC knowledge extracts actually resolved — a silent empty
        # extract degrades engine grounding with no error, so surface it here.
        "knowledge": {
            "loaded": lic_knowledge.is_loaded(),
            "available": lic_knowledge.available_lics(),
        },
    }
