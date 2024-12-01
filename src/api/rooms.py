from fastapi import APIRouter, Query, Body
from starlette.exceptions import HTTPException

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomGET, RoomUpdate, RoomPatch

router = APIRouter(prefix="/hotels", tags=["rooms, Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        room_data: Room = Body(openapi_examples={
            "1": {
                "summary": "Дорогая комната",
                "value": {
                    "hotel_id": 48,
                    "title": "Luxury",
                    "description": "Five Stars!",
                    "quantity": 3,
                    "price": 1000
                }
            },

            "2": {
                "summary": "Две кровати",
                "value": {
                    "hotel_id": 48,
                    "title": "Budget",
                    "description": "Two Stars...Sorry...",
                    "quantity": 30,
                    "price": 100
                }
            }
        })
):
    print(room_data)
    async with async_session_maker() as session:
        room = await RoomsRepository(session=session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int | None,
        title: str | None = Query(None, description="Название"),
        price: int | None = Query(None, description="Цена"),
        description: str | None = Query(None, description="Описание")
):
    async with async_session_maker() as session:
        rooms = await RoomsRepository(session=session).get_all(hotel_id=hotel_id,
                                                               title=title,
                                                               price=price,
                                                               description=description
                                                               )
        rooms = [RoomGET.model_validate(rooms) for rooms in rooms] if rooms else None
    return {"status": "OK", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        hotel_id: int,
        room_id: int
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session=session).get_one_or_none(id=room_id)
    return RoomGET.model_validate(room) if room else None


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(hotel_id: int,
                      room_id: int,
                      room_data: RoomUpdate
                      ):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(hotel_id: int,
                              room_id: int,
                              room_data: RoomPatch
                              ):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data, exclude_unset=True, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int,
                      room_id: int
                      ):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
