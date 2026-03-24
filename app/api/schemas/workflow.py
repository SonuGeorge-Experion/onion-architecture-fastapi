from typing import Any, Dict, Optional

from pydantic import BaseModel, ConfigDict


class WorkflowCreate(BaseModel):
    category_id: Optional[int]
    type: Optional[str] = None
    name: str
    template_json: Optional[Dict[str, Any]] = None
    version: Optional[str]
    is_active: Optional[bool] = True


class WorkflowResponse(BaseModel):
    workflow_id: Optional[int]
    category_id: Optional[int]
    type: Optional[str]
    name: Optional[str]
    template_json: Optional[Dict[str, Any]]
    version: Optional[str]
    is_active: Optional[bool]

    model_config = ConfigDict(from_attributes=True)
