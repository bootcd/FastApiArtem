from sqlalchemy import select

from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserWithHashedPassword, User


class UsersRepository(BaseRepository):
    model = UsersOrm
    scheme = User

    async def get_user_with_hashed_password(self, **filters) -> UserWithHashedPassword:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        user = result.scalars().one_or_none()
        user = UserWithHashedPassword.model_validate(user) or None
        return user
