from typing import Any, Dict, Optional

from app.application.dtos.donor import DonorDTO, DonorListDTO
from app.core.logging import get_logger
from app.domain.entities.donor import Donor as DomainDonor
from app.domain.repositories.donor_repository import DonorRepository


class AddDonorUseCase:
    def __init__(self, repository: DonorRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, data: Dict[str, Any]) -> DonorDTO:
        """Create a donor from a mapping of fields.

        Accepting a single mapping scales to large tables and keeps the
        callsite simple (pass `payload.model_dump()`). The mapping is used to
        construct the domain entity and passed to the repository.
        """
        self.logger.debug("AddDonorUseCase called", extra={"payload_keys": list(data.keys())})
        domain_donor = DomainDonor(donor_id=None, **data)
        created = await self.repository.add(domain_donor)
        self.logger.info("Donor created", extra={"donor_id": created.donor_id, "znumber": created.znumber})
        return DonorDTO(**created.__dict__)


class ListDonorsUseCase:
    def __init__(self, repository: DonorRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(
        self,
        filters: Optional[Dict[str, Any]] = None,
        search: Optional[str] = None,
        order_by: Optional[str] = None,
        order_dir: str = "asc",
        page: int = 1,
        per_page: int = 20,
    ) -> DonorListDTO:
        self.logger.debug("ListDonorsUseCase called", extra={"filters": filters, "search": search, "order_by": order_by, "order_dir": order_dir, "page": page, "per_page": per_page})
        items, total = await self.repository.list(
            filters=filters,
            search=search,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            per_page=per_page,
        )
        self.logger.info("Donors listed", extra={"count": len(items), "total": total, "page": page})

        return DonorListDTO(
            items=[DonorDTO(**d.__dict__) for d in items],
            total=total,
            page=page,
            per_page=per_page,
        )
