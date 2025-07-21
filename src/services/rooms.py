from datetime import date

from src.exceptions import WrongBookingDatesExceptions, ObjectNotFoundException, RoomNotFoundException, \
    HotelNotFoundException
from src.schemas.facilities import RoomsFacility
from src.schemas.rooms import Room, RoomUpdate, RoomPatch, RoomPatchRequest
from src.services.base import BaseService


class RoomsService(BaseService):

    async def add_room(self, room_data, hotel_id: int):
        _room_data = Room(**room_data.model_dump())
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException

        room = await self.db.rooms.add(_room_data)
        rooms_facility_data = [
            RoomsFacility(room_id=room.id, facility_id=facility_id) for facility_id in room_data.facilities_ids
        ]
        await self.db.rooms_facilities.add_bulk(data=rooms_facility_data)
        await self.db.commit()

    async def get_filtered_by_time(
            self,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        if date_to <= date_from:
            raise WrongBookingDatesExceptions
        return await self.db.rooms.get_filtered_by_date(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

    async def get_room(self, hotel_id: int, room_id: int):
        try:
            return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, room_id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException


    async def update_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomUpdate
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        await self.db.rooms_facilities.update_rooms_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
        await self.db.commit()


    async def partial_update_room(
            self,
            hotel_id: int,
            room_id: int,
            room_data: RoomPatchRequest
    ):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        _room_data_dict = room_data.model_dump(exclude_unset=True)
        _room_data = RoomPatch.model_validate(room_data.model_dump())
        await self.db.rooms.edit(data=_room_data, exclude_unset=True, id=room_id)
        if "facilities_ids" in _room_data_dict:
            await self.db.rooms_facilities.update_rooms_facilities(
                room_id=room_id,
                facilities_ids=_room_data_dict["facilities_ids"]
            )
        await self.db.commit()

    async def delete_room(self, room_id: int):
        try:
            await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        await self.db.rooms.delete(id=room_id)
        await self.db.commit()