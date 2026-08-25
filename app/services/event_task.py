from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from sqlalchemy import and_, or_
from app.schemas.event_task import EventTaskCreate, EventTaskUpdate, TaskSortField, SortOrder
from app.models.event import Event
from app.models.event_staff import EventStaff
from app.models.event_task import EventTask

def create_task_service(db: Session, new_task: EventTaskCreate, event_id: int, user_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Không tìm thấy sự kiện'
        )
    is_member = (
        db.query(EventStaff).filter(EventStaff.event_id == event_id, EventStaff.user_id == user_id).first())
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là thành viên của sự kiện này",
        )
    if new_task.assignee_id is not None:
        is_member = db.query(EventStaff).filter(
            EventStaff.event_id == event_id,
            EventStaff.user_id == new_task.assignee_id
        ).first()
        if not is_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Người được giao không phải là thành viên của sự kiện'
            )
    event_task = EventTask(
        title=new_task.title,
        description=new_task.description,
        assignee_id=new_task.assignee_id,
        event_id=event_id,
        status=new_task.status,
        priority=new_task.priority,
        due_date=new_task.due_date
    )
    db.add(event_task)
    db.commit()
    db.refresh(event_task)
    return event_task

def filter_event_tasks_service(
    db: Session,
    event_id: int,
    user_id: int,
    status_filter: Optional[str] = None,
    priority_filter: Optional[str] = None,
    assignee_id: Optional[int] = None,
    search: Optional[str] = None,
    sort_by: TaskSortField = TaskSortField.CREATED_AT,
    order: SortOrder = SortOrder.DESC,
    limit: int = 10,
    offset: int = 0,
):
    is_member = (
        db.query(EventStaff).filter(EventStaff.event_id == event_id, EventStaff.user_id == user_id).first())
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem công việc của sự kiện này",
        )
    query = db.query(EventTask).filter(EventTask.event_id == event_id)
    if status_filter:
        query = query.filter(EventTask.status == status_filter)
    if priority_filter:
        query = query.filter(EventTask.priority == priority_filter)
    if assignee_id is not None:
        query = query.filter(EventTask.assignee_id == assignee_id)
    if search:
        query = query.filter(EventTask.title.ilike(f"%{search}%"))
    sort_column = EventTask.due_date if sort_by == TaskSortField.DUE_DATE else EventTask.created_at
    if order == SortOrder.ASC:
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())
    tasks = query.offset(offset).limit(limit).all()
    return tasks

def get_event_task_by_id_service(db: Session, task_id: int, user_id: int):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công việc"
        )
    is_member = (
        db.query(EventStaff).filter(EventStaff.event_id == task.event_id, EventStaff.user_id == user_id).first())
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền xem công việc của sự kiện này",
        )
    return task

def update_event_task_service(db: Session, task_id: int, user_id: int, task_update: EventTaskUpdate):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công việc"
        )
    is_owner = db.query(EventStaff).filter(
        EventStaff.event_id == task.event_id,
        EventStaff.user_id == user_id,
        EventStaff.role == "OWNER",
    ).first()
    is_assignee = db.query(EventTask).filter(EventTask.id == task_id, EventTask.assignee_id == user_id).first()
    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa công việc của sự kiện này",
        )
    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.assignee_id is not None:
        is_assignee_member = db.query(EventStaff).filter(
            EventStaff.event_id == task.event_id,
            EventStaff.user_id == task_update.assignee_id
        ).first()
        if not is_assignee_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Người được giao không phải là thành viên của sự kiện'
            )
        task.assignee_id = task_update.assignee_id
    if task_update.status is not None:
        task.status = task_update.status
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.due_date is not None:
        task.due_date = task_update.due_date
    db.commit()
    db.refresh(task)
    return task

def delete_event_task_service(db: Session, task_id: int, user_id: int):
    task = db.query(EventTask).filter(EventTask.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy công việc"
        )
    is_owner = db.query(EventStaff).filter(
        EventStaff.event_id == task.event_id,
        EventStaff.user_id == user_id,
        EventStaff.role == "OWNER",
    ).first()
    is_assignee = db.query(EventTask).filter(EventTask.id == task_id, EventTask.assignee_id == user_id).first()
    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền chỉnh sửa công việc của sự kiện này",
        )
    db.delete(task)
    db.commit()
    return task