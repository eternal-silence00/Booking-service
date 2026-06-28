from fastapi import FastAPI
from booking_service.users.routers import router as auth_router
from booking_service.rooms.routers import router as room_service
from booking_service.bookings.routers import router as booking_router

app = FastAPI(title="Meeting Room Booking")

app.include_router(auth_router)
app.include_router(room_service)
app.include_router(booking_router)


@app.get("/health")
async def health():
    return {"status": "ok"}