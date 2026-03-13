from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.domain.value_objects.znumber import ZNumber


@dataclass
class Donor:
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]

    @classmethod
    def create(
        cls,
        donor_id: Optional[int],
        znumber: Optional[int],
        name: str,
        age: Optional[int],
        region: Optional[str],
        other_factors: Optional[Dict[str, Any]],
    ) -> "Donor":

        return cls(
            donor_id=donor_id,
            znumber=ZNumber(znumber),
            name=name,
            age=age,
            region=region,
            other_factors=other_factors or {},
        )
