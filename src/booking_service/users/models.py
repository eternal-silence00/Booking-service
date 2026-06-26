from enum import StrEnum
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from booking_service.core.base import Base
from datetime import datetime, timezone

class Role(StrEnum):
    EMPLOYEE = "employee"
    ADMIN = "admin"
    
class User(Base):
    
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[Role] = mapped_column(default=Role.EMPLOYEE, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))