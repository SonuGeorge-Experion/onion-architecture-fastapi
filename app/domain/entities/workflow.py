from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Workflow:
    workflow_id: Optional[int]
    category_id: Optional[int]
    type: Optional[str]
    name: Optional[str]
    template_json: Optional[Dict[str, Any]]
    version: Optional[str]
    is_active: Optional[bool]

    @classmethod
    def create(
        cls,
        workflow_id: Optional[int],
        category_id: Optional[int],
        type: Optional[str],
        name: Optional[str],
        template_json: Optional[Dict[str, Any]],
        version: Optional[str],
        is_active: Optional[bool] = True,
    ) -> "Workflow":
        return cls(
            workflow_id=workflow_id,
            category_id=category_id,
            type=type,
            name=name,
            template_json=template_json or {},
            version=version,
            is_active=is_active if is_active is not None else True,
        )
