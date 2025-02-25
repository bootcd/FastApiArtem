from pydantic import BaseModel, ConfigDict


class Facility(BaseModel):
    title: str

class FacilityGet(Facility):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomsFacility(BaseModel):
    room_id: int
    facility_id: int
    model_config = ConfigDict(from_attributes=True)


class RoomsFacilityGet(RoomsFacility):
    id: int
