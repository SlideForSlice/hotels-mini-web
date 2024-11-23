from fastapi import APIRouter
from app.exceptions import *
from app.rooms.dao import RoomsDAO
from app.rooms.schemas import SRooms

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
