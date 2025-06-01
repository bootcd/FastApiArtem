import json

from src.database import async_session_maker_null_pull
from src.schemas.hotels import Hotel
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = Hotel(title="OnlyOneStar", location="Anapa")
    async with DBManager(session=async_session_maker_null_pull) as db:
        await db.hotels.add(data=hotel_data)
        await db.commit()

