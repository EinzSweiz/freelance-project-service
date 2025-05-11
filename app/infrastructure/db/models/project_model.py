import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from uuid import uuid4
from enum import Enum
from datetime import datetime
from app.infrastructure.db.db_session import Base


class ProjectStatusEnum(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProjectModel(Base):
    __tablename__ = "projects"

    id = sa.Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    client_id = sa.Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    title = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    status = sa.Column(sa.Enum(ProjectStatusEnum), nullable=False, default=ProjectStatusEnum.OPEN)
    created_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
