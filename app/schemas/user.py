from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class SearchUser(str, Enum):
    EMAIL = 'email'
    FULLNAME = 'fullname'
    

class UserBase(BaseModel):
    id: int
    email: EmailStr

# Schema dùng khi Admin tạo User hoặc Cập nhật Profile
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
        
class EventInUser(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime