from abc import ABC, abstractmethod

from app.domain.entities.donor import Donor


class DonorRepository(ABC):
    @abstractmethod
    async def add(self, donor: Donor) -> Donor:
        raise NotImplementedError

    @abstractmethod
    async def list(
        self,
        filters: dict | None = None,
        search: str | None = None,
        order_by: str | None = None,
        order_dir: str = "asc",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[Donor], int]:
        """Return a tuple of (items, total_count)."""
        raise NotImplementedError
    
    @abstractmethod
    async def exists_by_znumber(self, znumber: int) -> bool:
        raise NotImplementedError
