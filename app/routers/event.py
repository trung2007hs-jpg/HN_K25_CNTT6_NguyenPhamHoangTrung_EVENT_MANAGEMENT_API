from typing import Optional
from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.event import EventCreate, EventDetailResponse, EventResponse, EventUpdate
from app.schemas.response import ResponseSchema
from app.schemas.user import UserBase, EventInUser
from app.services.event import (
    create_event_service,
    get_event_detail_service,
    get_events_service,
    update_event_service,
    delete_event_service,
)

event_router = APIRouter(prefix="/events", tags=["Sự kiện"])

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
    
@event_router.get('/', response_model=ResponseSchema[list[EventInUser]])
def get_events(
    request: Request, 
    search: Optional[str] = Query(default=None),
    current_user: User = Depends(get_current_user), 
    db: Session=Depends(get_db)
):
    events = get_events_service(db=db, user_id=current_user.id, search=search)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message='Lấy danh sách sự kiện thành công',
        data=events,
        path=request.url.path
    )

@event_router.get("/{event_id}", response_model=ResponseSchema[EventDetailResponse])
def get_event_detail(
    event_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = get_event_detail_service(db=db, event_id=event_id, user_id=current_user.id,)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Lấy chi tiết sự kiện thành công",
        data=event,
        path=request.url.path,
    )
    
@event_router.patch("/{event_id}", response_model=ResponseSchema[EventResponse])
def update_event(
    event_id: int,
    event_update: EventUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = update_event_service(db=db, event_id=event_id, user_id=current_user.id, event_update=event_update)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Cập nhật sự kiện thành công",
        data=event,
        path=request.url.path,
    )

@event_router.delete("/{event_id}", response_model=ResponseSchema[EventResponse])
def delete_event(
    event_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    event = delete_event_service(db=db, event_id=event_id, user_id=current_user.id)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Xóa sự kiện thành công",
        data=event,
        path=request.url.path,
    )