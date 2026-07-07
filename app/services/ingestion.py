import json
import logging
from datetime import date, datetime, timezone
from pathlib import Path

from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.batch import Batch, BatchError, BatchStatus
from app.models.feedback import Feedback
from app.schemas.feedback import FeedbackSchema

logger = logging.getLogger(__name__)


def walk_and_ingest(batch_id: str, folder_path: str) -> None:
    """Read all JSON files from folder_path, validate, and persist to DB.

    Creates its own DB session — safe to run as a FastAPI BackgroundTask.
    Malformed or invalid files are logged to batch_errors; the batch continues.
    """
    db: Session = SessionLocal()
    try:
        _run(batch_id, folder_path, db)
    finally:
        db.close()


def _run(batch_id: str, folder_path: str, db: Session) -> None:
    batch = db.get(Batch, batch_id)
    if not batch:
        logger.error("Batch %s not found", batch_id)
        return

    batch.status = BatchStatus.PROCESSING
    db.commit()

    files = sorted(Path(folder_path).glob("*.json"))

    if not files:
        batch.status = BatchStatus.FAILED
        batch.completed_at = datetime.now(timezone.utc)
        db.commit()
        logger.warning("No JSON files found in %s", folder_path)
        return

    batch.total_files = len(files)
    db.commit()

    successful = 0
    failed = 0

    for file in files:
        error = _ingest_file(file, batch_id, db)
        if error:
            db.add(BatchError(batch_id=batch_id, filename=file.name, error_reason=error))
            db.commit()
            failed += 1
        else:
            successful += 1

    batch.successful_count = successful
    batch.failed_count = failed
    batch.status = BatchStatus.COMPLETE
    batch.completed_at = datetime.now(timezone.utc)
    db.commit()
    logger.info("Batch %s complete: %d ok, %d failed", batch_id, successful, failed)


def _ingest_file(file: Path, batch_id: str, db: Session) -> str | None:
    """Return error string on failure, None on success."""
    try:
        raw = file.read_text(encoding="utf-8")
    except OSError as e:
        return f"Cannot read file: {e}"

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {e}"

    try:
        validated = FeedbackSchema.model_validate(data)
    except ValidationError as e:
        return f"Schema invalid: {e.error_count()} error(s) — {e.errors()[0]['msg']}"

    try:
        feedback_date = date.fromisoformat(validated.metadata.date)
    except ValueError:
        feedback_date = None

    try:
        db.add(Feedback(
            batch_id=batch_id,
            feedback_id=validated.metadata.feedback_id,
            feedback_type=validated.metadata.type,
            source_file=file.name,
            date=feedback_date,
            persona_json=validated.metadata.persona,
            body_json=validated.body,
            related_schools=validated.metadata.related_schools,
            related_services=validated.metadata.related_services,
            overall_sentiment=validated.metadata.overall_sentiment,
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        return f"DB error: {e}"

    return None
