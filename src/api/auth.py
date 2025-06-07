from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserPOST, UserGET, UserWithHashedPassword
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth, Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        user_data: UserPOST
):
    user_data = UserPOST(email=user_data.email, password=AuthService.pwd_context.hash(user_data.password))
    await db.users.add(user_data)
    await db.commit()
    return {"status": "OK"}


@router.post("/login")
async def login_user(
        db: DBDep,
        user_data: UserPOST,
        response: Response
):
    user = await db.users.get_user_with_hashed_password(email=user_data.email)
    if not user:
        raise HTTPException(status_code=401, detail=f"Пользователь с {user_data.email} не зарегистрирован.")
    if not AuthService().verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Неверный пароль")
    access_token = AuthService().create_access_token({'id': user.id})
    response.set_cookie('access_token', access_token)


@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    user = await db.users.get_one_or_none(id=user_id)
    user = UserWithHashedPassword.model_validate(user)
    return user


@router.get("/logout")
async def logout_user(
        response: Response
):
    response.delete_cookie('access_token')
    return {"status": "OK"}

