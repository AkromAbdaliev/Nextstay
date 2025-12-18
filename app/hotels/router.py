from fastapi import APIRouter, status

from app.core.exceptions import HotelNotFoundException
from app.hotels.schemas import SHotels
from app.hotels.service import HotelsService

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=list[SHotels])
async def get_hotels():
    return await HotelsService.find_all()


@router.get("/{hotel_id}", response_model=SHotels)
async def get_hotel(hotel_id: int):
    hotel = await HotelsService.find_by_id(hotel_id)
    if not hotel:
        raise HotelNotFoundException
    return hotel


@router.post("/", response_model=SHotels)
async def create_one(hotel: SHotels):
    return await HotelsService.add_one(**hotel.model_dump())


@router.put("/{hotel_id}", response_model=SHotels)
async def update_hotel(hotel_id: int, hotel: SHotels):
    existing_hotel = await HotelsService.find_by_id(hotel_id)
    if not existing_hotel:
        raise HotelNotFoundException

    return await HotelsService.update_one(existing_hotel, **hotel.model_dump())


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_one(hotel_id: int):
    existing_hotel = await HotelsService.find_by_id(hotel_id)
    if not existing_hotel:
        raise HotelNotFoundException
    return await HotelsService.delete_one(existing_hotel)
