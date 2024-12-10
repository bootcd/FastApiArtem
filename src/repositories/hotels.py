from sqlalchemy import select, func

from src.models.hotels import HotelsORm
from src.repositories.base import BaseRepository
from src.schemas.hotels import HotelGET


class HotelsRepository(BaseRepository):
    model = HotelsORm
    schema = HotelGET

    async def get_all(self,
                      offset,
                      limit,
                      location,
                      title,
                      ):
        query = select(self.model)
        if location:
            query = query.filter(func.lower(self.model.location).like(f'%{location.lower()}%'))
        if title:
            query = query.filter(func.lower(self.model.title).like(f'%{title.lower()}%'))
        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        return hotels



