from typing import List
from asyncpg.exceptions import UniqueViolationError
from pydantic import BaseModel
from sqlalchemy import select, insert, delete, update
from sqlalchemy.exc import NoResultFound, IntegrityError

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException


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

    async def get_filtered(self, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        result = result.scalars().all()
        return [self.schema.model_validate(instance) for instance in result]

    async def get_one_or_none(self, **filters) -> BaseModel | None:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        return self.schema.model_validate(result) if result else None

    async def get_one(self, **filters) -> BaseModel:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        try:
            result = result.scalar_one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.schema.model_validate(result)

    async def add(self, data: BaseModel):
        statement = insert(self.model).values(**data.model_dump()).returning(self.model)
        try:
            result = await self.session.execute(statement)
        except IntegrityError:
            raise ObjectAlreadyExistsException
        return result.scalars().one()

    async def add_bulk(self, data: List[BaseModel]):
        statement = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(statement)


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        statement = update(self.model).filter_by(**filter_by).values(**data.model_dump(exclude_unset=exclude_unset))
        await self.session.execute(statement)

    async def delete(self, *filter, **filter_by) -> None:
        statement = (
            delete(self.model)
            .filter(
                *filter
            )
            .filter_by(
                **filter_by
            )
        )
        await self.session.execute(statement)
