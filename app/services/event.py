from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import and_
from app.models.event import Event
from app.models.event_staff import EventStaff
from app.schemas.event import EventCreate, EventUpdate

def create_event_service(db: Session, event_in: EventCreate, user_id: int):
    db_event = Event(name=event_in.name, description=event_in.description, owner_id=user_id)
    db.add(db_event)
    db.flush()

    db_staff = EventStaff(
        event_id=db_event.id,
        user_id=user_id,
        role="OWNER",
    )
    db.add(db_staff)
    db.commit()
    db.refresh(db_event)
    return db_event

def get_events_service(db: Session, user_id: int, search: Optional[str] = None):
    query = db.query(Event).join(EventStaff).filter(EventStaff.user_id == user_id)
    if search:
        query = query.filter(Event.name.ilike(f"%{search}%"))
    return query.all()

def get_event_detail_service(db: Session, event_id: int, user_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sự kiện",
        )
    is_owner = db.query(EventStaff).filter(
        and_(
            EventStaff.event_id == event_id,
            EventStaff.user_id == user_id,
            EventStaff.role == "OWNER",
        )
    ).first() is not None
    is_member = db.query(EventStaff).filter(
        and_(EventStaff.event_id == event_id, EventStaff.user_id == user_id)
    ).first() is not None
    if not (is_owner or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của sự kiện này",
        )
    return event

def update_event_service(db: Session, event_id: int, user_id: int, event_update: EventUpdate):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sự kiện",
        )
    chk_owner_event = db.query(EventStaff).filter(
        and_(EventStaff.event_id == event_id, EventStaff.user_id == user_id, EventStaff.role == "OWNER")
    ).first()
    if not chk_owner_event:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là chủ sự kiện này",
        )
    update_data = event_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event_service(db: Session, event_id: int, user_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sự kiện",
        )
    chk_owner_event = db.query(EventStaff).filter(
        and_(EventStaff.event_id == event_id, EventStaff.user_id == user_id, EventStaff.role == "OWNER")
    ).first()
    if not chk_owner_event:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải là chủ sự kiện này",
        )
    db.delete(event)
    db.commit()
    return event