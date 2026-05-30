"""
Unit tests for issue #2 — AI extraction engine.
Mocks the AsyncOpenAI client; no real API calls made.
"""
import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.models.batch import Batch, BatchStatus, FeedbackType
from app.models.extraction import EntityType, Extraction, Sentiment
from app.models.feedback import Feedback
from app.services.extraction import _run, _to_extraction_rows, _system_prompt, _user_message


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_mock_client(mentions: list[dict]) -> MagicMock:
    content = json.dumps({"mentions": mentions})
    mock_resp = MagicMock()
    mock_resp.choices = [MagicMock()]
    mock_resp.choices[0].message.content = content
    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=mock_resp)
    return client


BODY = [
    {"question_1": "How is teaching quality?", "answer_1": "Teaching is excellent at the IT school."},
    {"question_2": "How is finance?", "answer_2": "Finance department is slow to respond."},
]

VALID_FEEDBACK_DATA = {
    "metadata": {
        "feedback_id": "MID-001", "date": "2025-11-15", "type": "MID_TERM",
        "persona": {"id": "SV001", "name": "Test User", "role": "student"},
        "related_schools": ["IT"], "related_services": ["FINANCE"],
        "overall_sentiment": "mixed",
    },
    "body": BODY,
}


def seed_batch_and_feedback(db) -> tuple[Batch, Feedback]:
    from app.services.ingestion import _ingest_file
    import tempfile, pathlib, json as _json

    batch = Batch(feedback_type=FeedbackType.MID_TERM, folder_path="/tmp")
    db.add(batch)
    db.commit()

    feedback = Feedback(
        batch_id=batch.id,
        feedback_id="MID-001",
        feedback_type=FeedbackType.MID_TERM,
        source_file="001.json",
        persona_json={"id": "SV001", "name": "Test", "role": "student"},
        body_json=BODY,
        related_schools=["IT"],
        related_services=["FINANCE"],
        overall_sentiment="mixed",
    )
    db.add(feedback)
    db.commit()
    return batch, feedback


# ── Test 1: single school mention → 1 Extraction row ─────────────────────────

def test_single_mention_creates_extraction(db):
    batch, feedback = seed_batch_and_feedback(db)
    mentions = [{"qa_index": 1, "entity_id": "IT", "entity_type": "school", "sentiment": "positive"}]

    client = make_mock_client(mentions)
    with patch("app.services.extraction.AsyncOpenAI", return_value=client):
        asyncio.run(_run(batch.id, db))

    rows = db.query(Extraction).all()
    assert len(rows) == 1
    assert rows[0].entity_id == "IT"
    assert rows[0].entity_type == EntityType.SCHOOL
    assert rows[0].sentiment == Sentiment.POSITIVE
    assert rows[0].source_question == BODY[0]["question_1"]
    assert rows[0].source_answer == BODY[0]["answer_1"]


# ── Test 2: multiple entity mentions → multiple rows ──────────────────────────

def test_multiple_mentions_all_stored(db):
    batch, feedback = seed_batch_and_feedback(db)
    mentions = [
        {"qa_index": 1, "entity_id": "IT", "entity_type": "school", "sentiment": "positive"},
        {"qa_index": 2, "entity_id": "FINANCE", "entity_type": "service", "sentiment": "negative"},
    ]

    client = make_mock_client(mentions)
    with patch("app.services.extraction.AsyncOpenAI", return_value=client):
        asyncio.run(_run(batch.id, db))

    rows = db.query(Extraction).order_by(Extraction.entity_id).all()
    assert len(rows) == 2
    entity_ids = {r.entity_id for r in rows}
    assert entity_ids == {"FINANCE", "IT"}


# ── Test 3: no mentions → zero rows, no crash ─────────────────────────────────

def test_no_mentions_produces_no_rows(db):
    batch, feedback = seed_batch_and_feedback(db)
    client = make_mock_client([])

    with patch("app.services.extraction.AsyncOpenAI", return_value=client):
        asyncio.run(_run(batch.id, db))

    assert db.query(Extraction).count() == 0


# ── Test 4: unknown entity_id in response is discarded ────────────────────────

def test_unknown_entity_id_discarded(db):
    batch, feedback = seed_batch_and_feedback(db)
    mentions = [
        {"qa_index": 1, "entity_id": "NONEXISTENT_SCHOOL", "entity_type": "school", "sentiment": "positive"},
        {"qa_index": 1, "entity_id": "IT", "entity_type": "school", "sentiment": "positive"},
    ]

    client = make_mock_client(mentions)
    with patch("app.services.extraction.AsyncOpenAI", return_value=client):
        asyncio.run(_run(batch.id, db))

    rows = db.query(Extraction).all()
    assert len(rows) == 1
    assert rows[0].entity_id == "IT"


# ── Test 5: invalid JSON from API → retried, then skipped (no crash) ──────────

def test_invalid_json_retried_then_skipped(db):
    batch, feedback = seed_batch_and_feedback(db)

    bad_resp = MagicMock()
    bad_resp.choices = [MagicMock()]
    bad_resp.choices[0].message.content = "not json at all {{{"

    client = MagicMock()
    client.chat.completions.create = AsyncMock(return_value=bad_resp)

    with patch("app.services.extraction.AsyncOpenAI", return_value=client):
        asyncio.run(_run(batch.id, db))

    # No crash, no rows, API called twice (retry)
    assert db.query(Extraction).count() == 0
    assert client.chat.completions.create.call_count == 2
