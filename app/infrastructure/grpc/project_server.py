import grpc
from uuid import UUID
from app.generated.project import project_pb2_grpc, project_pb2
from app.domain.repositories.project_repository import AbstractProjectRepository
from app.domain.common.logger import AbstractLogger
from app.domain.exceptions import ProjectNotFound


class ProjectServiceHandler(project_pb2_grpc.ProjectServiceServicer):
    def __init__(self, project_repo: AbstractProjectRepository, logger: AbstractLogger):
        self.project_repo = project_repo
        self.logger = logger

    async def GetProjectById(self, request, context):
        try:
            project_id = UUID(request.project_id)
            project = await self.project_repo.get_by_id(project_id)

            if project is None:
                self.logger.warning(f"Project not found: {project_id}")
                return await context.abort(grpc.StatusCode.NOT_FOUND, "Project not found")

            self.logger.info(f"✅ gRPC sending project: {project.id}")
            return project_pb2.ProjectResponse(
                project_id=str(project.id),
                client_id=str(project.client_id),
                status=project.status.value,
            )
        except ProjectNotFound as e:
            self.logger.warning(f"ProjectNotFound exception: {e}")
            return await context.abort(grpc.StatusCode.NOT_FOUND, str(e))

        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return await context.abort(grpc.StatusCode.INTERNAL, "Internal server error")
