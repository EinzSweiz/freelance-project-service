from fastapi import APIRouter, Depends, Request
from uuid import UUID
from typing import Annotated, List

from app.presentation.schemas.project_schemas import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectResponse,
)
from app.services.project_service import ProjectService
from app.services.dependencies import get_project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(
    request: Request,
    data: ProjectCreateRequest,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    user_id = request.state.user_id
    project = await service.create_project(
        client_id=UUID(user_id),
        title=data.title,
        description=data.description
    )
    return ProjectResponse(**project.to_dict())


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: UUID,
    data: ProjectUpdateRequest,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    project = await service.update_project(
        project_id=project_id,
        title=data.title,
        description=data.description
    )
    return ProjectResponse(**project.to_dict())


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    project = await service.get_project(project_id)
    return ProjectResponse(**project.to_dict())


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    await service.delete_project(project_id)
    return


@router.get("/client/{client_id}", response_model=List[ProjectResponse])
async def list_client_projects(
    client_id: UUID,
    service: Annotated[ProjectService, Depends(get_project_service)]
):
    projects = await service.list_projects_by_client(client_id)
    return [ProjectResponse(**p.to_dict()) for p in projects]
