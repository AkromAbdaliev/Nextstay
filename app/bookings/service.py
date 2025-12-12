from sqlalchemy import select

from app.bookings.models import Bookings
from app.bookings.schemas import SBookingsCreate, SBookingsRead
from app.core.database import async_session_maker
from app.core.exceptions import RoomCannotBeBookedException, RoomNotFoundException
from app.rooms.service import RoomsService
from app.services.base import BaseService


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def add_booking(cls, user_id: int, booking: SBookingsCreate) -> SBookingsRead:
        room = await RoomsService.find_one_or_none(id=booking.room_id)
        if not room:
            raise RoomNotFoundException

        data = {
            "room_id": booking.room_id,
            "user_id": user_id,
            "date_from": booking.date_from,
            "date_to": booking.date_to,
            "price": room.price,
        }
        # prevent overlapping bookings for the same room
        async with async_session_maker() as session:
            query = (
                select(Bookings)
                .where(Bookings.room_id == booking.room_id)
                .where(Bookings.date_from <= booking.date_to)
                .where(Bookings.date_to >= booking.date_from)
            )
            resp = await session.execute(query)
            existing = resp.scalar_one_or_none()
            if existing:
                raise RoomCannotBeBookedException

        created_booking = await BookingsService.add_one(**data)
        return SBookingsRead.model_validate(created_booking)
