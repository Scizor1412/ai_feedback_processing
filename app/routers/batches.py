import io
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.batch import Batch, BatchError, BatchStatus, FeedbackType
from app.models.extraction import Extraction, EntityType, Sentiment
from app.models.feedback import Feedback
from app.services.csv_export import generate_csv
from app.services.entities import ALL_ENTITIES
from app.services.extraction import run_extraction
from app.services.ingestion import walk_and_ingest

router = APIRouter(tags=["batches"])
templates = Jinja2Templates(directory="app/templates")


# ── UI routes ─────────────────────────────────────────────────────────────────

@router.get("/")
def trigger_form(request: Request, db: Session = Depends(get_db)):
    batches = db.query(Batch).order_by(Batch.created_at.desc()).limit(10).all()
    return templates.TemplateResponse("batches/trigger.html", {"request": request, "batches": batches})


@router.get("/batches/{batch_id}/review")
def review_page(batch_id: str, request: Request, reviewed: bool = False, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    # Aggregate extractions per entity
    rows = (
        db.query(
            Extraction.entity_id,
            Extraction.entity_type,
            Extraction.sentiment,
            func.count().label("cnt"),
        )
        .filter(Extraction.batch_id == batch_id)
        .group_by(Extraction.entity_id, Extraction.entity_type, Extraction.sentiment)
        .all()
    )

    entity_map: dict[str, dict] = {}
    for row in rows:
        eid = row.entity_id
        if eid not in entity_map:
            name, _ = ALL_ENTITIES.get(eid, (eid, ""))
            entity_map[eid] = {
                "entity_id": eid,
                "entity_name": name,
                "entity_type": row.entity_type.value,
                "pos_count": 0,
                "neg_count": 0,
            }
        if row.sentiment == Sentiment.POSITIVE:
            entity_map[eid]["pos_count"] += row.cnt
        else:
            entity_map[eid]["neg_count"] += row.cnt

    recipients = sorted(entity_map.values(), key=lambda x: x["pos_count"] + x["neg_count"], reverse=True)
    total_extractions = sum(r["pos_count"] + r["neg_count"] for r in recipients)

    return templates.TemplateResponse("batches/review.html", {
        "request": request,
        "batch": batch,
        "recipients": recipients,
        "total_extractions": total_extractions,
        "reviewed": reviewed,
    })


@router.get("/batches/{batch_id}/recipients/{entity_id}/preview")
def preview_mentions(batch_id: str, entity_id: str, request: Request, db: Session = Depends(get_db)):
    def _fetch(sentiment: Sentiment):
        return (
            db.query(Feedback.feedback_id, Extraction.source_question, Extraction.source_answer)
            .join(Extraction, Extraction.feedback_id == Feedback.id)
            .filter(Extraction.batch_id == batch_id, Extraction.entity_id == entity_id.upper(), Extraction.sentiment == sentiment)
            .all()
        )

    return templates.TemplateResponse("batches/preview.html", {
        "request": request,
        "positives": _fetch(Sentiment.POSITIVE),
        "negatives": _fetch(Sentiment.NEGATIVE),
    })


# ── Action routes ─────────────────────────────────────────────────────────────


@router.post("/batches")
async def create_batch(request: Request, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        body = await request.json()
        folder_path = body.get("folder_path", "")
        feedback_type_str = body.get("feedback_type", "MID_TERM")
        is_form = False
    else:
        form = await request.form()
        folder_path = str(form.get("folder_path", ""))
        feedback_type_str = str(form.get("feedback_type", "MID_TERM"))
        is_form = True

    if not Path(folder_path).is_dir():
        if is_form:
            batches = db.query(Batch).order_by(Batch.created_at.desc()).limit(10).all()
            return templates.TemplateResponse("batches/trigger.html", {
                "request": request, "batches": batches,
                "error": f"Folder not found: {folder_path}",
            }, status_code=400)
        raise HTTPException(status_code=400, detail=f"Folder not found: {folder_path}")

    batch = Batch(feedback_type=FeedbackType(feedback_type_str), folder_path=folder_path)
    db.add(batch)
    db.commit()
    db.refresh(batch)

    background_tasks.add_task(walk_and_ingest, batch.id, folder_path)

    if is_form:
        return RedirectResponse(url=f"/batches/{batch.id}/review", status_code=303)
    return {"batch_id": batch.id, "status": batch.status}


@router.post("/batches/{batch_id}/extract")
def trigger_extraction(batch_id: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    if batch.status not in (BatchStatus.COMPLETE, BatchStatus.EXTRACTED):
        raise HTTPException(status_code=400, detail=f"Batch status is {batch.status}, expected complete")

    background_tasks.add_task(run_extraction, batch_id)
    return RedirectResponse(url=f"/batches/{batch_id}/review", status_code=303)


@router.post("/batches/{batch_id}/mark-reviewed")
def mark_reviewed(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    batch.status = BatchStatus.REVIEWED
    db.commit()
    return RedirectResponse(url=f"/batches/{batch_id}/review?reviewed=true", status_code=303)


# ── CSV download routes ────────────────────────────────────────────────────────

@router.get("/batches/{batch_id}/recipients/{entity_id}/csv/positive")
def csv_positive(batch_id: str, entity_id: str, db: Session = Depends(get_db)):
    buf = generate_csv(db, batch_id, entity_id, Sentiment.POSITIVE)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv",
                              headers={"Content-Disposition": f"attachment; filename={entity_id}_positive.csv"})


@router.get("/batches/{batch_id}/recipients/{entity_id}/csv/negative")
def csv_negative(batch_id: str, entity_id: str, db: Session = Depends(get_db)):
    buf = generate_csv(db, batch_id, entity_id, Sentiment.NEGATIVE)
    return StreamingResponse(iter([buf.getvalue()]), media_type="text/csv",
                              headers={"Content-Disposition": f"attachment; filename={entity_id}_negative.csv"})


# ── Status/debug routes ────────────────────────────────────────────────────────

@router.get("/batches/{batch_id}/status")
def get_status(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {"batch_id": batch.id, "status": batch.status,
            "total_files": batch.total_files,
            "successful_count": batch.successful_count,
            "failed_count": batch.failed_count}


@router.get("/batches/{batch_id}/errors")
def get_errors(batch_id: str, db: Session = Depends(get_db)):
    batch = db.get(Batch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    errors = db.query(BatchError).filter(BatchError.batch_id == batch_id).all()
    return [{"filename": e.filename, "reason": e.error_reason} for e in errors]
