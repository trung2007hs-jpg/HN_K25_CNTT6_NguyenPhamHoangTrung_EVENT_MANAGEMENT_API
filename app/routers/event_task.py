from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.event_task import (
    EventTaskCreate,
    EventTaskResponse,
    SortOrder,
    TaskPriority,
    TaskSortField,
    TaskStatus,
)
from app.schemas.response import BaseResponseSchema
from app.services.event_task import (
    create_task_service, 
    delete_event_task_service,
    filter_event_tasks_service,
    get_event_task_by_id_service,
    update_event_task_service,
)


event_task_router = APIRouter(tags=['Công việc sự kiện'])

@event_task_router.post('/events/{event_id}/event-tasks', response_model=BaseResponseSchema[EventTaskResponse], status_code=status.HTTP_201_CREATED)
def create_task(
    request: Request,
    new_task: EventTaskCreate,
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = create_task_service(db=db, new_task=new_task, event_id=event_id, user_id=current_user.id)
    return BaseResponseSchema(
        status_code=status.HTTP_201_CREATED,
        message='Tạo công việc thành công',
        data=data,
        path=request.url.path
    )
    
@event_task_router.get('/events/{event_id}/event-tasks', response_model=BaseResponseSchema[list[EventTaskResponse]],  status_code=status.HTTP_200_OK,)
def get_event_tasks(
    event_id: int,
    request: Request,
    status_filter: Optional[TaskStatus] = Query(default=None, alias='status'),
    priority_filter: Optional[TaskPriority] = Query(default=None, alias='priority'),
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: TaskSortField = TaskSortField.CREATED_AT,
    order: SortOrder = SortOrder.DESC,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = filter_event_tasks_service(
        db=db,
        event_id=event_id,
        user_id=current_user.id,
        status_filter=status_filter,
        priority_filter=priority_filter,
        assignee_id=assignee_id,
        search=search,
        sort_by=sort_by,
        order=order,
        limit=limit,
        offset=offset,
    )
    return BaseResponseSchema(
        status_code=status.HTTP_200_OK,
        message='Lấy danh sách công việc thành công',
        data=data,
        path=request.url.path,
    )
    
@event_task_router.get('/event-tasks/{task_id}', response_model=BaseResponseSchema[EventTaskResponse], status_code=status.HTTP_200_OK)
def get_event_task_by_id(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = get_event_task_by_id_service(db=db, task_id=task_id, user_id=current_user.id)
    return BaseResponseSchema(
        status_code=status.HTTP_200_OK,
        message='Lấy thông tin công việc thành công',
        data=data,
        path=request.url.path,
    )
    
@event_task_router.patch('/event-tasks/{task_id}', response_model=BaseResponseSchema[EventTaskResponse], status_code=status.HTTP_200_OK)
def update_event_task(
    task_id: int,
    task_update: EventTaskCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = update_event_task_service(db=db, task_id=task_id, user_id=current_user.id, task_update=task_update)
    return BaseResponseSchema(
        status_code=status.HTTP_200_OK,
        message='Cập nhật công việc thành công',
        data=data,
        path=request.url.path,
    )

@event_task_router.delete('/event-tasks/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_event_task(
    request: Request,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    data = delete_event_task_service(db=db, task_id=task_id, user_id=current_user.id)
    return BaseResponseSchema(
        status_code=status.HTTP_204_NO_CONTENT,
        message='Xóa công việc thành công',
        data=data,
        path=request.url.path,
    )
        
