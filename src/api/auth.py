from fastapi import APIRouter
from starlette.responses import Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserAlreadyExistsException, UserAlreadyExistsHTTPException, UserNotFountException, \
    UserNotFountHTTPException, UserWrongPasswordException, UserWrongPasswordHTTPException
from src.schemas.users import UserPOST
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth, Аутентификация и авторизация"])


@router.post("/register")
async def register_user(
        db: DBDep,
        user_data: UserPOST
):
    try:
        await AuthService(db).register_user(user_data)
        return {"status": "OK"}
    except UserAlreadyExistsException:
        raise UserAlreadyExistsHTTPException


@router.post("/login")
async def login_user(
        db: DBDep,
        user_data: UserPOST,
        response: Response
):
    try:
        access_token = await AuthService(db).login_user(user_data)
        response.set_cookie('access_token', access_token)
    except UserNotFountException:
        raise UserNotFountHTTPException

    except UserWrongPasswordException:
        raise UserWrongPasswordHTTPException



@router.get("/me")
async def get_me(
        db: DBDep,
        user_id: UserIdDep
):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotFountException:
        raise UserNotFountHTTPException


@router.get("/logout")
async def logout_user(
        response: Response
):
    response.delete_cookie('access_token')
    return {"status": "OK"}

