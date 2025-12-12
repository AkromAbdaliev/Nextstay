from datetime import date

from fastapi import APIRouter, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.core.exceptions import RoomNotFoundException
from app.rooms.schemas import SRooms, SRoomsPeriod
from app.rooms.service import RoomsService

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.get("/available", response_model=list[SRooms])
async def get_rooms(hotel_id: int):
    return await RoomsService.get_available_rooms_now(hotel_id)


@router.get("/available/period", response_model=list[SRoomsPeriod])
@cache(expire=60)
async def get_rooms_for_period(hotel_id: int, date_from: date, date_to: date):
    return await RoomsService.get_available_rooms_for_period(
        hotel_id, date_from, date_to
    )


@router.get("/rooms", response_model=list[SRooms])
async def get_all_rooms(hotel_id: int):
    return await RoomsService.find_all(hotel_id=hotel_id)


@router.post("/rooms", response_model=SRooms)
async def create_room(hotel_id: int, room: SRooms):
    await FastAPICache.clear()
    return await RoomsService.add_one(hotel_id=hotel_id, **room.model_dump())


@router.put("/{room_id}", response_model=SRooms)
async def update_room(room_id: int, room: SRooms):
    existing_room = await RoomsService.find_by_id(room_id)
    if not existing_room:
        raise RoomNotFoundException

    updated_room = await RoomsService.update_one(existing_room, **room.model_dump())
    await FastAPICache.clear()
    return SRooms.model_validate(updated_room)


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_room(room_id: int):
    existing_room = await RoomsService.find_by_id(room_id)
    if not existing_room:
        raise RoomNotFoundException
    await RoomsService.delete_one(existing_room)
    await FastAPICache.clear()
