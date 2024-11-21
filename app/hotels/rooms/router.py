from datetime import date
from typing import Optional

from fastapi import APIRouter, Request, Depends, HTTPException
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking
from app.exceptions import *
from app.hotels.dao import HotelsDAO
from app.hotels.model import Hotels
from app.hotels.rooms.dao import RoomsDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.schemas import SHotel
from app.users.model import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

@router.get("")
async def get_rooms(hotel_id: int) -> list[SRooms]:
    return await RoomsDAO.find_all(hotel_id=hotel_id)

@router.get("/{room_id}")
async def get_room_by_id(hotel_id: int) -> SRooms:
    result = await RoomsDAO.find_by_id(hotel_id)
    if not result:
        raise RoomIsNotPresentException
    else:
        return result

@router.post("/add_room")
async def add_room(
        hotel_id: int,
        name: str,
        price: int,
        quantity: int,
        description: str,
        services: dict = None
) -> SRooms:
    return await RoomsDAO.add(hotel_id, name, price, quantity, description, services)

@router.patch("/add_services/{room_id}")
async def add_services(
        room_id: int,
        services: dict
) -> SRooms:
    updated_room = await RoomsDAO.update(id=room_id, services=services)
    if not updated_room:
        raise RoomIsNotPresentException
    else:
        return updated_room

@router.delete("/{room_id}")
async def delete_room_by_id(room_id: int) -> str:
    result = await RoomsDAO.delete(room_id)
    if not result:
        raise RoomIsNotPresentException
    else:
        return "Room was deleted"
