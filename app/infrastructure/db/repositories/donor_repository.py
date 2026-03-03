from typing import Optional

from sqlalchemy import asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlalchemy.exc import IntegrityError

from app.domain.entities.donor import Donor as DomainDonor
from app.domain.repositories.donor_repository import DonorRepository
from app.domain.exceptions import DuplicateZNumberException
from app.infrastructure.db.models.donor import Donors
from app.infrastructure.db.repositories.base_repository import BaseRepository
from app.infrastructure.db.utils import model_to_domain


class DonorRepositoryORM(BaseRepository, DonorRepository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, model_cls=Donors, domain_cls=DomainDonor)

    async def add(self, donor: DomainDonor) -> DomainDonor:
        try:
            return await self.create(donor, id_field="donor_id")
        except IntegrityError as exc:
            # Map DB unique-constraint on znumber to domain exception
            # Works for PostgreSQL (psycopg) and other dialects exposing 'orig' with constraint name
            err_msg = str(getattr(exc, "orig", exc))
            if "donors_znumber_key" in err_msg or "unique constraint" in err_msg.lower() and "znumber" in err_msg.lower():
                raise DuplicateZNumberException(str(donor.znumber)) from exc
            raise

    async def list(
        self,
        filters: dict | None = None,
        search: str | None = None,
        order_by: str | None = None,
        order_dir: str = "asc",
        page: int = 1,
        per_page: int = 20,
    ) -> tuple[list[DomainDonor], int]:
        filters = filters or {}
        conditions = []

        # simple equality filters
        for key, value in filters.items():
            col = getattr(Donors, key, None)
            if col is not None and value is not None:
                conditions.append(col == value)

        # search on name
        if search:
            conditions.append(Donors.name.ilike(f"%{search}%"))

        # total count
        count_stmt = select(func.count()).select_from(Donors)
        if conditions:
            count_stmt = count_stmt.where(*conditions)
        total_res = await self.session.execute(count_stmt)
        total = total_res.scalar_one()

        # ordering
        allowed_cols = {c.name for c in Donors.__table__.columns}
        if order_by not in allowed_cols:
            order_by = "donor_id"
        col = getattr(Donors, order_by)
        order_fn = asc if (order_dir or "").lower() == "asc" else desc

        stmt: Select = select(Donors)
        if conditions:
            stmt = stmt.where(*conditions)
        stmt = (
            stmt.order_by(order_fn(col)).limit(per_page).offset((page - 1) * per_page)
        )

        res = await self.session.execute(stmt)
        rows = res.scalars().all()

        # map models to domain objects
        items = [model_to_domain(r, DomainDonor) for r in rows]
        return items, int(total)
