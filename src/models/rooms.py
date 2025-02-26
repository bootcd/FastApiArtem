from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoomsOrm(Base):

    __tablename__ = "rooms"

    id:             Mapped[int] = mapped_column(primary_key=True)
    hotel_id:       Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title:          Mapped[str]
    description:    Mapped[str | None]
    quantity:       Mapped[int]
    price:          Mapped[int]

    facilities:     Mapped[List["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities"
    )
