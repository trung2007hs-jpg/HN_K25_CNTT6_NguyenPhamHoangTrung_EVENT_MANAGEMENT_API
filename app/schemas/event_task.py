from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserResponse

class EventTaskPriority(str, Enum):
    LOW  = 'LOW'
    MEDIUM  = 'MEDIUM'
    HIGH = 'HIGH'
    
class EventTaskStatus(str, Enum):
    TODO  = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    
class EventTaskCreate(BaseModel):
    title: str = Field(...)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: EventTaskStatus = Field(...)
    priority: EventTaskPriority = Field(...)
    due_date: Optional[datetime] = None 


class EventTaskBase(EventTaskCreate):
    id: int
    event_id: int
    created_at: datetime

class EventTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None

class EventTaskResponse(EventTaskBase):
    assignee: Optional[UserResponse] = None
    model_config = ConfigDict(from_attributes=True)