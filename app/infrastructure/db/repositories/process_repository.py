from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.domain.entities.process import (
    DonorProcessDetails,
    Process,
    Tissue,
    WorkflowStep,
)
from app.domain.repositories.process_repository import ProcessRepository
from app.infrastructure.db.models.donor import Donors
from app.infrastructure.db.models.process import Processes
from app.infrastructure.db.models.product import Tissues
from app.infrastructure.db.utils import model_to_domain


class ProcessRepositoryORM(ProcessRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_process_by_donor(self, donor_id: int) -> DonorProcessDetails | None:
        stmt = (
            select(Donors)
            .options(
                selectinload(Donors.tissues)
                .selectinload(Tissues.processes)
                .selectinload(Processes.workflow_steps)
            )
            .where(Donors.donor_id == donor_id)
        )
        res = await self.session.execute(stmt)
        donor = res.scalar_one_or_none()

        if not donor:
            return None

        tissues_domain = []
        for t in donor.tissues:
            processes_domain = []
            for p in t.processes:
                steps_domain = []
                for s in p.workflow_steps:
                    steps_domain.append(model_to_domain(s, WorkflowStep))
                mapped_p = model_to_domain(p, Process)
                mapped_p.workflow_steps = steps_domain
                processes_domain.append(mapped_p)

            mapped_t = model_to_domain(t, Tissue)
            mapped_t.processes = processes_domain
            tissues_domain.append(mapped_t)

        mapped_donor = model_to_domain(donor, DonorProcessDetails)
        mapped_donor.tissues = tissues_domain
        return mapped_donor
