from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class RoomsOrm(Base):

    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    title: Mapped[int]
    description: Mapped[str | None]
    quantity: Mapped[int]
    price: Mapped[int]
