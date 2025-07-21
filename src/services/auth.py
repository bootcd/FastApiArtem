from datetime import datetime, timezone, timedelta

import jwt
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, ObjectNotFoundException, \
    UserNotFountException, UserWrongPasswordException
from src.schemas.users import UserPOST, UserWithHashedPassword
from src.services.base import BaseService


class AuthService(BaseService):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        decoded_jwt = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decoded_jwt

    async def register_user(self, user_data: UserPOST):
        user_data = UserPOST(email=user_data.email, password=self.pwd_context.hash(user_data.password))
        try:
            await self.db.users.add(user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException:
            raise UserAlreadyExistsException

    async def login_user(self, user_data: UserPOST):
        try:
            user = await self.db.users.get_user_with_hashed_password(email=user_data.email)
        except ObjectNotFoundException:
            raise UserNotFountException

        if not self.verify_password(user_data.password, user.password):
            raise UserWrongPasswordException

        return  self.create_access_token({'id': user.id})

    async def get_me(self, user_id: int):
        try:
            user = await self.db.users.get_one_or_none(id=user_id)
            return  UserWithHashedPassword.model_validate(user)
        except ObjectNotFoundException:
            raise UserNotFountException
