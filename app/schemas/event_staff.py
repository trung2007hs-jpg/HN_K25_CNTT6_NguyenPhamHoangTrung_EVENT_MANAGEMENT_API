from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse

class EventStaffBase(BaseModel):
    role: Optional[str] = "STAFF"

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
    user: Optional[UserResponse] = None

    class Config:
        from_attributes = True