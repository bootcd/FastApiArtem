from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.rooms import RoomsRepository
from src.repositories.utils import room_ids_for_booking
from src.schemas.bookings import BookingGet, Booking
from src.schemas.rooms import RoomGET


class BookingsRepository(BaseRepository):

    model = BookingsOrm
    schema = BookingGet


    async def add_booking(self, rooms_repo: RoomsRepository, room: RoomGET, booking_data: Booking):
        rooms_to_booking = await rooms_repo.get_filtered_by_date(
            hotel_id=room.hotel_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to
        )
        room_id: int = room.id
        rooms_to_booking_ids = [room.id for room in rooms_to_booking]
        if room_id not in rooms_to_booking_ids:
            raise Exception("Нет таких свободных номеров на эти даты.")

        booking = await self.add(booking_data)

        return booking


