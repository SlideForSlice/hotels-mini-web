from datetime import date
from http.client import HTTPException
from types import NoneType

from app.dao.base import BaseDAO
from app.bookings.model import Bookings
from sqlalchemy import insert, select, and_, or_, func

from app.database import async_session_maker
from app.exceptions import HotelAlreadyExistsException
from app.hotels.model import Hotels
from app.hotels.rooms.model import Rooms

class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def add(
            cls,
            name: str,
            location: str,
            rooms_quantity: int,
            services: dict = None,
    ):
        async with async_session_maker() as session:

            query = select(Hotels).where(Hotels.name == name)
            result = await session.execute(query)
            hotel_exists = result.scalar_one_or_none()

            if not hotel_exists:
                new_hotel = Hotels(name=name, location=location, rooms_quantity=rooms_quantity, services=services)
                session.add(new_hotel)
                await session.commit()
                await session.refresh(new_hotel)
                return new_hotel
            else:
                raise HotelAlreadyExistsException



