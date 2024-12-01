from typing import List

from sqlalchemy import select, func

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm

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
