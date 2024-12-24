from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, Query,Depends
from datetime import date
from app.bookings.router import router as bookings_router
from app.users.router import router as users_router
from app.pages.router import router as pages_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router
from app.images.router import router as images_router
app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(pages_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(images_router)

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
