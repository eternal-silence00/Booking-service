from fastapi import APIRouter, Depends
from booking_service.rooms.schemas import RoomCreate, SlotCreate, RoomResponse, SlotResponse
from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.users.models import User
from booking_service.core.security import get_admin_user, get_current_user
from booking_service.rooms.service import RoomService
from booking_service.core.database import get_db


router = APIRouter()

@router.post("/rooms", response_model=RoomResponse, status_code=201)
async def create_room(
    data: RoomCreate,
    session: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
    ):
    return await RoomService(session).create_room(data)


@router.get("/rooms", response_model=list[RoomResponse])
async def get_rooms(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    return await RoomService(session).get_all_rooms()

@router.post("/rooms/{room_id}/slots", response_model=SlotResponse, status_code=201)
async def create_slot(
    room_id: int,
    data: SlotCreate,
    session: AsyncSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    return await RoomService(session).create_slot(room_id=room_id, data=data)

@router.get("/rooms/{room_id}/slots", response_model=list[SlotResponse])
async def get_room_slots(
    room_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return await RoomService(session).get_room_slots(room_id)