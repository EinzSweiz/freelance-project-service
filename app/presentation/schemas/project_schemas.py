from pydantic import BaseModel, Field
from uuid import UUID
from enum import Enum
from datetime import datetime


class ProjectStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectCreateRequest(BaseModel):
    title: str = Field(..., min_length=3)
    description: str


class ProjectUpdateRequest(BaseModel):
    title: str
    description: str


class ProjectResponse(BaseModel):
    id: UUID
    client_id: UUID
    title: str
    description: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
