from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_book = await BookingDAO.add(
        user_id=1,
        room_id=1,
        date_from=datetime.strptime("2024-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-07-24", "%Y-%m-%d"),
    )

    assert new_book.user_id == 1
    assert new_book.room_id == 1

    new_book_id = await BookingDAO.find_by_id(new_book.id)

    assert new_book_id is not None