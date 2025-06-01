import json

from src.database import async_session_maker
from src.schemas.hotels import Hotel
from src.utils.db_manager import DBManager


async def test_add_hotel():
    hotel_data = Hotel(title="OnlyOneStar", location="Anapa")
    pass

