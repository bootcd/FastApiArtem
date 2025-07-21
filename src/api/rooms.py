from datetime import date

from fastapi import APIRouter, Query, Body, HTTPException

from src.api.dependencies import DBDep
from src.exceptions import ObjectNotFoundException, WrongBookingDatesExceptions, WrongBookingDatesHTTPException, \
    RoomNotFoundException, HotelNotFoundException, HotelNotFoundHTTPException, RoomNotFoundHTTPException
from src.schemas.facilities import RoomsFacility
from src.schemas.rooms import Room, RoomUpdate, RoomPatch, RoomAddRequest, RoomGET, RoomPatchRequest
from src.services.rooms import RoomsService

router = APIRouter(prefix="/hotels", tags=["rooms, Номера"])


@router.post("/{hotel_id}/rooms")
async def create_room(
        hotel_id: int,
        db: DBDep,
        room_data: RoomAddRequest = Body()
):
    try:
        room = await RoomsService(db).add_room(room_data, hotel_id)
        return {"status": "OK", "data": room}
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.get("/{hotel_id}/rooms")
async def get_rooms(
        db: DBDep,
        hotel_id: int | None,
        date_from: date = Query(example="2025-05-01"),
        date_to: date = Query(example="2025-05-25")
):
    try:
        return await RoomsService(db).get_filtered_by_time(hotel_id,date_from,date_to)
    except WrongBookingDatesExceptions as e:
        raise WrongBookingDatesHTTPException

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        room = await RoomsService(db).get_room(hotel_id, room_id)
        return {"status": "OK", "data": room}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomUpdate
):
    try:
        await RoomsService(db).update_room(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.patch("/{hotel_id}/rooms/{room_id}")
async def partial_update_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
        room_data: RoomPatchRequest
):
    try:
        await RoomsService(db).partial_update_room(hotel_id, room_id, room_data)
        return {"status": "OK"}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    try:
        await RoomsService(db).delete_room(room_id=room_id)
        return {"status": "OK"}
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
