from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class BookingCreate(BaseModel):
    slot_id: int
    booking_date: date
    
class BookingResponse(BaseModel):
    id: int
    user_id: int
    slot_id: int
    booking_date: date
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)