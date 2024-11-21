from sqlalchemy import Integer, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import NullType
from typing_extensions import Optional

from app.database import Base

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[Integer] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[String] = mapped_column(String, nullable=False)
    description: Mapped[String] = mapped_column(String, nullable=False)
    price: Mapped[Integer] = mapped_column(Integer, nullable=False)
    services: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    quantity: Mapped[Integer] = mapped_column(Integer, nullable=False)
    image_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)