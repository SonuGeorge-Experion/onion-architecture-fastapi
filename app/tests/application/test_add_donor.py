# tests/application/test_add_donor.py

import pytest
from app.application.use_cases.donor import AddDonorUseCase
from app.application.dtos.donor import CreateDonorInputDTO
from app.domain.entities.donor import Donor


class FakeRepo:
    async def exists_by_znumber(self, znumber):
        return False

    async def add(self, donor: Donor):
        donor.donor_id = 1
        return donor


@pytest.mark.asyncio
async def test_add_donor_success():
    repo = FakeRepo()
    use_case = AddDonorUseCase(repo)

    input_dto = CreateDonorInputDTO(
        znumber=12345,
        name="Chandler",
        age=30,
        region="NY",
        other_factors={}
    )

    result = await use_case.execute(input_dto)

    assert result.donor_id == 1
    assert result.name == "Chandler"