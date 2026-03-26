# tests/application/test_list_donor.py

import pytest
from app.application.use_cases.donor import ListDonorsUseCase
from app.domain.entities.donor import Donor


class FakeRepo:
    async def list(self, **kwargs):
        return (
            [
                Donor(
                    donor_id=1,
                    znumber=12345,
                    name="Joey",
                    age=30,
                    region="LA",
                    other_factors={}
                )
            ],
            1
        )


@pytest.mark.asyncio
async def test_list_donors():
    repo = FakeRepo()
    use_case = ListDonorsUseCase(repo)

    items, total = await use_case.execute()

    assert total == 1
    assert items[0].name == "Joey"