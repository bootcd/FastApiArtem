from sqlalchemy import select, func, insert

from src.models.hotels import HotelsORm
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORm

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

    async def add(self, data):
        statement = insert(HotelsORm).values(**data.model_dump())
        result = await self.session.execute(statement)
        return result


