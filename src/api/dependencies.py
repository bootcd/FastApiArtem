from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.params import Query
from pydantic import BaseModel
from starlette.requests import Request

from src.services.auth import AuthService


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Сраница")]
    per_page: Annotated[int | None, Query(3, description="Количество отелей на 1 странице")]


PaginationDep = Annotated[PaginationParams, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(401, detail="Не предоставлен токен.")
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    return AuthService().decode_token(token)["id"]


UserIdDep = Annotated[int, Depends(get_current_user_id)]
