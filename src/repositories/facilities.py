from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.base import BaseRepository
from src.schemas.facilities import FacilityGet, RoomsFacilityGet


class FacilitiesRepository(BaseRepository):

    model = FacilitiesOrm
    schema = FacilityGet


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacilityGet