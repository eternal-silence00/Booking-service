import os
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from booking_service.main import app
from booking_service.core.database import get_db
from booking_service.core.base import Base
import booking_service.users.models
import booking_service.rooms.models
import booking_service.bookings.models
from sqlalchemy import text

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/booking_test",
)

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    
async def override_get_db():
    engine = create_async_engine(TEST_DATABASE_URL)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        
@pytest.fixture(scope="session")
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()
    
@pytest.fixture
async def user_token(async_client):
    await async_client.post("/auth/register", json={"email": "user@test.com", "password": "test12345"})
    resp = await async_client.post("/auth/login", json={"email": "user@test.com", "password": "test12345"})
    return resp.json()["access_token"]

@pytest.fixture
async def admin_token(async_client):
    await async_client.post("/auth/register", json={"email": "admin@test.com", "password": "test12345"})
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("UPDATE users SET role='ADMIN' WHERE email='admin@test.com'"))
    await engine.dispose()
    resp = await async_client.post("/auth/login", json={"email": "admin@test.com", "password": "test12345"})
    return resp.json()["access_token"]

@pytest.fixture(autouse=True)
async def clean_db():
    yield
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE users, rooms, slots, bookings RESTART IDENTITY CASCADE"))
    await engine.dispose()