from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.event_task import EventTaskCreate
from app.schemas.response import BaseResponseSchema
from app.schemas.event_task import EventTaskResponse
from app.services.event_task import create_task_service


event_task_router = APIRouter(tags=['Công việc sự kiện'])

@event_task_router.post('/events/{event_id}/event-tasks', response_model=BaseResponseSchema[EventTaskResponse], status_code=status.HTTP_201_CREATED)
def create_task(
    request: Request,
    new_task: EventTaskCreate,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = create_task_service(db=db, new_task=new_task, event_id=event_id)
    return BaseResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message='Tạo công việc thành công',
        data=data,
        path=request.url.path
    )