from sqlalchemy.ext.asyncio import AsyncSession
from booking_service.users.repository import UserRepository
from fastapi import HTTPException
from booking_service.core.security import hash_password, verify_password, create_access_token
from booking_service.users.schemas import UserCreate



class AuthService:
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def register(
        self, 
        data: UserCreate,
        ):
        repo = UserRepository(self.session)
        email_exists = await repo.get_by_email(data.email)
        if email_exists:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = hash_password(data.password)
        user = await repo.create_user(data.email, hashed_password)
        return user
    
    async def login(
        self, 
        data: UserCreate,
    ):
        repo = UserRepository(self.session)
        user = await repo.get_by_email(data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        verified = verify_password(data.password, user.hashed_password)
        if not verified:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        access_token = create_access_token({"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}