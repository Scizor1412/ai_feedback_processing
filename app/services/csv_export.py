"""Generate positive/negative CSVs for a batch recipient (in-memory, no disk writes)."""
import csv
import io

from sqlalchemy.orm import Session

from app.models.extraction import Extraction, Sentiment
from app.models.feedback import Feedback


def generate_csv(db: Session, batch_id: str, entity_id: str, sentiment: Sentiment) -> io.StringIO:
    """Return StringIO with CSV rows for the given batch/entity/sentiment.

    Columns: feedback_id, source_question, source_answer
    Empty result produces a valid CSV with headers only.
    """
    rows = (
        db.query(Feedback.feedback_id, Extraction.source_question, Extraction.source_answer)
        .join(Extraction, Extraction.feedback_id == Feedback.id)
        .filter(
            Extraction.batch_id == batch_id,
            Extraction.entity_id == entity_id.upper(),
            Extraction.sentiment == sentiment,
        )
        .all()
    )

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["feedback_id", "source_question", "source_answer"])
    writer.writerows(rows)
    buf.seek(0)
    return buf
