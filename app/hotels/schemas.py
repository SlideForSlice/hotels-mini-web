from typing import Optional
from pydantic import BaseModel



class SHotel(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[dict] = None
    rooms_quantity: int
    image_id: Optional[int] = None

    class Config:
        from_attributes = True