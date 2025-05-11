class ProjectServiceException(Exception):
    """Base class for all project-related exceptions."""
    pass


class ProjectNotFound(ProjectServiceException):
    """Raised when a project with a given ID is not found."""
    pass


class UnauthorizedProjectAccess(ProjectServiceException):
    """Raised when a user tries to access a project they don't own."""
    pass
