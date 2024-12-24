from datetime import date
from typing import Optional

from app.dao.base import BaseDAO
from app.bookings.model import Bookings
from sqlalchemy import select, and_, or_

from app.database import async_session_maker
from app.exceptions import HotelAlreadyExistsException
from app.hotels.model import Hotels
from app.rooms.model import Rooms

class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def add(
            cls,
            name: str,
            location: str,
            rooms_quantity: int,
            services: Optional[dict] = None,
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

    @classmethod
    async def find_all(
            cls,
            location: str,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:

            # Запрос для поиска отелей по местоположению и свободным комнатам
            query = select(Hotels).join(Rooms).outerjoin(Bookings).where(
                and_(
                    Hotels.location == location,
                    or_(
                        Bookings.date_from.is_(None),
                        Bookings.date_to.is_(None),
                        or_(
                            Bookings.date_to <= date_from,
                            Bookings.date_from >= date_to
                        )
                    )
                )
            )

            result = await session.execute(query)
            hotels = result.scalars().all()

            return hotels

    @classmethod
    async def find_by_id_and_date(
            cls,
            hotel_id: int,
            date_from: date,
            date_to: date
    ):
        async with async_session_maker() as session:
            # Получаем все комнаты отеля с указанным hotel_id
            stmt = select(Rooms).where(
                Rooms.hotel_id == hotel_id,
                Rooms.id.notin_(select(Bookings.room_id).where(
                    and_(
                        Bookings.date_from < date_to,
                        Bookings.date_to > date_from
                    )
                ))
            )
            result = await session.execute(stmt)
            rooms = result.scalars().all()  # Получаем список свободных комнат

            return rooms





