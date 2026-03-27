from abc import ABC, abstractmethod

from app.domain.entities.workflow import Workflow


class WorkflowRepository(ABC):
    @abstractmethod
    async def add(self, workflow: Workflow) -> Workflow:
        raise NotImplementedError

    @abstractmethod
    async def deactivate_active_by_category(self, category_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_by_category_id(
        self, category_id: int | None = None
    ) -> list[Workflow] | None:
        raise NotImplementedError
