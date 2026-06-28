from fastapi import APIRouter, Depends, Query
from booking_service.bookings.service import BookingService
from booking_service.users.models import User
from booking_service.core.security import get_admin_user, get_current_user
from booking_service.core.database import get_db
from booking_service.bookings.schemas import BookingCreate, BookingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.rooms.schemas import RoomAvailability
from datetime import date

router = APIRouter()

@router.post("/bookings", response_model=BookingResponse, status_code=201)
async def create_booking(
    booking_data: BookingCreate,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    service = BookingService(session)
    return await service.create_booking(user_id=user.id, booking_data=booking_data)

@router.get("/bookings/me", response_model=list[BookingResponse])
async def get_my_bookings(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    service = BookingService(session)
    return await service.get_my_bookings(user_id=user.id)

@router.delete("/bookings/{booking_id}", status_code=204)
async def cancel_booking(
    booking_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    service = BookingService(session)
    await service.cancel_booking(booking_id=booking_id, current_user=user)
    return None

@router.get("/availability", response_model=list[RoomAvailability])
async def get_availability(
    booking_date: date = Query(..., alias="date"),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await BookingService(session).get_availability(booking_date)