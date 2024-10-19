from fastapi import Query, APIRouter

from dependencies import PaginationDep
from schemas.schemas import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["hotels, Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "Three Stars"},
    {"id": 2, "title": "Дубай", "name": "So hot in July"},
    {"id": 3, "title": "Goa", "name": "Cabin in the Woods"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.post("/")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@router.get("/")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    # ПАГИНАЦИЯ

    # Задаем индекс первого элемента отображения отелей в срезе
    # - берем заданное количество отелей на страницу,
    # - умножаем на номер страницы со сдвигом "влево" на 1 (нумерация индексов с 0)
    start = pagination.per_page * (pagination.page - 1)

    # Задаем индекс конечного элемента отображения отелей в срезе
    # - берем индекс первого отеля на странице (срезе),
    # - прибавляем количество отелей на страницу
    stop = start + pagination.per_page
    return hotels_[start:stop]


@router.put("/hotels/{hotel_id}")
def put_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {"status": "OK",
            }


@router.patch("/{hotel_id}")
def patch_hotel(hotel_id: int,
                hotel_data: HotelPATCH
                ):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title is not None:
        hotel['title'] = hotel_data.title
    if hotel_data.name is not None:
        hotel['name'] = hotel_data.title
    return {"status": "OK",
            }


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
