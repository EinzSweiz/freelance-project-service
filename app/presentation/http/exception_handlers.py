from fastapi import Request
from fastapi.responses import JSONResponse
from app.domain.exceptions import ProjectNotFound, UnauthorizedProjectAccess


async def project_not_found(request: Request, exc: ProjectNotFound):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def unauthorized_project_access(request: Request, exc: UnauthorizedProjectAccess):
    return JSONResponse(status_code=401, content={"detail": str(exc)})

