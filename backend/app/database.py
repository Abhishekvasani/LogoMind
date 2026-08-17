"""
Database configuration and session management.
"""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base  # noqa: F401 (re-export Base for migrations)

# Load variables from backend/.env so configuration is honoured.
load_dotenv()

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "sqlite:///./logomind.db"
)  # dev default; production: PostgreSQL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite dev only
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency — yields a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables. Called on app startup.

    Note: create_all only adds NEW tables; it does not add columns to existing
    ones (Alembic would, but is not wired here). For the dev SQLite DB we
    apply a small, guarded column migration so existing installs pick up the
    concept_prompts column without a manual DB reset. Production (Postgres)
    should use Alembic migrations instead.
    """
    # Import models so they register with Base.metadata before create_all.
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Dev-only: add columns the create_all path can't backfill onto an
    # existing SQLite table. Idempotent — checks PRAGMA first.
    if DATABASE_URL.startswith("sqlite"):
        _migrate_sqlite_columns(engine)


def _migrate_sqlite_columns(engine) -> None:
    """Add any missing JSON columns to the projects table (SQLite dev only).

    Each entry: (column name, SQL type). Safe to extend as new stage outputs
    are added. ALTER TABLE ADD COLUMN is a no-op if the column already exists
    because we guard with PRAGMA table_info first.
    """
    import logging

    from sqlalchemy import inspect, text

    insp = inspect(engine)
    if "projects" not in insp.get_table_names():
        return  # nothing to migrate; create_all will build it fresh

    existing = {c["name"] for c in insp.get_columns("projects")}
    # Columns introduced after the initial schema, with their SQL types.
    needed = [
        ("concept_prompts", "JSON"),
        ("client_persona", "JSON"),
        ("appeal_report", "JSON"),
        ("contest_brief", "JSON"),
        ("contest_feedback", "JSON"),
    ]
    with engine.begin() as conn:
        for col, col_type in needed:
            if col not in existing:
                conn.execute(text(f'ALTER TABLE projects ADD COLUMN "{col}" {col_type}'))
                logging.getLogger("logomind").info("Migrated SQLite: added column projects.%s", col)

    # Sketches gained DB-backed image storage (serverless-safe): backfill the
    # columns for existing installs the same guarded way.
    if "sketches" in insp.get_table_names():
        sketch_cols = {c["name"] for c in insp.get_columns("sketches")}
        sketch_needed = [
            ("image_data", "BLOB"),
            ("image_content_type", "VARCHAR(64)"),
        ]
        with engine.begin() as conn:
            for col, col_type in sketch_needed:
                if col not in sketch_cols:
                    conn.execute(text(f'ALTER TABLE sketches ADD COLUMN "{col}" {col_type}'))
                    logging.getLogger("logomind").info("Migrated SQLite: added column sketches.%s", col)
