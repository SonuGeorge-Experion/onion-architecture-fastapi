"""Standard success response model for all API endpoints."""

from pydantic import BaseModel, Field


class SuccessResponse[T](BaseModel):
    """Wrapper for all successful API responses.

    Usage:
        # Single item
        SuccessResponse[DonorResponse](
            message="Donor fetched successfully",
            data=donor,
        )

        # No data (e.g., delete confirmation)
        SuccessResponse(
            message="Donor deleted successfully",
        )
    """

    success: bool = Field(
        default=True, description="Indicates the request was successful."
    )
    message: str = Field(..., description="Human-readable success message.")
    data: T | None = Field(default=None, description="Response payload.")
