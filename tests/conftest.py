import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Use SQLite in-memory for tests — no Docker required
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

from app.database import Base
import app.models  # noqa: F401 — register all models


@pytest.fixture
def db():
    # StaticPool reuses one connection so the in-memory DB survives across
    # threads (needed when TestClient dispatches routes in a threadpool).
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)
