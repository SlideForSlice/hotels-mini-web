from typing import Optional
from pydantic import BaseModel



class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Optional[dict] = None
    quantity: int
    image_id: Optional[int] = None


    class Config:
        from_attributes = True