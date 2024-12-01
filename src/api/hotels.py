from fastapi import Query, APIRouter

from src.database import async_session_maker
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH, HotelGET

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


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
    return HotelGET.model_validate(hotel) if hotel else None


@router.put("/")
async def put_hotel(hotel_data: Hotel,
                    hotel_id: int | None = None,
                    location: str | None = None,
                    title: str | None = None
                    ):
    filter_by = {}
    if hotel_id:
        filter_by['id'] = hotel_id
    if title:
        filter_by['title'] = title
    if location:
        filter_by['location'] = location
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, **filter_by)
        await session.commit()
    return {"status": "OK",
            }


@router.delete("/")
async def delete_hotel(hotel_id: int | None = None,
                       title: str | None = None,
                       location: str | None = None):
    filter_by = {}
    if hotel_id:
        filter_by['id'] = hotel_id
    if title:
        filter_by['title'] = title
    if location:
        filter_by['location'] = location
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(**filter_by)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int,
                hotel_data: HotelPATCH
                ):
    return {"status": "OK"}
