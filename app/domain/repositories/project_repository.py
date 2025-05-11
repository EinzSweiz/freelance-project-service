from abc import ABC, abstractmethod
from uuid import UUID
from typing import List
from app.domain.entities.project_entity import Project


class AbstractProjectRepository(ABC):
    @abstractmethod
    async def create(self, project: Project) -> None:
        """Create a new project in the database."""
        pass

    @abstractmethod
    async def get_by_id(self, project_id: UUID) -> Project:
        """Get project by its ID."""
        pass

    @abstractmethod
    async def update(self, project: Project) -> None:
        """Update a project."""
        pass

    @abstractmethod
    async def delete(self, project_id: UUID) -> None:
        """Delete a project by ID."""
        pass

    @abstractmethod
    async def list_by_client(self, client_id: UUID) -> List[Project]:
        """List all projects belonging to a client."""
        pass
