"""
Unit tests for issue #1 — JSON feedback ingestion pipeline.
Covers all 5 acceptance criteria from the GitHub issue.
Uses SQLite in-memory; no Docker or PostgreSQL required.
"""
import json
from pathlib import Path

import pytest

from app.models.batch import Batch, BatchError, BatchStatus, FeedbackType
from app.models.feedback import Feedback
from app.services.ingestion import _run  # test internal fn directly for simplicity


VALID_FEEDBACK = {
    "metadata": {
        "feedback_id": "MID-2025-001",
        "date": "2025-11-15",
        "type": "MID_TERM",
        "persona": {"id": "SV001", "name": "Nguyen Van An", "role": "student"},
        "related_schools": ["IT"],
        "related_services": ["ACADEMIC"],
        "overall_sentiment": "positive",
    },
    "body": [
        {"question_1": "How is teaching quality?", "answer_1": "Teaching quality is excellent."},
        {"question_2": "How are IT services?", "answer_2": "IT support is responsive."},
    ],
}


def write_file(directory: Path, name: str, content) -> Path:
    path = directory / name
    if isinstance(content, dict):
        path.write_text(json.dumps(content))
    else:
        path.write_text(content)
    return path


def make_batch(db, tmp_path) -> Batch:
    batch = Batch(feedback_type=FeedbackType.MID_TERM, folder_path=str(tmp_path))
    db.add(batch)
    db.commit()
    return batch


# ── Test 1: Valid JSON file is parsed and inserted correctly ─────────────────

def test_valid_file_inserted(db, tmp_path):
    write_file(tmp_path, "001.json", VALID_FEEDBACK)
    batch = make_batch(db, tmp_path)

    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.status == BatchStatus.COMPLETE
    assert batch.successful_count == 1
    assert batch.failed_count == 0

    feedback = db.query(Feedback).first()
    assert feedback is not None
    assert feedback.feedback_id == "MID-2025-001"
    assert feedback.feedback_type == FeedbackType.MID_TERM
    assert feedback.related_schools == ["IT"]
    assert feedback.overall_sentiment == "positive"
    assert len(feedback.body_json) == 2


# ── Test 2: Malformed JSON skipped; batch continues with remaining files ─────

def test_malformed_json_skipped_batch_continues(db, tmp_path):
    write_file(tmp_path, "001.json", VALID_FEEDBACK)
    write_file(tmp_path, "002.json", "{not valid json")

    batch = make_batch(db, tmp_path)
    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.status == BatchStatus.COMPLETE
    assert batch.successful_count == 1
    assert batch.failed_count == 1

    # Valid file was saved
    assert db.query(Feedback).count() == 1

    # Error was logged for the bad file
    error = db.query(BatchError).filter(BatchError.filename == "002.json").first()
    assert error is not None
    assert "Invalid JSON" in error.error_reason


# ── Test 3: Missing required fields → validation error, file skipped ─────────

def test_missing_required_fields_skipped(db, tmp_path):
    incomplete = {
        "metadata": {"date": "2025-11-15"},  # missing feedback_id, type, persona, etc.
        "body": [],
    }
    write_file(tmp_path, "001.json", incomplete)

    batch = make_batch(db, tmp_path)
    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.failed_count == 1
    assert db.query(Feedback).count() == 0

    error = db.query(BatchError).first()
    assert "Schema invalid" in error.error_reason


# ── Test 4: Empty folder → FAILED status, not a crash ───────────────────────

def test_empty_folder_fails_gracefully(db, tmp_path):
    batch = make_batch(db, tmp_path)
    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.status == BatchStatus.FAILED
    assert batch.successful_count == 0
    assert batch.failed_count == 0
    assert db.query(Feedback).count() == 0


# ── Test 5: Batch status transitions pending → complete; completed_at set ────

def test_batch_status_transitions(db, tmp_path):
    write_file(tmp_path, "001.json", VALID_FEEDBACK)
    batch = make_batch(db, tmp_path)

    assert batch.status == BatchStatus.PENDING

    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.status == BatchStatus.COMPLETE
    assert batch.completed_at is not None
    assert batch.total_files == 1


# ── Test 6: Per-type persona shapes (PARENTS, INTERNSHIP) validate correctly ─
# Regression test: PARENTS and INTERNSHIP personas don't have a plain `name`
# field like MID_TERM/YEAR_END, so a single shared persona schema rejects them.

def test_parents_persona_shape_accepted(db, tmp_path):
    feedback = {
        "metadata": {
            "feedback_id": "PAR-2025-001",
            "date": "2025-11-15",
            "type": "PARENTS",
            "persona": {"id": "PA001", "name": "Tran Thi Binh", "role": "parent", "child_name": "Tran Van Cuong"},
            "related_schools": ["IT"],
            "related_services": ["ACADEMIC"],
            "overall_sentiment": "positive",
        },
        "body": [{"question_1": "How is teaching quality?", "answer_1": "Good."}],
    }
    write_file(tmp_path, "001.json", feedback)
    batch = Batch(feedback_type=FeedbackType.PARENTS, folder_path=str(tmp_path))
    db.add(batch)
    db.commit()

    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.successful_count == 1
    assert batch.failed_count == 0


def test_internship_persona_shape_accepted(db, tmp_path):
    feedback = {
        "metadata": {
            "feedback_id": "INT-2025-001",
            "date": "2025-11-15",
            "type": "INTERNSHIP",
            "persona": {
                "id": "EMP001",
                "role": "employer",
                "evaluator_name": "Vo Kim Khanh",
                "intern_name": "Huynh Thi Lan",
            },
            "related_schools": ["BUS"],
            "related_services": ["CAREER"],
            "overall_sentiment": "mostly_positive",
        },
        "body": [{"question_1": "How is the intern's competency?", "answer_1": "Good."}],
    }
    write_file(tmp_path, "001.json", feedback)
    batch = Batch(feedback_type=FeedbackType.INTERNSHIP, folder_path=str(tmp_path))
    db.add(batch)
    db.commit()

    _run(batch.id, str(tmp_path), db)

    db.refresh(batch)
    assert batch.successful_count == 1
    assert batch.failed_count == 0
