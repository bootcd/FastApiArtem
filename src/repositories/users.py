from sqlalchemy import select

from src.exceptions import ObjectNotFoundException
from src.models.users import UsersOrm
from src.repositories.base import BaseRepository
from src.schemas.users import UserWithHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    schema = UserWithHashedPassword

    async def get_user_with_hashed_password(self, **filters) -> UserWithHashedPassword:
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        result = result.scalar_one()
        if not result:
            raise ObjectNotFoundException
        return UserWithHashedPassword.model_validate(result)
