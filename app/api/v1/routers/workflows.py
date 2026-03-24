from fastapi import APIRouter, Depends, status, Request

from app.api.dependencies.db import get_async_db
from app.api.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.application.dtos.workflow import CreateWorkflowInputDTO, WorkflowOutputDTO
from app.application.use_cases.workflow import AddWorkflowUseCase
from app.infrastructure.db.repositories.workflow_repository import WorkflowRepositoryORM

router = APIRouter()


@router.post("/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(payload: WorkflowCreate, db=Depends(get_async_db)):
    input_dto = CreateWorkflowInputDTO(**payload.model_dump()) #.from_schema(payload)

    repository = WorkflowRepositoryORM(db)
    use_case = AddWorkflowUseCase(repository)

    domain_workflow = await use_case.execute(input_dto)
    output_dto = WorkflowOutputDTO(**vars(domain_workflow)) #.from_domain(domain_workflow)

    return WorkflowResponse.model_validate(output_dto, from_attributes=True)

