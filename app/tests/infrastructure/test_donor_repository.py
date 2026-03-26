# tests/infrastructure/test_donor_repository.py

import pytest
from app.infrastructure.db.repositories.donor_repository import DonorRepositoryORM
from app.domain.entities.donor import Donor


@pytest.mark.asyncio
async def test_add_and_exists(db_session):
    repo = DonorRepositoryORM(db_session)

    donor = Donor(
        donor_id=None,
        znumber=12345,
        name="Test",
        age=25,
        region="Test",
        other_factors={}
    )

    created = await repo.add(donor)

    exists = await repo.exists_by_znumber(12345)

    assert created.donor_id is not None
    assert exists is True