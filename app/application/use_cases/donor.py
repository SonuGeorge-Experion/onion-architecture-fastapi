from typing import Any, Dict, Optional

from app.application.dtos.donor import CreateDonorInputDTO, DonorListDTO
from app.core.logging import get_logger
from app.domain.entities.donor import Donor as DomainDonor
from app.domain.repositories.donor_repository import DonorRepository
from app.domain.services.donor_service import DonorService


class AddDonorUseCase:
    def __init__(self, repository: DonorRepository) -> None:
        self.repository = repository
        self.logger = get_logger(self.__class__.__name__)

    async def execute(self, input_dto: CreateDonorInputDTO) -> DomainDonor:
        """Create a donor from input DTO.

        Returns the domain entity directly. Conversion to output DTO
        is the responsibility of the caller (typically the router/API layer).
        """
        self.logger.debug(
            "AddDonorUseCase called",
            extra={"donor_name": input_dto.name, "znumber": input_dto.znumber},
        )

        # check for duplicate znumber before creating domain entity to avoid unnecessary DB transaction
        znumber = input_dto.znumber
        await DonorService().validate_unique_znumber(znumber, self.repository)
        # add donor
        domain_donor = DomainDonor.create(donor_id=None, **vars(input_dto))
        created = await self.repository.add(domain_donor)
        self.logger.info(
            "Donor created",
            extra={"donor_id": created.donor_id, "znumber": created.znumber},
        )
        return created


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
    ) -> tuple[list[DomainDonor], int]:
        """List donors with filtering, search, sorting, and pagination.

        Returns tuple of (domain entities list, total count).
        Conversion to output DTOs is the responsibility of the caller.
        """
        self.logger.debug(
            "ListDonorsUseCase called",
            extra={
                "filters": filters,
                "search": search,
                "order_by": order_by,
                "order_dir": order_dir,
                "page": page,
                "per_page": per_page,
            },
        )
        items, total = await self.repository.list(
            filters=filters,
            search=search,
            order_by=order_by,
            order_dir=order_dir,
            page=page,
            per_page=per_page,
        )
        self.logger.info(
            "Donors listed",
            extra={"count": len(items), "total": total, "page": page},
        )
        return items, total
