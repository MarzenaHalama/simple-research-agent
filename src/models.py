from pydantic import BaseModel, Field
from enum import Enum


class ResearchStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ResearchRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=2000, description="Research question")


class IterationUpdate(BaseModel):
    iteration: int
    total: int
    text: str
    finished: bool


class ResearchResponse(BaseModel):
    status: ResearchStatus
    iterations_used: int
    result: str


class ErrorResponse(BaseModel):
    detail: str
