"""
Database configuration and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from . import Base  # re-export for convenience

DATABASE_URL = "sqlite:///./logomind.db"  # dev default; production: PostgreSQL

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
    Base.metadata.create_all(bind=engine)
