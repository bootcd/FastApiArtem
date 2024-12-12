from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update


class BaseRepository:
    model = None
    schema = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        result = result.scalars().all()
        return [self.schema.model_validate(instance) for instance in result]

    async def get_one_or_none(self, **filters) -> BaseModel | None:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        return self.schema.model_validate(result)

    async def add(self, data: BaseModel):
        statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(statement)
        return result.scalars().one()

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        statement = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(statement)

    async def delete(self, **filter_by) -> None:
        statement = delete(self.model).filter_by(**filter_by)
        await self.session.execute(statement)
