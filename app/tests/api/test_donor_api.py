# tests/api/test_donor_api.py

import pytest


@pytest.mark.asyncio
async def test_create_donor_api(client):
    response = await client.post(
        "/api/v1/donors",
        json={
            "znumber": 12345,
            "name": "Monica",
            "age": 28,
            "region": "NY",
            "other_factors": {}
        }
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "Monica"
    assert data["donor_id"] is not None