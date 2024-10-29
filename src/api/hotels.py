from fastapi import Query, APIRouter
from sqlalchemy import select

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsORm
from src.schemas.schemas import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])

@router.post("/")
def create_hotel(hotel_data: Hotel):
    return {"status": "OK"}


@router.get("/")
async def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    async with async_session_maker() as session:
        query = select(HotelsORm).filter_by(id=id, title=title)
        result = await session.execute(query)
        hotels = result.all()
        print(hotels)
    offset = pagination.per_page * (pagination.page - 1)
    limit = pagination.per_page
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
