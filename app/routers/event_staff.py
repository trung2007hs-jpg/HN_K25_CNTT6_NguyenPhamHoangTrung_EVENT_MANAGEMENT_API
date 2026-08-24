from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.user import User
from app.schemas.event_staff import EventStaffCreate, UserInEventStaffResponse
from app.schemas.response import ResponseSchema
from app.services.event_staff import add_member_service

event_staff_router = APIRouter(prefix="/events/{event_id}/members", tags=["Event Staff"])

@event_staff_router.post("/", response_model=ResponseSchema[UserInEventStaffResponse], status_code=status.HTTP_201_CREATED)
def add_member(
    event_id: int,
    new_event_staff: EventStaffCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = add_member_service(db=db, event_id=event_id, owner_id=current_user.id, new_event_staff=new_event_staff)
    return ResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message="Thêm thành viên vào sự kiện thành công",
        data=member,
        path=request.url.path,
    )