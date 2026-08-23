from sqlalchemy.orm import Session
from app.models.event import Event
from app.schemas.event import EventCreate


def create_event_service(db: Session, event_in: EventCreate, user_id: int):
    db_event = Event(name=event_in.name, description=event_in.description, owner_id=user_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event