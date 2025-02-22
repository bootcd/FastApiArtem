from datetime import date

from sqlalchemy import select, func

from src.models.hotels import HotelsORm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import room_ids_for_booking
from src.schemas.hotels import HotelGET


class HotelsRepository(BaseRepository):
    model = HotelsORm
    schema = HotelGET

    async def get_filtered_by_date(
            self,
            date_from: date,
            date_to: date,
            location: str = None,
            title: str=None,
            offset: int = None,
            limit: int = None
    ):

        room_ids_to_get = room_ids_for_booking(
            date_from=date_from,
            date_to=date_to
        )

        hotel_ids = (
            select(RoomsOrm.hotel_id)
            .filter(
                RoomsOrm.hotel_id.in_(room_ids_to_get)
            )
        )
        if location:
            hotel_ids = hotel_ids.filter(func.lower(self.model.location).like(f'%{location.lower()}%'))
        if title:
            hotel_ids = hotel_ids.filter(func.lower(self.model.title).like(f'%{title.lower()}%'))
        if limit:
            hotel_ids = hotel_ids.limit(limit)
        if offset:
             hotel_ids = hotel_ids.offset(offset)
        return await self.get_filtered(HotelsORm.id.in_(hotel_ids))
