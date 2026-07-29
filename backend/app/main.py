"""
LogoMind FastAPI application.

The complete backend — wires together database, AI orchestration,
and all 9 pipeline stages (PROD-JOURNEY-001).

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


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialise database on startup."""
    init_db()
    yield


app = FastAPI(
    title="LogoMind API",
    description="""
    LogoMind — Strategic Design Intelligence Platform.

    LogoMind helps logo designers think like world-class creative directors
    by transforming an incomplete client brief into a complete creative
    strategy (the Strategic Sketch Brief).

    **LogoMind will never make a creative decision for the designer.**

    Pipeline: Brief → Discovery → Strategy → Insight → Create → Judge → SSB → Coach → Presentation
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
app.include_router(router, prefix="/api", tags=["logomind"])


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
    return {"status": "healthy"}
