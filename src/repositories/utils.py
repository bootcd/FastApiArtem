from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm

def room_ids_for_booking(
            date_from: date,
            date_to: date,
            hotel_id: int = None,
    ):

        rooms_count = (
            select(BookingsOrm.room_id, func.count(BookingsOrm.room_id).label("rooms_booked"))
            .filter(
                BookingsOrm.date_from <= date_to,
                BookingsOrm.date_to >= date_from
            )
            .group_by(BookingsOrm.room_id)
            .cte(name="rooms_count")
        )


        rooms_left_table = (
            select(
                RoomsOrm.id.label("room_id"),
                (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .outerjoin(rooms_count, RoomsOrm.id==rooms_count.c.room_id)
            .cte("rooms_left_table")
        )

        query = select(RoomsOrm.id)
        if hotel_id:
            query=query.filter_by(hotel_id=hotel_id)
        room_ids_from_hotel = query.subquery(name="room_ids_from_hotel")



        room_ids_to_get = (
            select(rooms_left_table.c.room_id)
            .filter(
                rooms_left_table.c.rooms_left > 0,
                rooms_left_table.c.room_id.in_(room_ids_from_hotel)
            )
        )

        return room_ids_to_get
