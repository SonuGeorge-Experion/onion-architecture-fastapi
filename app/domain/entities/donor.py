from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Donor:
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]
