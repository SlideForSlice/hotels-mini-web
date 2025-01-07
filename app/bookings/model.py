from sqlalchemy import Computed, Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    room_id: Mapped[Integer] = mapped_column(ForeignKey("rooms.id"))
    user_id: Mapped[Integer] = mapped_column(ForeignKey("users.id"))
    date_from: Mapped[Date] = mapped_column(Date, nullable=False)
    date_to: Mapped[Date] = mapped_column(Date, nullable=False)
    price: Mapped[Integer] = mapped_column(Integer, nullable=False)
    total_cost: Mapped[int] = mapped_column(Computed("(date_to - date_from) * price"))
    total_days: Mapped[int] = mapped_column(Computed("date_to - date_from"))