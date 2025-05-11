from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.entities.project_entity import Project, ProjectStatus
from app.domain.repositories.project_repository import AbstractProjectRepository
from app.domain.common.logger import AbstractLogger
from app.infrastructure.db.models.project_model import ProjectModel, ProjectStatusEnum


class PostgresqlProjectRepository(AbstractProjectRepository):
    def __init__(self, session: AsyncSession, logger: AbstractLogger) -> None:
        self.session = session
        self.logger = logger

    async def create(self, project: Project) -> None:
        self.logger.debug(f"Creating project: {project}")
        db_project = ProjectModel(
            id=project.id,
            client_id=project.client_id,
            title=project.title,
            description=project.description,
            status=ProjectStatusEnum(project.status.value),
            created_at=project.created_at,
            updated_at=project.updated_at,
        )
        self.session.add(db_project)
        await self.session.commit()
        self.logger.info(f"Project created with ID: {project.id}")

    async def get_by_id(self, project_id: UUID) -> Optional[Project]:
        self.logger.debug(f"Fetching project by ID: {project_id}")
        result = await self.session.execute(select(ProjectModel).where(ProjectModel.id == project_id))
        record = result.scalar_one_or_none()
        if record:
            self.logger.info(f"Project found with ID: {project_id}")
        else:
            self.logger.warning(f"Project not found with ID: {project_id}")
        return self._to_entity(record) if record else None

    async def update(self, project: Project) -> None:
        self.logger.debug(f"Updating project: {project}")
        result = await self.session.execute(select(ProjectModel).where(ProjectModel.id == project.id))
        db_project = result.scalar_one_or_none()
        if db_project:
            db_project.title = project.title
            db_project.description = project.description
            db_project.status = ProjectStatusEnum(project.status.value)
            db_project.updated_at = project.updated_at
            await self.session.commit()
            self.logger.info(f"Project updated with ID: {project.id}")
        else:
            self.logger.warning(f"Project not found for update: {project.id}")

    async def delete(self, project_id: UUID) -> None:
        self.logger.debug(f"Deleting project with ID: {project_id}")
        result = await self.session.execute(select(ProjectModel).where(ProjectModel.id == project_id))
        db_project = result.scalar_one_or_none()
        if db_project:
            await self.session.delete(db_project)
            await self.session.commit()
            self.logger.info(f"Project deleted with ID: {project_id}")
        else:
            self.logger.warning(f"Project not found for delete: {project_id}")

    async def list_by_client(self, client_id: UUID) -> List[Project]:
        self.logger.debug(f"Listing projects by client_id: {client_id}")
        result = await self.session.execute(select(ProjectModel).where(ProjectModel.client_id == client_id))
        records = result.scalars().all()
        return [self._to_entity(project) for project in records]

    def _to_entity(self, model: ProjectModel) -> Project:
        return Project(
            id=model.id,
            client_id=model.client_id,
            title=model.title,
            description=model.description,
            status=ProjectStatus(model.status.value),
            created_at=model.created_at,
            updated_at=model.updated_at
        )
