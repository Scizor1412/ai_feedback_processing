"""
Unit tests for issue #4 — Batch review UI.
Uses FastAPI TestClient with SQLite in-memory DB.
"""
import os
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
import app.models  # noqa: F401
from app.models.batch import Batch, BatchStatus, FeedbackType
from app.models.extraction import EntityType, Extraction, Sentiment
from app.models.feedback import Feedback


@pytest.fixture
def client(db):
    """TestClient wired to the test DB session."""
    from app.main import app
    app.dependency_overrides[get_db] = lambda: db
    yield TestClient(app, raise_server_exceptions=True)
    app.dependency_overrides.clear()


def seed_batch(db, status=BatchStatus.EXTRACTED) -> Batch:
    batch = Batch(
        feedback_type=FeedbackType.MID_TERM,
        folder_path="/tmp",
        status=status,
        total_files=1,
        successful_count=1,
    )
    db.add(batch)
    db.commit()
    return batch


def seed_extraction(db, batch: Batch) -> Extraction:
    fb = Feedback(
        batch_id=batch.id, feedback_id="MID-001",
        feedback_type=FeedbackType.MID_TERM, source_file="001.json",
        persona_json={}, body_json=[],
        related_schools=["IT"], related_services=[], overall_sentiment="positive",
    )
    db.add(fb)
    db.commit()

    ex = Extraction(
        feedback_id=fb.id, batch_id=batch.id,
        entity_id="IT", entity_type=EntityType.SCHOOL,
        source_question="How is teaching?", source_answer="Teaching is great.",
        sentiment=Sentiment.POSITIVE,
    )
    db.add(ex)
    db.commit()
    return ex


# ── Test 1: GET / returns 200 with the batch trigger form ────────────────────

def test_trigger_form_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Run a Feedback Batch" in resp.text
    assert "folder_path" in resp.text


# ── Test 2: GET /batches/{id}/review returns 200 with entity table ────────────

def test_review_page_renders_recipients(client, db):
    batch = seed_batch(db)
    seed_extraction(db, batch)

    resp = client.get(f"/batches/{batch.id}/review")
    assert resp.status_code == 200
    assert "IT" in resp.text or "School of Information Technology" in resp.text
    assert "Positive" in resp.text or "pos" in resp.text.lower()


# ── Test 3: GET preview partial returns mention sections ──────────────────────

def test_preview_partial_returns_mentions(client, db):
    batch = seed_batch(db)
    seed_extraction(db, batch)

    resp = client.get(f"/batches/{batch.id}/recipients/IT/preview")
    assert resp.status_code == 200
    assert "Teaching is great." in resp.text
    assert "Positive mentions" in resp.text or "positive" in resp.text.lower()


# ── Test 4: POST mark-reviewed updates batch status ──────────────────────────

def test_mark_reviewed_updates_status(client, db):
    batch = seed_batch(db, status=BatchStatus.EXTRACTED)

    resp = client.post(f"/batches/{batch.id}/mark-reviewed", follow_redirects=False)
    assert resp.status_code in (302, 303)

    db.refresh(batch)
    assert batch.status == BatchStatus.REVIEWED
