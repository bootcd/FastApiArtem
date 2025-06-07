from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingPost

router = APIRouter(prefix="/bookings", tags=["Bookings, Бронирования"])

@router.post("/")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking: BookingPost,
):
    room = await db.rooms.get_one_or_none(id=booking.room_id)
    _booking_data = Booking(**booking.model_dump(), user_id=user_id, price=room.price)
    try:
        booking = await db.bookings.add_booking(rooms_repo = db.rooms, room=room, booking_data=_booking_data)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    else:
        await db.commit()

    return {"booking": booking}


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
    print(user_id)
    bookings = await db.bookings.get_all(user_id=user_id)
    return {"booking": bookings}

