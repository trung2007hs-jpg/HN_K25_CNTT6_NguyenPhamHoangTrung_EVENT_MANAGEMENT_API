from datetime import datetime
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class BaseResponseSchema(BaseModel, Generic[DataT]):
    status_code: int
    message: str
    data: Optional[DataT] = None
    errors: Optional[Any] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    path: str

class ResponseSchema(BaseResponseSchema[DataT], Generic[DataT]):
    status_code: int = 200
    message: str = "Success"

class ErrorResponseSchema(BaseResponseSchema[None]):
    status_code: int = 400
    message: str = "Error"
    
class TokenData(BaseModel):
    access_token: str
    token_type: str

