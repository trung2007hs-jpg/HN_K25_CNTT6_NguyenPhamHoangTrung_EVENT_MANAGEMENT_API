from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.user import UserResponse
from schemas.event_staff import EventStaffResponse
from schemas.event_task import EventTaskResponse

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema tạo Event mới
class EventCreate(EventBase):
    pass

# Schema cập nhật Event
class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Schema trả về Event cơ bản
class EventResponse(EventBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: Optional[UserResponse] = None

    class Config:
        from_attributes = True

# Schema trả về Event chi tiết (kèm danh sách Staff và Tasks)
class EventDetailResponse(EventResponse):
    staffs: List[EventStaffResponse] = []
    tasks: List[EventTaskResponse] = []