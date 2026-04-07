"""Standard error response models for all API endpoints."""

from typing import Any

from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    """Structured error information returned inside an error response.

    Attributes:
        code: Machine-readable error code (e.g. ``USER_NOT_FOUND``,
            ``VALIDATION_ERROR``).
        type: Exception class name or error category (e.g. ``DomainException``).
        message: Human-readable error description.
        details: Optional extra context – validation field errors, debug info, etc.
    """

    code: str = Field(..., description="Machine-readable error code.")
    type: str | None = Field(
        default=None, description="Error category or exception class name."
    )
    message: str = Field(..., description="Human-readable error description.")
    details: list[Any] | Any | None = Field(
        default=None,
        description="Additional error context such as validation field errors.",
    )


class ErrorResponse(BaseModel):
    """Wrapper for all error API responses.

    Usage:
        # Domain error
        ErrorResponse(
            error=ErrorDetail(
                code="USER_NOT_FOUND",
                type="DomainException",
                message="User does not exist",
            )
        )

        # Validation error with field details
        ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                type="RequestValidationError",
                message="Invalid request data",
                details=[
                    {"loc": ["body", "email"], "msg": "field required",
                    "type": "value_error"}
                ],
            )
        )
    """

    success: bool = Field(
        default=False, description="Always False for error responses."
    )
    error: ErrorDetail = Field(..., description="Structured error information.")
