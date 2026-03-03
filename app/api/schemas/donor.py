from typing import Any, Dict, Optional

from pydantic import BaseModel


class DonorCreate(BaseModel):
    znumber: Optional[int] = None
    name: str
    age: Optional[int] = None
    region: Optional[str] = None
    other_factors: Optional[Dict[str, Any]] = None
