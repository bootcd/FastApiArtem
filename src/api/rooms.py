from datetime import date

from fastapi import APIRouter, Query, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacility
from src.schemas.rooms import Room, RoomUpdate, RoomPatch, RoomAddRequest, RoomGET, RoomPatchRequest

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
    room = await db.rooms.get_one_with_rels(room_id=room_id)
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomUpdate
):
    await db.rooms_facilities.update_rooms_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatchRequest
):
    _room_data_dict = room_data.model_dump(exclude_unset=True)
    _room_data = RoomPatch.model_validate(room_data.model_dump())
    await db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
    if "facilities_ids" in _room_data_dict:
        await db.rooms_facilities.update_rooms_facilities(room_id=room_id, facilities_ids=_room_data_dict["facilities_ids"])
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
