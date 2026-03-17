from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Self

from app.api.schemas.donor import DonorCreate
from app.domain.entities.donor import Donor


@dataclass
class CreateDonorInputDTO:
    """Input DTO for creating a donor (application layer)."""
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]

    @staticmethod
    def from_schema(schema: DonorCreate) -> Self:
        """Convert API schema to input DTO."""
        return CreateDonorInputDTO(
            znumber=schema.znumber,
            name=schema.name,
            age=schema.age,
            region=schema.region,
            other_factors=schema.other_factors,
        )


@dataclass
class DonorOutputDTO:
    """Output DTO for returning donor data (application layer)."""
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]

    @staticmethod
    def from_domain(entity: Donor) -> Self:
        """Convert domain entity to output DTO."""
        return DonorOutputDTO(
            donor_id=entity.donor_id,
            znumber=entity.znumber,
            name=entity.name,
            age=entity.age,
            region=entity.region,
            other_factors=entity.other_factors,
        )


@dataclass
class DonorListDTO:
    """List DTO for returning paginated donor data."""
    items: List[DonorOutputDTO]
    total: int
    page: int
    per_page: int
