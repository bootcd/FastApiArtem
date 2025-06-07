from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.facilities import FacilityGet


class Room(BaseModel):
    title:          str
    description:    Optional[str] = None
    quantity:       int
    price:          int
    hotel_id:       int
    model_config = ConfigDict(from_attributes=True)


class RoomAddRequest(Room):

    facilities_ids: Optional[List[int]] = None


class RoomGET(RoomAddRequest):
    id: int


class RoomUpdate(RoomAddRequest):
    price: int = Field(gt=0)


class RoomPatch(BaseModel):
    title:          str | None = Field(None)
    description:    str | None = Field(None)
    quantity:       int | None = Field(None)
    price:          int | None = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)


class RoomPatchRequest(RoomPatch):
    facilities_ids: List[int] = None


class RoomWithRels(RoomGET):
    facilities: List[FacilityGet]