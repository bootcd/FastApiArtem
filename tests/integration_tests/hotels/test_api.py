from httpx import AsyncClient


async def test_api_hotels(ac: AsyncClient):
    response = await ac.get(
        "/hotels/",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10"
        }
    )

    assert response.status_code == 200

    response = await ac.get(
        "/hotels/"
    )

    assert response.status_code == 422