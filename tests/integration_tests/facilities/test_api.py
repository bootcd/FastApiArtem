from httpx import AsyncClient


async def test_api_facilities_get_all(ac: AsyncClient):
    response = await ac.get(
        "/facilities/",
    )
    facilities = response.json()

    mock_facility = {"id": 1, "title": "Интернет"}

    assert response.status_code == 200
    assert isinstance(facilities, list)
    assert mock_facility in facilities


async def test_api_facilities_add(ac: AsyncClient):
    title = "Блэкаут шторы"

    response = await ac.post(
        "/facilities/",
        json = {"title": title}
    )

    new_facility_data = response.json()

    assert response.status_code == 200
    assert new_facility_data
    assert isinstance(new_facility_data, dict)
    assert new_facility_data.get("title") == title