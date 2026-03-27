from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies.db import get_async_db
from app.api.schemas.workflow import WorkflowCreate, WorkflowResponse
from app.application.dtos.workflow import CreateWorkflowInputDTO, WorkflowOutputDTO
from app.application.use_cases.workflow import (
    AddWorkflowUseCase,
    GetWorkflowsByCategoryUseCase,
)
from app.infrastructure.db.repositories.workflow_repository import WorkflowRepositoryORM

router = APIRouter()


@router.get("/workflows", response_model=list[WorkflowResponse])
async def get_workflows_by_category(
    category_id: int | None = None, db=Depends(get_async_db)
):
    filter_desc = f"category {category_id}" if category_id else "any category"

    repo = WorkflowRepositoryORM(db)
    use_case = GetWorkflowsByCategoryUseCase(repo)

    result = await use_case.execute(category_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No workflows found for {filter_desc}",
        )

    return result


@router.post(
    "/workflows", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED
)
async def create_workflow(payload: WorkflowCreate, db=Depends(get_async_db)):
    input_dto = CreateWorkflowInputDTO(**payload.model_dump())

    repository = WorkflowRepositoryORM(db)
    use_case = AddWorkflowUseCase(repository)

    domain_workflow = await use_case.execute(input_dto)
    output_dto = WorkflowOutputDTO(**vars(domain_workflow))

    return WorkflowResponse.model_validate(output_dto, from_attributes=True)
