import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, Enum as SAEnum, ForeignKey, String
from sqlalchemy import JSON
from sqlalchemy.orm import relationship

from app.database import Base
from app.models.batch import FeedbackType


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    feedback_id = Column(String, nullable=False)       # e.g. "MID-2025-001"
    feedback_type = Column(SAEnum(FeedbackType), nullable=False)
    source_file = Column(String, nullable=False)        # original filename
    date = Column(Date, nullable=True)
    persona_json = Column(JSON, nullable=False)
    body_json = Column(JSON, nullable=False)            # full Q&A array — source of truth
    related_schools = Column(JSON, nullable=False, default=list)
    related_services = Column(JSON, nullable=False, default=list)
    overall_sentiment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    batch = relationship("Batch", back_populates="feedbacks")
    extractions = relationship("Extraction", back_populates="feedback")
