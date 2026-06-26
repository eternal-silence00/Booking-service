from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.core.database import get_db
from booking_service.users.service import AuthService
from booking_service.users.schemas import UserCreate, UserResponse, Token

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, session: AsyncSession = Depends(get_db)):
    return await AuthService(session).register(data)

@router.post("/auth/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_db)):
    return await AuthService(session).login(data)