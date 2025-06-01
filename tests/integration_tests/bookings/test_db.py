from datetime import date
from src.schemas.bookings import Booking, BookingGet, BookingPut
from src.utils.db_manager import DBManager


async def test_add_booking(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    booking_data = Booking(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=8, day=10),
        date_to=date(year=2025, month=8, day=20),
        price=1000
    )

    # CREATE
    booking = await db.bookings.add(data=booking_data)

    #READ
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert isinstance(booking, BookingGet)

    #UPDATE
    await db.bookings.edit(data=BookingPut(price=3000), id=booking.id, exclude_unset=True)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking.price == 3000

    #DELETE
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=booking.id)
    assert booking is None
