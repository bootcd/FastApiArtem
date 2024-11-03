from pydantic import BaseModel, Field


class Hotel(BaseModel):
    title: str
    location: str


class HotelGET(Hotel):
    id: int

    class Config:
        from_attributes = True

class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
