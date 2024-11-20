from typing import Optional
from fastapi import FastAPI, Query,Depends
from datetime import date
from pydantic import BaseModel
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
app = FastAPI()

app.include_router(users_router)
app.include_router(bookings_router)


class HotelSearchArgs:
    def __init__(
            self,
            location: str,
            date_from: date,
            date_to: date,
            has_spa: Optional[bool] = None,
            stars: Optional[int] = Query(None, ge=0, le=5),
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get("hotels")
def get_hotels(
        search_args: HotelSearchArgs = Depends(),
):

    return search_args
