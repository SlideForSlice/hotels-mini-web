from datetime import date

from fastapi import APIRouter, Request, Depends, HTTPException
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import *
from app.hotels.dao import HotelsDAO
from app.hotels.model import Hotels
from app.hotels.schemas import SHotel
from app.users.model import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)

@router.get("")
async def get_hotels(location: str) -> list[SHotel]:
    return await HotelsDAO.find_all(location=location)

@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> SHotel:
    result =  await HotelsDAO.find_by_id(hotel_id)
    if not result:
        raise HotelIsNotPresentException
    else:
        return result

@router.post("/add_hotel")
async def add_hotel(
        name: str,
        location: str,
        rooms_quantity: int,
        services: dict = None
) -> SHotel:
    return await HotelsDAO.add(name, location, rooms_quantity, services)

@router.patch("/add_services/{hotel_id}")
async def add_services(
        hotel_id: int,
        services: dict
) -> SHotel:
    updated_hotel = await HotelsDAO.update(id=hotel_id, services=services)
    if not updated_hotel:
        raise HotelAlreadyExistsException
    else:
        return updated_hotel


@router.delete("/{hotel_id}")
async def delete_hotel_by_id(hotel_id: int) -> str:
    result = await HotelsDAO.delete(hotel_id)
    if not result:
        raise HotelIsNotPresentException
    else:
        return "Hotel was deleted"
