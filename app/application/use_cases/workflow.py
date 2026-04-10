from app.api.schemas.workflow import WorkflowResponse
from app.application.dtos.workflow import CreateWorkflowInputDTO
from app.core.logging import get_logger
from app.domain.entities.workflow import Workflow as DomainWorkflow
from app.domain.repositories.workflow_repository import WorkflowRepository


class AddWorkflowUseCase:
    def __init__(self, repository: WorkflowRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, input_dto: CreateWorkflowInputDTO) -> DomainWorkflow:
        """Create a workflow from input DTO.

        When creating a new workflow, deactivates all existing active workflows
        with the same category_id by setting their is_active to false.

        Returns the domain entity directly. Conversion to output DTO
        is the responsibility of the caller (typically the router/API layer).
        """
        self.logger.debug(
            "AddWorkflowUseCase called",
            extra={
                "category_id": input_dto.category_id,
                "workflow_name": input_dto.name,
            },
        )

        if input_dto.category_id is not None:
            await self.repository.deactivate_active_by_category(input_dto.category_id)

        domain_workflow = DomainWorkflow.create(workflow_id=None, **vars(input_dto))

        created = await self.repository.add(domain_workflow)

        self.logger.info(
            "Workflow created",
            extra={
                "workflow_id": created.workflow_id,
                "category_id": created.category_id,
            },
        )
        return created


class GetWorkflowsByCategoryUseCase:
    def __init__(self, repository: WorkflowRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(
        self, category_id: int | None = None
    ) -> list[DomainWorkflow] | None:
        filter_desc = f"category {category_id}" if category_id else "all categories"

        self.logger.debug(
            "GetWorkflowsByCategoryUseCase called", extra={"category_id": category_id}
        )
        workflows = await self.repository.get_by_category_id(category_id)

        if not workflows:
            self.logger.info("No workflows found", extra={"filter": filter_desc})
            return None

        self.logger.info(
            "Workflows retrieved",
            extra={"filter": filter_desc, "count": len(workflows)},
        )
        return [self._to_response(w) for w in workflows]

    def _to_response(self, w: DomainWorkflow) -> WorkflowResponse:
        return WorkflowResponse.model_construct(
            workflow_id=w.workflow_id,
            name=w.name,
            template_json=w.template_json,
            version=w.version,
            is_active=w.is_active,
        )
# sample