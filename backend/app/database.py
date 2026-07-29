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
    """Create all tables. Called on app startup."""
    # Import models so they register with Base.metadata before create_all.
    from . import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
