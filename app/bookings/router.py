from datetime import date

from fastapi import APIRouter, Depends

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import *
from app.users.dependencies import get_current_user
from app.users.model import Users
from fastapi_versioning import version

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("")
@version(1)
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
@version(1)
async def add_booking(
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
) -> SBooking:
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCanNotBeBookedException
    else:
        return booking

@router.delete("/{booikin_id}")
@version(1)
async def delete_booking_by_id(booikin_id: int) -> str:
    result = await BookingDAO.delete(booikin_id)
    if not result:
        raise BookingIsNotPresentException
    else:
        return "Booking was deleted"

