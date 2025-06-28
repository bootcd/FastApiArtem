
from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsBookedException, WrongBookingDatesExceptions
from src.schemas.bookings import Booking, BookingPost

router = APIRouter(prefix="/bookings", tags=["Bookings, Бронирования"])

@router.post("/")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking: BookingPost,
):
    try:
        room = await db.rooms.get_one(id=booking.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=404, detail="Номер не найден")

    _booking_data = Booking(**booking.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(room=room, booking_data=_booking_data)
    except AllRoomsBookedException as e:
        raise HTTPException(status_code=409, detail=e.detail)
    except WrongBookingDatesExceptions as e:
        raise HTTPException(status_code=409, detail=e.detail)
    else:
        await db.commit()

    return {"status": "ok", "data": booking}


@router.get("/")
async def get_bookings(
        db: DBDep,
):
    bookings = await db.bookings.get_all()
    return {"booking": bookings}


@router.get("/me")
async def get_bookings_me(
        db: DBDep,
        user_id: UserIdDep
):
    bookings = await db.bookings.get_all(user_id=user_id)
    return {"booking": bookings}

