from datetime import date
from types import NoneType

from app.dao.base import BaseDAO
from app.bookings.model import Bookings
from sqlalchemy import delete, insert, select, and_, or_, func

from app.database import engine, async_session_maker
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
            ).where(room_id == Rooms.id).group_by(Rooms.quantity, booked_rooms.c.room_id)

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

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
