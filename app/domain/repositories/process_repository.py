from abc import ABC, abstractmethod

from app.domain.entities.process import DonorProcessDetails


class ProcessRepository(ABC):
    @abstractmethod
    async def get_process_by_donor(self, donor_id: int) -> DonorProcessDetails | None:
        raise NotImplementedError
