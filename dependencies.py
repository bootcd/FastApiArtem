from typing import Annotated

from fastapi import Depends
from fastapi.params import Query
from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: Annotated[int | None, Query(1, description="Сраница")]
    per_page: Annotated[int | None, Query(3, description="Количество отелей на 1 странице")]


PaginationDep = Annotated[PaginationParams, Depends()]
