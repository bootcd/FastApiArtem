from datetime import date

from src.api.dependencies import PaginationDep
from src.exceptions import ObjectAlreadyExistsException, HotelAlreadyExistsException, ObjectNotFoundException, \
    HotelNotFoundException
from src.schemas.hotels import Hotel
from src.services.base import BaseService


class HotelsService(BaseService):

    async def add_hotel(self, hotel_data: Hotel):
        try:
            hotel = await self.db.hotels.add(hotel_data)
            await self.db.commit()
            return hotel
        except ObjectAlreadyExistsException:
            raise HotelAlreadyExistsException


    async def get_filtered_by_date(
            self,
            pagination: PaginationDep,
            date_from: date,
            date_to: date,
            location: str,
            title: str
    ):

        return await self.db.hotels.get_filtered_by_date(
            date_from=date_from,
            date_to=date_to,
            location=location,
            title=title,
            offset=pagination.per_page * (pagination.page - 1),
            limit=pagination.per_page,
        )

    async def get_hotel(self, hotel_id: int):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

    async def partially_edit_hotel(self, hotel_data: Hotel, exclude_unset: bool, hotel_id):
        await self.db.hotels.edit(data=hotel_data, exclude_unset=exclude_unset, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()
