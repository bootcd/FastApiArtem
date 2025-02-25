from datetime import date

from fastapi import APIRouter, Query, Body
from starlette.exceptions import HTTPException

from src.api.dependencies import DBDep
from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.facilities import RoomsFacility
from src.schemas.rooms import Room, RoomGET, RoomUpdate, RoomPatch, RoomAddRequest

router = APIRouter(prefix="/hotels", tags=["rooms, Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {
                "summary": "Дорогая комната",
                "value": {
                    "hotel_id": 3,
                    "title": "Luxury",
                    "description": "Five Stars!",
                    "quantity": 3,
                    "price": 1000,
                    "facilities_ids": [
                        1,2
                    ]
                }
            },

            "2": {
                "summary": "Две кровати",
                "value": {
                    "hotel_id": 3,
                    "title": "Budget",
                    "description": "Two Stars...Sorry...",
                    "quantity": 30,
                    "price": 100,
                    "facilities_ids": [
                        1, 2, 3
                    ]
                }
            }
        })
):
    _room_data = Room(**room_data.model_dump())
    room = await db.rooms.add(_room_data)
    rooms_facility_data = [RoomsFacility(room_id=room.id, facility_id=facility_id) for facility_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(data=rooms_facility_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int | None,
        date_from: date = Query(example="2025-05-01"),
        date_to: date = Query(example="2025-05-25")
):
    rooms = await db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)
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
    facilities_ids = [fa.facility_id for fa in await db.rooms_facilities.get_all(room_id=room_id)]
    fa_ids_from_data = room_data.facilities_ids
    fa_ids_for_delete = set(facilities_ids) - set(fa_ids_from_data)
    fa_ids_for_add = set(fa_ids_from_data) - set(facilities_ids)
    rooms_facility_data = [RoomsFacility(room_id=room_id, facility_id=facility_id) for facility_id in fa_ids_for_add]
    await db.rooms_facilities.delete(db.rooms_facilities.model.facility_id.in_(fa_ids_for_delete), room_id=room_id)
    await db.rooms_facilities.add_bulk(data=rooms_facility_data)
    await db.rooms.edit(data=RoomPatch.model_validate(room_data), id=room_id)
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
