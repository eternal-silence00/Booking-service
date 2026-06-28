from pydantic import ConfigDict, BaseModel, Field, model_validator
from datetime import time

class RoomCreate(BaseModel):
    
    name: str = Field(..., max_length=100)
    capacity: int = Field(..., gt=0)
    
class RoomResponse(BaseModel):
    id: int
    name: str
    capacity: int
    
    model_config = ConfigDict(from_attributes=True)
  

class SlotCreate(BaseModel):
    start_time: time = Field(..., description="Start time of the slot")
    end_time: time = Field(..., description="End time of the slot")
    
    @model_validator(mode="after")
    def check_times(self):
        self.start_time = self.start_time.replace(second=0, microsecond=0)
        self.end_time = self.end_time.replace(second=0, microsecond=0)
        if self.start_time >= self.end_time:
            raise ValueError("Start time must be before end time")
        return self

class SlotResponse(BaseModel):
    id: int
    room_id: int
    start_time: time
    end_time: time

    model_config = ConfigDict(from_attributes=True)