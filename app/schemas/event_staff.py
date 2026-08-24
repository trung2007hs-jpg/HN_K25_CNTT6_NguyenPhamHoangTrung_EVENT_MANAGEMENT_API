from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserBase

class EventStaffRole(str, Enum):
    MEMBER = "MEMBER"
    OWNER = "OWNER"

class EventStaffBase(BaseModel):
    role: EventStaffRole = Field(..., description="Vai trò của nhân sự trong sự kiện")

# Schema cho request thêm nhân sự vào sự kiện
class EventStaffCreate(EventStaffBase):
    user_id: int = Field(..., description="ID của User cần thêm vào sự kiện")

# Schema trả về thông tin nhân sự kèm chi tiết User
class EventStaffResponse(EventStaffBase):
    event_id: int
    user_id: int
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class UserInEventStaffResponse(EventStaffResponse):
    user: Optional[UserBase] = None
    model_config = ConfigDict(from_attributes=True)