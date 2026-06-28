from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.bookings.repository import BookingRepository
from booking_service.rooms.repository import RoomRepository
from booking_service.bookings.schemas import BookingCreate
from booking_service.users.models import User, Role
from fastapi import HTTPException



class BookingService:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.booking_repo = BookingRepository(self.session)
        self.room_repo = RoomRepository(self.session)

    async def create_booking(self, user_id: int, booking_data: BookingCreate):
        slot = await self.room_repo.get_slot_by_id(booking_data.slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        existing_booking = await self.booking_repo.get_by_slot_and_date(booking_data.slot_id, booking_data.booking_date)
        if existing_booking:
            raise HTTPException(status_code=409, detail="Booking already exists for this slot and date")
        return await self.booking_repo.create_booking(user_id=user_id, slot_id=booking_data.slot_id, booking_date=booking_data.booking_date)
    
    async def get_my_bookings(self, user_id: int):
        return await self.booking_repo.get_by_user_id(user_id)
    
    async def cancel_booking(self, booking_id: int, current_user: User):
        booking_exists = await self.booking_repo.get_by_id(booking_id)
        if not booking_exists:
            raise HTTPException(status_code=404, detail="Booking not found")
        if booking_exists.user_id != current_user.id and current_user.role != Role.ADMIN:
            raise HTTPException(status_code=403, detail="Not allowed to cancel this booking")
        return await self.booking_repo.delete(booking_exists)