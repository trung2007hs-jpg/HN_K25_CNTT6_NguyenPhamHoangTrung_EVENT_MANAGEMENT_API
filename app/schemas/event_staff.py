from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserBase

class EventStaffBase(BaseModel):
    role: str 

# Schema cho request thêm nhân sự vào sự kiện
class EventStaffCreate(EventStaffBase):
    user_id: int

# Schema cho request cập nhật vai trò nhân sự
class EventStaffUpdate(BaseModel):
    role: str

# Schema trả về thông tin nhân sự kèm chi tiết User
class EventStaffResponse(EventStaffBase):
    event_id: int
    user_id: int
    joined_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class UserInEventStaffResponse(EventStaffResponse):
    user: Optional[UserBase] = None
    model_config = ConfigDict(from_attributes=True)