from datetime import datetime, timezone

import jwt
from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserPOST, User
from passlib.context import CryptContext

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "AsdewrfwrefdreWD3434564trdsf43yt546yu65thfgdf235rt45uy"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register")
async def register_user(user_data: UserPOST):
    async with async_session_maker() as session:
        user_data = User(email=user_data.email, password=pwd_context.hash(user_data.password))
        await UsersRepository(session=session).add(user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        user_data: UserPOST,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail=f"Пользователь с {user_data.email} не зарегестрирован.")
        if not verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = create_access_token({'id': user.id})
        response.set_cookie('access_token', access_token)


@router.post("/only_auth")
async def only_auth(
        request: Request
):
    access_token = request.cookies.get('access_token') or None
    return {"access_token": access_token}
