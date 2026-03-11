from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime
from decimal import Decimal


@dataclass
class WorkflowStep:
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


@dataclass
class Process:
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
    workflow_steps: List[WorkflowStep] = field(default_factory=list)


@dataclass
class Tissue:
    tissue_id: Optional[int]
    donor_id: Optional[int]
    category_id: Optional[int]
    bundle_details: Optional[Dict[str, Any]]
    status: Optional[str]
    created_at: Optional[datetime]
    processes: List[Process] = field(default_factory=list)


@dataclass
class DonorProcessDetails:
    donor_id: Optional[int]
    znumber: Optional[int]
    name: str
    age: Optional[int]
    region: Optional[str]
    other_factors: Optional[Dict[str, Any]]
    tissues: List[Tissue] = field(default_factory=list)
