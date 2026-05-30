from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.batch import FeedbackType


class FeedbackPersona(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    role: str


class FeedbackMetadata(BaseModel):
    feedback_id: str
    date: str
    type: FeedbackType
    persona: FeedbackPersona
    related_schools: list[str]
    related_services: list[str]
    overall_sentiment: str


class FeedbackSchema(BaseModel):
    metadata: FeedbackMetadata
    body: list[dict[str, Any]]
