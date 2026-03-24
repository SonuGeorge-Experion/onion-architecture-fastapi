# import logging
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger
from app.domain.exceptions import DomainException, DuplicateZNumberException

# from application.exceptions import UseCaseException

logger = get_logger(__name__)


def register_exception_handlers(app):

    # Domain → 400
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        if isinstance(exc, DuplicateZNumberException):
            status_code = status.HTTP_409_CONFLICT
            level = "warning"
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            level = "warning"

        # Log known domain exceptions without traceback (warning level)
        logger.warning(
            "Domain exception",
            extra={
                "error_type": exc.__class__.__name__,
                "error_message": str(exc),
                "path": request.url.path,
                "method": request.method,
                "status_code": status_code,
            },
        )

        return JSONResponse(
            status_code=status_code,
            content={
                "error_type": exc.__class__.__name__,
                "error_message": str(exc),
            },
        )

    # Request validation errors → 422, log with details
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.warning(
            "Request validation error",
            extra={
                "errors": exc.errors(),
                "path": request.url.path,
                "method": request.method,
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
        )

    # Preserve HTTPException
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "HTTPException",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": request.url.path,
                "method": request.method,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # Catch-all 500
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        # Log with traceback for unexpected errors
        logger.exception(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_type": exc.__class__.__name__,
                "error_message": "An unexpected error occurred.",
            },
        )
