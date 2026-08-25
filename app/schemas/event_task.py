from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user import UserBase 

class TaskPriority(str, Enum):
    LOW  = 'LOW'
    MEDIUM  = 'MEDIUM'
    HIGH = 'HIGH'
    
class TaskStatus(str, Enum):
    TODO  = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    
class TaskSortField(str, Enum):
  CREATED_AT = "created_at"
  DUE_DATE = "due_date"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
    
class EventTaskCreate(BaseModel):
    title: str = Field(...)
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: TaskStatus = Field(...)
    priority: TaskPriority = Field(...)
    due_date: Optional[datetime] = None 


class EventTaskBase(EventTaskCreate):
    id: int
    event_id: int
    created_at: datetime

class EventTaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None

class EventTaskResponse(EventTaskBase):
    id: int
    event_id: int
    assignee: Optional[UserBase] = None
    event: Optional[EventInTask] = None
    model_config = ConfigDict(from_attributes=True)
    
class EventInTask(BaseModel):
    name: str
    description: Optional[str] = None
    
    