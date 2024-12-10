from datetime import date

from pydantic import BaseModel
class BookingPost(BaseModel):
    date_from: date
    date_to: date
    price: int
class Booking(BookingPost):
    hotel_id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int

class BookingGet(Booking):
    id: int
    total_cost: int
