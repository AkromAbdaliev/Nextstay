from fastapi import APIRouter, Depends, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from app.bookings.schemas import SBookingsCreate, SBookingsRead
from app.bookings.service import BookingsService
from app.core.exceptions import BookingNotFoundException
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.schemas import SUserRead

router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("", response_model=list[SBookingsRead])
@cache(expire=120)
async def get_bookings(
    user: SUserRead = Depends(get_current_user),
) -> list[SBookingsRead]:
    return await BookingsService.find_all(user_id=user.id)


@router.get("/{booking_id}", response_model=SBookingsRead)
async def get_booking(
    booking_id: int, user: SUserRead = Depends(get_current_user)
) -> SBookingsRead:
    booking = await BookingsService.find_by_id(booking_id)
    if not booking or booking.user_id != user.id:
        raise BookingNotFoundException
    return booking


@router.post("", response_model=SBookingsRead)
async def create_one(
    booking: SBookingsCreate, user: SUserRead = Depends(get_current_user)
):
    await FastAPICache.clear()
    booking = await BookingsService.add_booking(booking=booking, user_id=user.id)
    booking_dict = booking.model_dump()
    send_booking_confirmation_email.delay(booking_dict, user.email)
    return booking


@router.put("/{booking_id}", response_model=SBookingsRead)
async def update_booking(
    booking_id: int,
    booking_data: SBookingsCreate,
    user: SUserRead = Depends(get_current_user),
):
    existing_booking = await BookingsService.find_by_id(booking_id)
    if not existing_booking or existing_booking.user_id != user.id:
        raise BookingNotFoundException

    updated_booking = await BookingsService.update_one(
        existing_booking, **booking_data.model_dump()
    )
    await FastAPICache.clear()
    return updated_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(booking_id: int, user: SUserRead = Depends(get_current_user)):
    existing_booking = await BookingsService.find_by_id(booking_id)
    if existing_booking and existing_booking.user_id == user.id:
        await BookingsService.delete_one(existing_booking)
        await FastAPICache.clear()
