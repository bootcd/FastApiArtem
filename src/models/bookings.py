from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class BookingsOrm(Base):
    __tablename__ = "bookings"

    id:         Mapped[int] = mapped_column(primary_key=True)
    hotel_id:   Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    room_id:    Mapped[int] = mapped_column(ForeignKey("rooms.id"))
    user_id:    Mapped[int] = mapped_column(ForeignKey('users.id'))
    date_from:  Mapped[date]
    date_to:    Mapped[date]
    price:      Mapped[int]

    @hybrid_property
    def total_cost(self) -> int:
        return self.price*(self.date_to - self.date_from).days
