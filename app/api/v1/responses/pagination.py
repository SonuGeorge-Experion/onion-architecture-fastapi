"""Standard paginated response model for list API endpoints."""

from pydantic import BaseModel, Field


class PaginationMeta(BaseModel):
    """Metadata describing the current pagination state."""

    total: int = Field(..., description="Total number of items across all pages.")
    page: int = Field(..., description="Current page number (1-indexed).")
    per_page: int = Field(..., description="Maximum items per page.")
    total_pages: int = Field(..., description="Total number of pages.")


class PaginatedResponse[T](BaseModel):
    """Wrapper for paginated list responses.

    Usage:
        PaginatedResponse[DonorResponse](
            message="Donors fetched successfully",
            data=donor_list,
            pagination=PaginationMeta(
                total=100,
                page=1,
                per_page=20,
                total_pages=5,
            ),
        )
    """

    success: bool = Field(
        default=True, description="Indicates the request was successful."
    )
    message: str = Field(..., description="Human-readable success message.")
    data: list[T] = Field(
        default_factory=list, description="List of items for the current page."
    )
    pagination: PaginationMeta = Field(..., description="Pagination metadata.")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "message": "message",
                "data": [],
                "pagination": {"total": 2, "page": 1, "per_page": 1, "total_pages": 2},
            }
        }
