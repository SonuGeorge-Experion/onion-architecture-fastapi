from typing import Optional

from app.application.dtos.process import DonorProcessDetailsDTO
from app.core.logging import get_logger
from app.domain.repositories.process_repository import ProcessRepository


class GetProcessByDonorUseCase:
    def __init__(self, repository: ProcessRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, donor_id: int) -> Optional[DonorProcessDetailsDTO]:
        self.logger.debug(
            "GetProcessByDonorUseCase called", extra={"donor_id": donor_id}
        )
        domain_donor_details = await self.repository.get_process_by_donor(donor_id)

        if not domain_donor_details:
            self.logger.info("Donor not found", extra={"donor_id": donor_id})
            return None

        self.logger.info(
            "Donor process details retrieved", extra={"donor_id": donor_id}
        )
        return DonorProcessDetailsDTO(**domain_donor_details.__dict__)
