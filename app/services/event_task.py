from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.event_task import EventTaskCreate
from app.models.event_staff import EventStaff
from app.models.event_task import EventTask

def create_task_service(db: Session, new_task: EventTaskCreate, event_id: int):
    event_staff = db.query(EventStaff).filter(EventStaff.event_id == event_id).first()
    if not event_staff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Không tìm thấy sự kiện'
        )
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
        due_date=new_task.due_date
    )
    db.add(event_task)
    db.commit()
    db.refresh(event_task)
    return event_task