from pydantic import EmailStr
from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm

    async def get_one_or_none(self, email: EmailStr) -> UserWithHashedPassword:
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        user = UserWithHashedPassword.model_validate(user) if user else user
        return user
