from datetime import date
from typing import Optional

import time
import sentry_sdk

from fastapi import Depends, FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router
from fastapi_versioning import VersionedFastAPI
from starlette.middleware import Middleware


from app.logger import logger

app = FastAPI()

sentry_sdk.init(
    dsn="https://examplePublicKey@o0.ingest.sentry.io/0",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)



app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)

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

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    description='Greet users with a nice message',
    middleware=[
        Middleware(SessionMiddleware, secret_key='mysecretkey')
    ]
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time,4)
    })
    return response


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)


# app.mount("/static", StaticFiles(directory="app/static"), name="static")