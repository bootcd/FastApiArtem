from src.exceptions import RoomNotFoundException, ObjectNotFoundException
from src.schemas.bookings import BookingPost, Booking
from src.services.base import BaseService


class BookingsService(BaseService):

    async def add_booking(self, booking: BookingPost, user_id: int):
        try:
            room = await self.db.rooms.get_one(id=booking.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        _booking_data = Booking(**booking.model_dump(), user_id=user_id, price=room.price)
        booking = await self.db.bookings.add_booking(room=room, booking_data=_booking_data)
        await self.db.commit()
        return booking


    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_bookings_me(self, user_id: int):
        return await self.db.bookings.get_all(user_id=user_id)