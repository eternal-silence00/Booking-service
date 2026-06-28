from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from sqlalchemy import select
from booking_service.bookings.models import Booking


class BookingRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_booking(self, user_id: int, slot_id: int, booking_date: date):
        booking = Booking(user_id=user_id, slot_id=slot_id, booking_date=booking_date)
        self.session.add(booking)
        await self.session.flush()
        await self.session.refresh(booking)
        return booking
    
    async def get_by_id(self, booking_id: int):
        result = await self.session.execute(select(Booking).where(Booking.id == booking_id))
        return result.scalar_one_or_none()
    
    async def get_by_user_id(self, user_id: int):
        result = await self.session.execute(select(Booking).where(Booking.user_id == user_id))
        return result.scalars().all()
    
    async def delete(self, booking: Booking):
        await self.session.delete(booking)
        await self.session.flush()
        
    async def get_by_slot_and_date(self, slot_id: int, booking_date: date):
        result = await self.session.execute(
            select(Booking).where(
                Booking.slot_id == slot_id,
                Booking.booking_date == booking_date
            )
        )
        return result.scalar_one_or_none()
    
    async def get_all_by_date(self, booking_date: date):
        result = await self.session.execute(select(Booking).where(Booking.booking_date == booking_date))
        return result.scalars().all()