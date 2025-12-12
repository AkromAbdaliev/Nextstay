from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from app.admin.auth import authentication_backend
from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.core.config import settings
from app.core.database import engine
from app.hotels.router import router as hotels_router
from app.rooms.router import router as rooms_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=3600,
)
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)


@app.get("/")
def welcome():
    return {"Welcome to Hotel Bookings"}


admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(HotelAdmin)
admin.add_view(RoomAdmin)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
