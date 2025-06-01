from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class BookingPost(BaseModel):
    date_from: date
    date_to: date
    room_id: int

class Booking(BookingPost):
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int

class BookingPut(BookingPost):
    room_id: Optional[int] = None
    user_id: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    price: Optional[int] = None

class BookingGet(Booking):
    id: int
    total_cost: int

    model_config = ConfigDict(from_attributes=True)