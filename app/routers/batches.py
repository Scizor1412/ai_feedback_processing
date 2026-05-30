from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batch import Batch, BatchError, BatchStatus, FeedbackType
from app.models.feedback import Feedback
from app.services.ingestion import walk_and_ingest

router = APIRouter(prefix="/batches", tags=["batches"])


class CreateBatchRequest(BaseModel):
    folder_path: str
    feedback_type: FeedbackType


@router.post("", status_code=202)
def create_batch(
    request: CreateBatchRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    if not Path(request.folder_path).is_dir():
        raise HTTPException(status_code=400, detail=f"Folder not found: {request.folder_path}")

    batch = Batch(feedback_type=request.feedback_type, folder_path=request.folder_path)
    db.add(batch)
    db.commit()
    db.refresh(batch)

    background_tasks.add_task(walk_and_ingest, batch.id, request.folder_path)

    return {"batch_id": batch.id, "status": batch.status}


@router.get("/{batch_id}/status")
def get_batch_status(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {
        "batch_id": batch.id,
        "status": batch.status,
        "total_files": batch.total_files,
        "successful_count": batch.successful_count,
        "failed_count": batch.failed_count,
        "completed_at": batch.completed_at,
    }


@router.get("/{batch_id}/errors")
def get_batch_errors(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    errors = db.query(BatchError).filter(BatchError.batch_id == batch_id).all()
    return [{"filename": e.filename, "reason": e.error_reason} for e in errors]
