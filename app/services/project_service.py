from app.domain.repositories.project_repository import AbstractProjectRepository
from app.domain.entities.project_entity import Project, ProjectStatus
from app.domain.common.logger import AbstractLogger
from app.domain.exceptions import ProjectNotFound
from app.infrastructure.kafka.kafka_producer import KafkaProducer
from app.config.kafka_config import KAFKA_TOPICS
from datetime import datetime
from uuid import UUID


class ProjectService:
    def __init__(self, project_repo: AbstractProjectRepository, logger: AbstractLogger, kafka_producer: KafkaProducer):
        self.project_repo = project_repo
        self.logger = logger
        self.kafka_producer = kafka_producer

    async def create_project(self, client_id: UUID, title: str, description: str) -> Project:
        project = Project.create(client_id=client_id, title=title, description=description)
        await self.project_repo.create(project)
        self.logger.info(f"Project created: {project}")

        await self.kafka_producer.send(
            topic=KAFKA_TOPICS["project_created"],
            event={
                "project_id": str(project.id),
                "client_id": str(project.client_id),
                "title": project.title,
                "timestamp": datetime.now().isoformat()
            }
        )
        return project

    async def update_project(self, project_id: UUID, title: str, description: str) -> Project:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            self.logger.warning(f"Project not found for update: {project_id}")
            raise ProjectNotFound(f"Project {project_id} not found")

        project.update(title, description)
        await self.project_repo.update(project)

        await self.kafka_producer.send(
            topic=KAFKA_TOPICS["project_updated"],
            event={
                "project_id": str(project.id),
                "title": project.title,
                "timestamp": datetime.now().isoformat()
            }
        )

        return project

    async def delete_project(self, project_id: UUID) -> None:
        await self.project_repo.delete(project_id)
        self.logger.info(f"Project deleted: {project_id}")
        await self.kafka_producer.send(
            topic=KAFKA_TOPICS["project_deleted"],
            event={
                "project_id": str(project_id),
                "timestamp": datetime.now().isoformat()
            }
        )

    async def get_project(self, project_id: UUID) -> Project:
        project = await self.project_repo.get_by_id(project_id)
        if not project:
            raise ProjectNotFound(f"Project {project_id} not found")
        return project

    async def list_projects_by_client(self, client_id: UUID) -> list[Project]:
        return await self.project_repo.list_by_client(client_id)
