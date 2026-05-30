import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class FeedbackType(str, enum.Enum):
    MID_TERM = "MID_TERM"
    YEAR_END = "YEAR_END"
    PARENTS = "PARENTS"
    INTERNSHIP = "INTERNSHIP"


class BatchStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETE = "complete"
    FAILED = "failed"


class Batch(Base):
    __tablename__ = "batches"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    feedback_type = Column(SAEnum(FeedbackType), nullable=False)
    folder_path = Column(String, nullable=False)
    status = Column(SAEnum(BatchStatus), nullable=False, default=BatchStatus.PENDING)
    total_files = Column(Integer, default=0)
    successful_count = Column(Integer, default=0)
    failed_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    completed_at = Column(DateTime(timezone=True), nullable=True)

    feedbacks = relationship("Feedback", back_populates="batch")
    errors = relationship("BatchError", back_populates="batch")


class BatchError(Base):
    __tablename__ = "batch_errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    batch_id = Column(String(36), ForeignKey("batches.id"), nullable=False)
    filename = Column(String, nullable=False)
    error_reason = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    batch = relationship("Batch", back_populates="errors")
