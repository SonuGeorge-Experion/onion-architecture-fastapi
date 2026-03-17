from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class DonorCreate(BaseModel):
    znumber: Optional[int] = None
    name: str
    age: Optional[int] = None
    region: Optional[str] = None
    other_factors: Optional[Dict[str, Any]] = None


class DonorResponse(BaseModel):
    """Response schema for a single donor (API boundary)."""
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)


class DonorListResponse(BaseModel):
    """Response schema for paginated donor list (API boundary)."""
    items: List[DonorResponse]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
