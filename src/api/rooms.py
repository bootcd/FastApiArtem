from fastapi import APIRouter, Query, Body
from starlette.exceptions import HTTPException

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomGET, RoomUpdate, RoomPatch

router = APIRouter(prefix="/hotels", tags=["rooms, Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
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
    room = await db.rooms.add(room_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int | None,
        title: str | None = Query(None, description="Название"),
        price: int | None = Query(None, description="Цена"),
        description: str | None = Query(None, description="Описание")
):
    rooms = await db.rooms.get_all(hotel_id=hotel_id,
                                   title=title,
                                   price=price,
                                   description=description
                                   )
    rooms = [RoomGET.model_validate(rooms) for rooms in rooms] if rooms else None
    return {"status": "OK", "data": rooms}


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    room = await db.rooms.get_one_or_none(id=room_id)
    return RoomGET.model_validate(room) if room else None


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomUpdate
):
    await db.rooms.edit(data=room_data, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatch
):
    await db.rooms.edit(data=room_data, exclude_unset=True, id=room_id)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.delete(id=room_id)
    await db.commit()
    return {"status": "OK"}
