from fastapi import FastAPI

import app.models  # register all models with Base before create_all
from app.database import Base, engine
from app.routers import batches

# MTP: create tables at startup (Alembic migrations added pre-MVP)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Feedback Process", version="0.1.0")

app.include_router(batches.router)


@app.get("/health")
def health():
    return {"status": "ok"}
