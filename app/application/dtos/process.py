from typing import Any, Dict, List, Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.application.dtos.donor import DonorOutputDTO


class WorkflowStepDTO(BaseModel):
    step_id: Optional[int]
    process_id: Optional[int]
    step_num: Optional[int]
    initials: Optional[str]
    verified_by_initials: Optional[str]
    spin_program: Optional[str]
    spin_count: Optional[int]
    actual_duration: Optional[str]
    temp_start: Optional[Decimal]
    temp_stop: Optional[Decimal]
    temp_compliant: Optional[bool]
    na_performed: Optional[bool]
    deviation_notes: Optional[str]
    start_time: Optional[datetime]
    completed_at: Optional[datetime]
    step_data: Optional[Dict[str, Any]]
    device_id: Optional[str]
    client_timestamp: Optional[datetime]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class ProcessDTO(BaseModel):
    process_id: Optional[int]
    session_id: Optional[int]
    plan_id: Optional[int]
    workflow_id: Optional[int]
    template_snapshot: Optional[Dict[str, Any]]
    tissue_id: Optional[int]
    status: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    workflow_steps: List[WorkflowStepDTO] = []

    model_config = ConfigDict(from_attributes=True)


class TissueDTO(BaseModel):
    tissue_id: Optional[int]
    donor_id: Optional[int]
    category_id: Optional[int]
    bundle_details: Optional[Dict[str, Any]]
    status: Optional[str]
    created_at: Optional[datetime]
    processes: List[ProcessDTO] = []

    model_config = ConfigDict(from_attributes=True)


class DonorProcessDetailsDTO(DonorOutputDTO):
    tissues: List[TissueDTO] = []

    model_config = ConfigDict(from_attributes=True)
