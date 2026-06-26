from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from booking_service.core.base import Base
from datetime import time

class Room(Base):
    
    __tablename__ = "rooms"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    capacity: Mapped[int] = mapped_column(nullable=False)
    
    slots: Mapped[list["Slot"]] = relationship(back_populates="room")
    

class Slot(Base):
    
    __tablename__ = "slots"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time: Mapped[time] = mapped_column(nullable=False)
    end_time: Mapped[time] = mapped_column(nullable=False)
    
    room: Mapped["Room"] = relationship(back_populates="slots")