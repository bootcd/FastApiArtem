from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Room(BaseModel):
    title:          str
    description:    Optional[str] = None
    quantity:       int
    price:          int
    hotel_id:       int

    model_config = ConfigDict(from_attributes=True)

class RoomGET(Room):
    id: int


class RoomUpdate(BaseModel):
    title:          str
    description:    str
    quantity:       int
    price:          int = Field(gt=0)

    model_config = ConfigDict(from_attributes=True)

class RoomPatch(BaseModel):
    title:          str | None = Field(None)
    description:    str | None = Field(None)
    quantity:       int | None = Field(None)
    price:          int | None = Field(None, gt=0)

    model_config = ConfigDict(from_attributes=True)
