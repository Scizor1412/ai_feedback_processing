"""
Unit tests for issue #3 — CSV generation.
Uses SQLite in-memory; seeds real Feedback and Extraction rows.
"""
import csv
import io

from app.models.batch import Batch, BatchStatus, FeedbackType
from app.models.extraction import EntityType, Extraction, Sentiment
from app.models.feedback import Feedback
from app.services.csv_export import generate_csv


def seed(db):
    batch = Batch(feedback_type=FeedbackType.MID_TERM, folder_path="/tmp")
    db.add(batch)
    db.commit()

    fb = Feedback(
        batch_id=batch.id, feedback_id="MID-001",
        feedback_type=FeedbackType.MID_TERM, source_file="001.json",
        persona_json={}, body_json=[],
        related_schools=["IT"], related_services=[], overall_sentiment="positive",
    )
    db.add(fb)
    db.commit()

    pos = Extraction(
        feedback_id=fb.id, batch_id=batch.id,
        entity_id="IT", entity_type=EntityType.SCHOOL,
        source_question="How is teaching?", source_answer="Teaching is great.",
        sentiment=Sentiment.POSITIVE,
    )
    neg = Extraction(
        feedback_id=fb.id, batch_id=batch.id,
        entity_id="IT", entity_type=EntityType.SCHOOL,
        source_question="How is IT support?", source_answer="IT support is very slow.",
        sentiment=Sentiment.NEGATIVE,
    )
    db.add_all([pos, neg])
    db.commit()
    return batch, fb


# ── Test 1: CSV has correct headers ──────────────────────────────────────────

def test_csv_correct_headers(db):
    batch, _ = seed(db)
    buf = generate_csv(db, batch.id, "IT", Sentiment.POSITIVE)
    reader = csv.reader(buf)
    headers = next(reader)
    assert headers == ["feedback_id", "source_question", "source_answer"]


# ── Test 2: positive and negative CSVs separated correctly ───────────────────

def test_positive_negative_separated(db):
    batch, _ = seed(db)

    pos_buf = generate_csv(db, batch.id, "IT", Sentiment.POSITIVE)
    neg_buf = generate_csv(db, batch.id, "IT", Sentiment.NEGATIVE)

    pos_rows = list(csv.reader(pos_buf))[1:]  # skip header
    neg_rows = list(csv.reader(neg_buf))[1:]

    assert len(pos_rows) == 1
    assert len(neg_rows) == 1
    assert "great" in pos_rows[0][2]
    assert "slow" in neg_rows[0][2]


# ── Test 3: empty result → valid CSV with headers only ───────────────────────

def test_empty_result_returns_header_only(db):
    batch, _ = seed(db)
    buf = generate_csv(db, batch.id, "FINANCE", Sentiment.POSITIVE)
    rows = list(csv.reader(buf))
    assert len(rows) == 1  # only header
    assert rows[0] == ["feedback_id", "source_question", "source_answer"]


# ── Test 4: CSV contains feedback_id, source_question, source_answer ─────────

def test_csv_columns_correct(db):
    batch, fb = seed(db)
    buf = generate_csv(db, batch.id, "IT", Sentiment.POSITIVE)
    rows = list(csv.reader(buf))
    data_row = rows[1]
    assert data_row[0] == "MID-001"          # feedback_id
    assert data_row[1] == "How is teaching?" # source_question
    assert data_row[2] == "Teaching is great."  # source_answer
