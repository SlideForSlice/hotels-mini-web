from sqlalchemy import Integer, Column, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    name: Mapped[String] = mapped_column(String, nullable=False)
    location: Mapped[String] = mapped_column(String, nullable=False)
    services: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    rooms_quantity: Mapped[Integer] = mapped_column(Integer, nullable=False)
    image_id: Mapped[Integer | None] = mapped_column(Integer, nullable=True)