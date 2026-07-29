"""
Shared fixtures for the LogoMind backend test suite.

Tests run against an in-memory SQLite database and the deterministic Mock AI
provider, so the whole pipeline is exercisable without an API key or cost.
"""

import os
import sys
from pathlib import Path

# Ensure the backend package (app/) is importable when running pytest from
# the backend/ directory or the repo root.
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Force a clean, isolated configuration before the app is imported.
# In-memory SQLite keeps each test process hermetic.
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["LOGOMIND_AI_PROVIDER"] = "mock"
os.environ.pop("OPENAI_API_KEY", None)

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import database as db_module
from app.services.ai_orchestrator import MockAIProvider, set_ai_provider


@pytest.fixture(scope="session")
def test_engine():
    """A single in-memory SQLite engine shared across the test session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # keep one connection so :memory: persists
    )
    # Re-point the app's engine + session at the test engine.
    db_module.engine = engine
    db_module.SessionLocal.configure(bind=engine)
    db_module.init_db()  # create tables
    return engine


@pytest.fixture(scope="session")
def client(test_engine):
    """A TestClient backed by the in-memory engine and Mock AI provider."""
    # Pin the mock provider (also the default, but be explicit for isolation).
    set_ai_provider(MockAIProvider())
    from app.main import app

    with TestClient(app) as c:
        yield c
