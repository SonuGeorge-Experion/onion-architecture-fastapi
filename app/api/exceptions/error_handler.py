# import logging
from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.responses.error import ErrorDetail, ErrorResponse
from app.core.logging import get_logger
from app.domain.exceptions import DomainException, DuplicateZNumberException

logger = get_logger(__name__)


def register_exception_handlers(app):

    # Domain → 400
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        if isinstance(exc, DuplicateZNumberException):
            status_code = status.HTTP_409_CONFLICT
            # level = "warning"
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            # level = "warning"

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

        error_response = ErrorResponse(
            error=ErrorDetail(
                code="DOMAIN_ERROR",
                type=exc.__class__.__name__,
                message=str(exc),
            )
        )

        return JSONResponse(
            status_code=status_code,
            content=error_response.model_dump(),
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

        error_response = ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                type="RequestValidationError",
                message="Invalid request data",
                details=exc.errors(),
            )
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.model_dump(),
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

        error_response = ErrorResponse(
            error=ErrorDetail(
                code="HTTP_ERROR",
                type="HTTPException",
                message=str(exc.detail),
            )
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.model_dump(),
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

        error_response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                type=exc.__class__.__name__,
                message="An unexpected error occurred.",
            )
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.model_dump(),
        )
