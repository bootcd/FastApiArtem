from fastapi import Query, APIRouter
from sqlalchemy import select, func, insert

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsORm
from src.schemas.schemas import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])

@router.post("/")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        statement = insert(HotelsORm).values(**hotel_data.model_dump())
        await session.execute(statement)
        await session.commit()
    return {"status": "OK"}


@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Город"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsORm)
        if location:
            query = query.filter(func.lower(HotelsORm.location).like(f'%{location.lower()}%'))
        if title:
            query = query.filter(func.lower(HotelsORm.title).like(f'%{title.lower()}%'))
        offset = pagination.per_page * (pagination.page - 1)
        limit = pagination.per_page
        query = (query
                 .limit(limit)
                 .offset(offset)
                 )
        result = await session.execute(query)
        hotels = result.scalars().all()
    return hotels


@router.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    return {"status": "OK",
            }


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int,
                hotel_data: HotelPATCH
                ):
    return {"status": "OK"}


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    return {"status": "OK"}
