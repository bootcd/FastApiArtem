from src.exceptions import AllRoomsBookedException, WrongBookingDatesExceptions
from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.schemas.bookings import BookingGet, Booking
from src.schemas.rooms import RoomGET


class BookingsRepository(BaseRepository):

    model = BookingsOrm
    schema = BookingGet


    async def add_booking(self, room: RoomGET, booking_data: Booking):
        if booking_data.date_to <= booking_data.date_from:
            raise WrongBookingDatesExceptions
        rooms_to_booking_query = room_ids_for_booking(
            hotel_id=room.hotel_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to
        )
        result = await self.session.execute(rooms_to_booking_query)
        rooms_to_booking_ids: list[int] = result.scalars().all()
        room_id: int = room.id
        if room_id not in rooms_to_booking_ids:
            raise AllRoomsBookedException
        booking = await self.add(booking_data)
        return booking


