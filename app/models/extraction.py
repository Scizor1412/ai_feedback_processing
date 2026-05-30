import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class EntityType(str, enum.Enum):
    SCHOOL = "school"
    SERVICE = "service"


class Sentiment(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"


class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    feedback_id = Column(String(36), ForeignKey("feedbacks.id"), nullable=False)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    entity_id = Column(String, nullable=False)          # e.g. "IT", "FINANCE"
    entity_type = Column(SAEnum(EntityType), nullable=False)
    source_question = Column(Text, nullable=False)      # full question text
    source_answer = Column(Text, nullable=False)        # full ~100-word answer (full Q&A context)
    sentiment = Column(SAEnum(Sentiment), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    feedback = relationship("Feedback", back_populates="extractions")
    batch = relationship("Batch")

    __table_args__ = (
        Index("ix_extractions_entity_sentiment_batch", "entity_id", "sentiment", "batch_id"),
    )
