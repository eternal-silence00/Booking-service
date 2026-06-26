from fastapi import FastAPI

app = FastAPI(title="Meeting Room Booking")

@app.get("/health")
async def health():
    return {"status": "ok"}