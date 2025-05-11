from dataclasses import dataclass
from enum import Enum
from uuid import uuid4, UUID
from datetime import datetime
from typing import Optional


class ProjectStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Project:
    id: UUID
    client_id: UUID
    title: str
    description: str
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

    @classmethod
    def create(cls, client_id: UUID, title: str, description: str) -> "Project":
        now = datetime.now()
        return cls(
            id=uuid4(),
            client_id=client_id,
            title=title,
            description=description,
            status=ProjectStatus.OPEN,
            created_at=now,
            updated_at=now
        )

    def update(self, title: str, description: str):
        self.title = title
        self.description = description
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "client_id": str(self.client_id),
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Project":
        return cls(
            id=UUID(data["id"]),
            client_id=UUID(data["client_id"]),
            title=data["title"],
            description=data["description"],
            status=ProjectStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
        )
