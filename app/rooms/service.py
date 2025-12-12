from datetime import date

from sqlalchemy import func, literal_column, select

from app.bookings.models import Bookings
from app.core.database import async_session_maker
from app.rooms.models import Rooms
from app.rooms.schemas import SRoomsPeriod
from app.services.base import BaseService


class RoomsService(BaseService):
    model = Rooms

    @classmethod
    async def get_available_rooms_now(cls, hotel_id: int) -> list[Rooms]:
        async with async_session_maker() as session:
            booked_rooms = select(Bookings.room_id).where(
                Bookings.date_from <= func.current_date(),
                Bookings.date_to >= func.current_date(),
            )
            available_rooms = (
                select(Rooms)
                .where(Rooms.hotel_id == hotel_id)
                .where(Rooms.id.not_in(booked_rooms))
            )

            result = await session.execute(available_rooms)
            return result.scalars().all()

    @classmethod
    async def get_available_rooms_for_period(
        cls, hotel_id: int, date_from: date, date_to: date
    ) -> list[SRoomsPeriod]:
        async with async_session_maker() as session:
            booked_rooms_subq = select(Bookings.room_id).where(
                Bookings.date_from <= date_to, Bookings.date_to >= date_from
            )

            total_days = (date_to - date_from).days
            total_cost_expr = total_days * Rooms.price

            available_rooms = (
                select(
                    Rooms.id,
                    Rooms.hotel_id,
                    Rooms.name,
                    Rooms.description,
                    Rooms.price,
                    Rooms.services,
                    Rooms.quantity,
                    Rooms.image_id,
                    literal_column(str(total_days)).label("total_days"),
                    total_cost_expr.label("total_cost"),
                )
                .where(Rooms.hotel_id == hotel_id)
                .where(Rooms.id.not_in(booked_rooms_subq))
            )

            result = await session.execute(available_rooms)
            return [SRoomsPeriod(**row) for row in result.mappings()]
