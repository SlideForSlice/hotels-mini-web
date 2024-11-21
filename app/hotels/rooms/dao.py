from datetime import date
from http.client import HTTPException
from types import NoneType
from typing import Optional

from app.dao.base import BaseDAO
from app.bookings.model import Bookings
from sqlalchemy import insert, select, and_, or_, func

from app.database import async_session_maker
from app.exceptions import *
from app.hotels.model import Hotels
from app.hotels.rooms.model import Rooms

class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def add(
            cls,
            hotel_id: int,
            name: str,
            price: int,
            quantity: int,
            description: str,
            services: Optional[dict] = None
    ):
        async with async_session_maker() as session:
            query = select(Hotels).where(Hotels.id == hotel_id)
            result = await session.execute(query)
            hotel_exists = result.scalar_one_or_none()
            if hotel_exists:
                query = select(Rooms).where(Rooms.name == name)
                result = await session.execute(query)
                room_exists = result.scalar_one_or_none()

                if not room_exists:
                    new_room = Rooms(hotel_id=hotel_id, name=name, price=price, quantity=quantity, services=services, description=description)
                    session.add(new_room)
                    await session.commit()
                    await session.refresh(new_room)
                    return new_room
                else:
                    raise RoomAlreadyExistsException
            else:
                raise HotelIsNotPresentException