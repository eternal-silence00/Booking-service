from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from booking_service.rooms.models import Room, Slot
from datetime import time


class RoomRepository:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_room(self, name: str, capacity: int):
        room = Room(name=name, capacity=capacity)
        self.session.add(room)
        await self.session.flush()
        await self.session.refresh(room)
        return room 
    
    async def get_all_rooms(self):
        result = await self.session.execute(select(Room))
        return result.scalars().all()
    
    async def get_room_by_id(self, room_id: int):
        result = await self.session.execute(select(Room).where(Room.id == room_id))
        return result.scalar_one_or_none() 
    
    async def create_slot(self, room_id: int, start_time: time, end_time: time):
        slot = Slot(room_id=room_id, start_time=start_time, end_time=end_time)
        self.session.add(slot)
        await self.session.flush()
        await self.session.refresh(slot)
        return slot
    
    async def get_all_room_slots(self, room_id: int):
        result = await self.session.execute(select(Slot).where(Slot.room_id == room_id))
        return result.scalars().all()
    
    async def get_slot_by_id(self, slot_id: int):
        result = await self.session.execute(select(Slot).where(Slot.id == slot_id))
        return result.scalar_one_or_none()