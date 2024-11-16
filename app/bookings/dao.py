from app.dao.base import BaseDAO
from app.bookings.model import Bookings


class BookingDAO(BaseDAO):
    model = Bookings


