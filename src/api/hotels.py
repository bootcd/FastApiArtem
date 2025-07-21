from datetime import date

from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import HotelAlreadyExistsException, HotelAlreadyHttpExistsException, \
    HotelNotFoundException, HotelNotFoundHTTPException
from src.schemas.hotels import Hotel, HotelPATCH
from src.services.hotels import HotelsService

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])


@router.post("/")
async def create_hotel(
        db: DBDep,
        hotel_data: Hotel
):
    try:
        return await HotelsService(db).add_hotel(hotel_data)
    except HotelAlreadyExistsException:
        raise HotelAlreadyHttpExistsException

@router.get("/")
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        date_from: date = Query(example="2025-05-01"),
        date_to: date = Query(example="2025-05-25"),
        location: str | None = Query(None, description="Город"),
        title: str | None = Query(None, description="Название отеля")
):

    hotels = await HotelsService(db).get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        pagination=pagination
    )
    return {"status": "ok", "data": hotels}


@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int
):
    try:
        return await HotelsService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.put("/")
async def put_hotel(
        db: DBDep,
        hotel_data: Hotel,
        hotel_id: int | None = None,
):
    await HotelsService(db).partially_edit_hotel(hotel_data, exclude_unset=True, hotel_id=hotel_id)
    return {"status": "OK"}


@router.delete("/")
async def delete_hotel(
        db: DBDep,
        hotel_id: int | None = None,
):
    await HotelsService(db).delete_hotel(hotel_id=hotel_id)
    return {"status": "OK"}
