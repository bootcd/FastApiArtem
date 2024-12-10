from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingPost

router = APIRouter(prefix="/booking/hotels/{hotel_id}/rooms", tags=["Bookings, Бронирования"])

@router.post("/{room_id}")
async def add_booking(
        db: DBDep,
        user_id: UserIdDep,
        hotel_id: int,
        room_id: int,
        booking: BookingPost,
):
    booking = Booking(**booking.model_dump(), hotel_id=hotel_id, room_id=room_id, user_id=user_id)
    booking = await db.bookings.add(booking)
    await db.commit()
    return {"booking": booking}
