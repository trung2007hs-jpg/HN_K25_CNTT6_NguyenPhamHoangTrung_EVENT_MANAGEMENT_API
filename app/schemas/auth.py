from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(...)

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    role: str

class RegisterUser(LoginUser):
    full_name: str = Field(...)