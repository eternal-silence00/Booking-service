from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.rooms.repository import RoomRepository
from booking_service.rooms.schemas import RoomCreate, SlotCreate
from fastapi import HTTPException

class RoomService:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = RoomRepository(session)
        
    async def create_room(self, data: RoomCreate):
        room = await self.repo.create_room(name=data.name, capacity=data.capacity)
        return room
    
    async def get_all_rooms(self):
        result = await self.repo.get_all_rooms()
        return result
    
    async def create_slot(self, data: SlotCreate, room_id: int):
        room = await self.repo.get_room_by_id(room_id=room_id)
        if not room: 
            raise HTTPException(status_code=404, detail="Room not found")
        slot = await self.repo.create_slot(room_id=room_id, start_time=data.start_time, end_time=data.end_time)
        return slot
    
    async def get_room_slots(self, room_id: int):
        room = await self.repo.get_room_by_id(room_id=room_id)
        if not room: 
            raise HTTPException(status_code=404, detail="Room not found")
        result = await self.repo.get_all_room_slots(room_id=room_id)
        return result