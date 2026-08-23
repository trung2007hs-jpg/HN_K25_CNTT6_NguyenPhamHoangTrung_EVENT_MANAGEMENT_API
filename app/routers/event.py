from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.event import EventCreate, EventResponse
from app.schemas.response import ResponseSchema
from app.schemas.user import UserBase
from app.services.event import create_event_service

event_router = APIRouter(prefix="/events", tags=["Event"])


@event_router.post("/", response_model=ResponseSchema[EventResponse])
def create_event(
        event_in: EventCreate,
        request: Request,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):
    event = create_event_service(db=db, event_in=event_in, user_id=current_user.id)
    return ResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message="Tạo sự kiện thành công",
        data=event,
        path=request.url.path,
    )