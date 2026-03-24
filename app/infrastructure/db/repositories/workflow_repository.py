from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.workflow import Workflow as DomainWorkflow
from app.domain.repositories.workflow_repository import WorkflowRepository
from app.infrastructure.db.models.workflow import Workflows
from app.infrastructure.db.repositories.base_repository import BaseRepository
from app.infrastructure.db.utils import model_to_domain


class WorkflowRepositoryORM(BaseRepository, WorkflowRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, model_cls=Workflows, domain_cls=DomainWorkflow)

    async def add(self, workflow: DomainWorkflow) -> DomainWorkflow:
        return await self.create(workflow, id_field="workflow_id")

    async def deactivate_active_by_category(self, category_id: int) -> None:
        stmt = (
            update(Workflows)
            .where(Workflows.category_id == category_id, Workflows.is_active == True)
            .values(is_active=False)
        )
        await self.session.execute(stmt)
        await self.session.commit()
