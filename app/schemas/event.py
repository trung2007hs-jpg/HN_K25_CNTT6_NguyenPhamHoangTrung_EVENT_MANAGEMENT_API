from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserBase
from app.schemas.event_staff import EventStaffResponse
from app.schemas.event_task import EventTaskBase

class EventBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema tạo Event mới
class EventCreate(BaseModel):
    name: str = Field(...)
    description: Optional[str] = None

# Schema cập nhật Event
class EventUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

# Schema trả về Event cơ bản
class EventResponse(EventBase):
    id: int
    created_at: datetime
    owner: Optional[UserBase] = Field(default=None, validation_alias="user")

    model_config = ConfigDict(from_attributes=True)

# Schema trả về Event chi tiết (kèm danh sách Staff và Tasks)
class EventDetailResponse(EventResponse):
    staffs: List[EventStaffResponse] = Field(default_factory=list)
    tasks: List[EventTaskBase] = Field(default_factory=list)