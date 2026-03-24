from dataclasses import dataclass
from typing import Any, Dict, Optional, Self

from app.api.schemas.workflow import WorkflowCreate
from app.domain.entities.workflow import Workflow


@dataclass
class CreateWorkflowInputDTO:
    category_id: Optional[int]
    type: Optional[str]
    name: str
    template_json: Optional[Dict[str, Any]]
    version: Optional[str]
    is_active: Optional[bool] = True

    @staticmethod
    def from_schema(schema: WorkflowCreate) -> Self:
        return CreateWorkflowInputDTO(
            category_id=schema.category_id,
            type=schema.type,
            name=schema.name,
            template_json=schema.template_json,
            version=schema.version,
            is_active=schema.is_active,
        )


@dataclass
class WorkflowOutputDTO:
    workflow_id: Optional[int]
    category_id: Optional[int]
    type: Optional[str]
    name: Optional[str]
    template_json: Optional[Dict[str, Any]]
    version: Optional[str]
    is_active: Optional[bool]

    @staticmethod
    def from_domain(entity: Workflow) -> "WorkflowOutputDTO":
        return WorkflowOutputDTO(
            workflow_id=entity.workflow_id,
            category_id=entity.category_id,
            type=entity.type,
            name=entity.name,
            template_json=entity.template_json,
            version=entity.version,
            is_active=entity.is_active,
        )
