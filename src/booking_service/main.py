from fastapi import FastAPI
from booking_service.users.routers import router as auth_router

app = FastAPI(title="Meeting Room Booking")

app.include_router(auth_router)

@app.get("/health")
async def health():
    return {"status": "ok"}