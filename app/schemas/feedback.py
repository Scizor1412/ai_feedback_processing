from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.batch import FeedbackType


class StudentPersona(BaseModel):
    """Persona shape for MID_TERM and YEAR_END feedback."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    role: str


class ParentPersona(BaseModel):
    """Persona shape for PARENTS feedback."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str
    role: str
    child_name: str


class EmployerPersona(BaseModel):
    """Persona shape for INTERNSHIP feedback — evaluator/intern pair, no plain `name`."""

    model_config = ConfigDict(extra="allow")

    id: str
    role: str
    evaluator_name: str
    intern_name: str


PERSONA_SCHEMA_BY_TYPE: dict[FeedbackType, type[BaseModel]] = {
    FeedbackType.MID_TERM: StudentPersona,
    FeedbackType.YEAR_END: StudentPersona,
    FeedbackType.PARENTS: ParentPersona,
    FeedbackType.INTERNSHIP: EmployerPersona,
}


class FeedbackMetadata(BaseModel):
    feedback_id: str
    date: str
    type: FeedbackType
    persona: dict[str, Any]
    related_schools: list[str]
    related_services: list[str]
    overall_sentiment: str

    @model_validator(mode="after")
    def validate_persona_shape(self) -> "FeedbackMetadata":
        schema = PERSONA_SCHEMA_BY_TYPE[self.type]
        validated = schema.model_validate(self.persona)
        self.persona = validated.model_dump()
        return self


class FeedbackSchema(BaseModel):
    metadata: FeedbackMetadata
    body: list[dict[str, Any]]
