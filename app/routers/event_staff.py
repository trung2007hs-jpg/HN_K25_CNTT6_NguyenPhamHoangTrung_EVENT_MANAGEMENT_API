from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.user import User
from app.schemas.event_staff import EventStaffCreate, UserInEventStaffResponse
from app.schemas.response import ResponseSchema
from app.services.event_staff import (
    add_member_service, 
    get_list_members_event_service,
    remove_member_service
)

event_staff_router = APIRouter(prefix="/events/{event_id}/members", tags=["Member"])

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
    
@event_staff_router.get("/", response_model=ResponseSchema[list[UserInEventStaffResponse]])
def get_list_members_event(
    event_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    members = get_list_members_event_service(db=db, event_id=event_id, user_id=current_user.id)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Lấy danh sách thành viên sự kiện thành công",
        data=members,
        path=request.url.path,
    )
    
@event_staff_router.delete("/{user_id}", response_model=ResponseSchema[UserInEventStaffResponse])
def remove_member(  
    event_id: int,
    user_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    member = remove_member_service(db=db, event_id=event_id, owner_id=current_user.id, member_id=user_id)
    return ResponseSchema(
        status_code=status.HTTP_200_OK,
        message="Xóa thành viên khỏi sự kiện thành công",
        data=member,
        path=request.url.path,
    )
    