from fastapi import Query, APIRouter
from sqlalchemy import select, func, insert

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsORm
from src.repositories.hotels import HotelsRepository
from src.schemas.schemas import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])


@router.post("/")
async def create_hotel(hotel_data: Hotel):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session=session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Город"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        hotels = await HotelsRepository(session=session).get_all(offset=pagination.per_page * (pagination.page - 1),
                                                                 limit=pagination.per_page,
                                                                 location=location,
                                                                 title=title,
                                                                 )

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
