from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserPOST, User
from src.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(user_data: UserPOST):
    async with async_session_maker() as session:
        user_data = User(email=user_data.email, password=AuthService.pwd_context.hash(user_data.password))
        await UsersRepository(session=session).add(user_data)
        await session.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        user_data: UserPOST,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=user_data.email)
        if not user:
            raise HTTPException(status_code=401, detail=f"Пользователь с {user_data.email} не зарегестрирован.")
        if not AuthService().verify_password(user_data.password, user.password):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({'id': user.id})
        response.set_cookie('access_token', access_token)


@router.post("/me")
async def get_me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.get("/logout")
async def logout_user(
        response: Response
):
    response.delete_cookie('access_token')
    return {"status": "OK"}