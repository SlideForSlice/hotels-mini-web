from datetime import date
from types import NoneType

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.logger import logger
from app.bookings.model import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.rooms.model import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ):
        try:
            async with async_session_maker() as session:

                booked_rooms = select(Bookings).where(
                    and_(
                        Bookings.user_id == user_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from
                            )
                        )
                    )
                ).cte("booked_rooms")

                get_rooms_left = select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label("rooms_left")
                ).select_from(Rooms).join(
                    booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == room_id).group_by(Rooms.quantity, booked_rooms.c.room_id)

                # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

                rooms_left = await session.execute(get_rooms_left)
                rooms_left = rooms_left.scalar_one_or_none()

                if not isinstance(rooms_left, NoneType):
                    if rooms_left > 0:

                        get_price = select(Rooms.price).filter_by(id=room_id)
                        price = await session.execute(get_price)
                        price: int = price.scalar()

                        add_booking = insert(Bookings).values(
                            user_id=user_id,
                            room_id=room_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price
                        ).returning(Bookings)

                        new_booking = await session.execute(add_booking)
                        await session.commit()
                        return new_booking.scalar()

                    else:
                        return None
                else:
                    return None
        except (SQLAlchemyError, Exception) as e:
            error_type = "DB Error" if isinstance(e, SQLAlchemyError) else "Unknown Error"
            error_message = f"{error_type}: Cannot add Booking"
            extra = {
                "user_id": user_id,
                "room_id": room_id,
                "date_from" : date_from ,
                "date_to": date_to ,
            }
            logger.error(
                error_message, extra=extra, exc_info=True
            )