from datetime import date
from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload

from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.schemas.rooms import RoomGET, RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = RoomGET

    async def get_all(self,
                      hotel_id,
                      title,
                      price,
                      description
                      ):
        query = select(RoomsOrm)
        if title:
            query = query.filter_by(title=title)
        if hotel_id:
            query = query.filter_by(hotel_id=hotel_id)
        if price:
            query = query.filter_by(price=price)
        if description:
            query = query.filter(func.lower(self.model.description).contains(description.lower()))
        result = await self.session.execute(query)
        result = result.scalars().all()
        return result

    async def get_filtered_by_date(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date,
    ):
        room_ids_to_get = room_ids_for_booking(
            hotel_id=hotel_id,
            date_from=date_from,
            date_to=date_to
        )

        query = (
            select(self.model)
            .options(
                joinedload(self.model.facilities)
            )
            .filter(RoomsOrm.id.in_(room_ids_to_get))
                 )
        result = await self.session.execute(query)
        rooms = result.scalars().unique().all()
        return [RoomWithRels.model_validate(room) for room in rooms]


    async def get_one_with_rels(self, room_id):
        query = (
            select(self.model)
            .options(
                joinedload(self.model.facilities)
            )
            .filter(RoomsOrm.id == room_id))

        result = await self.session.execute(query)
        room = result.unique().scalar_one_or_none()
        return RoomWithRels.model_validate(room)


