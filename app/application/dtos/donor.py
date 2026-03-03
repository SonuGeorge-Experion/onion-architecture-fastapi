from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class DonorDTO(BaseModel):
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)


class DonorListDTO(BaseModel):
    items: List[DonorDTO]
    total: int
    page: int
    per_page: int

    model_config = ConfigDict(from_attributes=True)
