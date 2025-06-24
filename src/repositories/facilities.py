from sqlalchemy import delete, select, insert

from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilityGet, RoomsFacilityGet


class FacilitiesRepository(BaseRepository):

    model = FacilitiesOrm
    schema = FacilityGet


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilityGet

    async def update_rooms_facilities(self, room_id, facilities_ids):

        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)
        current_facilities_ids = result.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            statement = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_delete),
            )

            await self.session.execute(statement)

        if ids_to_insert:
            statement = (
                insert(self.model).values(
                    [
                        {"room_id": room_id, "facility_id": fa_id} for fa_id in ids_to_insert
                    ]
                )
            )

            await self.session.execute(statement)
