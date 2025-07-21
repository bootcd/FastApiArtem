import pytest
from pydantic import BaseModel

from src.config import settings
from src.database import async_session_maker_null_pull
from src.utils.db_manager import DBManager


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-10", 200),
    (1, "2024-08-01", "2024-08-12", 409),
    (1, "2024-09-01", "2024-09-12", 200),
]
)
async def test_add_booking(
        db, authed_ac,
        room_id, date_from, date_to, status_code
):
    response = await authed_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )
    assert response.status_code == status_code
    res = response.json()
    assert isinstance(res, dict)
    if status_code == 200:
        assert res["room_id"] == room_id


@pytest.fixture(scope="session")
async def delete_all_bookings():
    assert settings.MODE == "TEST"
    async with DBManager(session=async_session_maker_null_pull) as db_:
        await db_.bookings.delete()
        await db_.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, bookings_quantity", [
    (1, "2024-08-01", "2024-08-10", 1),
    (1, "2024-08-01", "2024-08-10", 2),
    (1, "2024-08-01", "2024-08-10", 3),
    (1, "2024-08-01", "2024-08-10", 4),
    (1, "2024-08-01", "2024-08-10", 5),
    ]
)
async def test_add_and_get_my_booking(
        db, authed_ac, delete_all_bookings,
        room_id, date_from, date_to, bookings_quantity
):
    add_booking_response = await authed_ac.post(
        "/bookings/",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to
        }
    )

    assert add_booking_response.status_code == 200
    me_response = await authed_ac.get("/bookings/me")
    assert me_response.status_code == 200
    res = me_response.json()
    assert len(res) == bookings_quantity
