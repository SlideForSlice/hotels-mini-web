from sqlalchemy import Integer, JSON, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    hotel_id: Mapped[Integer] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[String] = mapped_column(String)
    description: Mapped[String] = mapped_column(String)
    price: Mapped[Integer] = mapped_column(Integer)
    services: Mapped[JSON] = mapped_column(JSON)
    quantity: Mapped[Integer] = mapped_column(Integer)
    image_id: Mapped[Integer] = mapped_column(Integer)