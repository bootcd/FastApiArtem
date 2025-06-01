import json

import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker, async_session_maker_null_pull
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room
from src.schemas.users import UserPOST
from src.utils.db_manager import DBManager


@pytest.fixture(scope="function", autouse=True)
async def db(setup_database):
    async with DBManager(session=async_session_maker_null_pull) as db:
        yield db

@pytest.fixture(scope="session", autouse=True)
async def setup_database():

    assert settings.MODE == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("tests/mock_hotels.json", "r", encoding="utf-8") as f:
        _hotels = [Hotel(**hotel) for hotel in json.load(f)]

    with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
        _rooms = [Room(**room) for room in json.load(f)]

    user = {"email": "foobar@fonar.com", "password": "foobar"}

    async with DBManager(session=async_session_maker_null_pull) as db_:
        await db_.hotels.add_bulk(data=_hotels)
        await db_.rooms.add_bulk(data=_rooms)
        await db_.users.add(data=UserPOST(**user))
        await db_.commit()
