from datetime import date

from fastapi import Query, APIRouter

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import Hotel, HotelPATCH, HotelGET

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])


@router.post("/")
async def create_hotel(
        db: DBDep,
        hotel_data: Hotel
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.get("/")
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        date_from: date = Query(example="2025-05-01"),
        date_to: date = Query(example="2025-05-25"),
        location: str | None = Query(None, description="Город"),
        title: str | None = Query(None, description="Название отеля")
):

    hotels = await db.hotels.get_filtered_by_date(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        offset=pagination.per_page * (pagination.page - 1),
        limit=pagination.per_page,
    )
    return hotels


@router.get("/{hotel_id}")
async def get_hotel(
        db: DBDep,
        hotel_id: int
):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return HotelGET.model_validate(hotel) if hotel else None


@router.put("/")
async def put_hotel(
        db: DBDep,
        hotel_data: Hotel,
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
    await db.hotels.edit(hotel_data, **filter_by)
    await db.commit()
    return {"status": "OK"}


@router.delete("/")
async def delete_hotel(
        db: DBDep,
        hotel_id: int | None = None,
        title: str | None = None,
        location: str | None = None
):
    filter_by = {}
    if hotel_id:
        filter_by['id'] = hotel_id
    if title:
        filter_by['title'] = title
    if location:
        filter_by['location'] = location
    await db.hotels.delete(**filter_by)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}")
def patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    return {"status": "OK"}
