from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None
    scheme = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filters) -> BaseModel | None:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return self.scheme.model_validate(result.scalars().one_or_none())

    async def add(self, data: BaseModel):
        statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(statement)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        statement = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(statement)

    async def delete(self, **filter_by) -> None:
        statement = delete(self.model).filter_by(**filter_by)
        await self.session.execute(statement)
