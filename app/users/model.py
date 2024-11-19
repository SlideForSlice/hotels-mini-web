from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    email: Mapped[String] = mapped_column(String, unique=True, nullable=False)
    hashed_password: Mapped[String] = mapped_column(String, nullable=False)