from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.event import Event
from app.models.event_staff import EventStaff
from app.models.user import User
from app.schemas.event_staff import EventStaffCreate

def add_member_service(db: Session, event_id: int, owner_id: int, new_event_staff: EventStaffCreate,):
	event = db.query(Event).filter(Event.id == event_id).first()
	if event is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Không tìm thấy sự kiện",
		)
	if event.owner_id != owner_id:
		raise HTTPException(
			status_code=status.HTTP_403_FORBIDDEN,
			detail="Bạn không phải là chủ sự kiện này",
		)
	user = db.query(User).filter(User.id == new_event_staff.user_id).first()
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Không tìm thấy người dùng",
		)
	member = db.query(EventStaff).filter(
		EventStaff.event_id == event_id,
		EventStaff.user_id == new_event_staff.user_id,
	).first()
	if member is not None:
		raise HTTPException(
			status_code=status.HTTP_409_CONFLICT,
			detail="Người dùng đã là thành viên của sự kiện",
		)
	member = EventStaff(
		event_id=event_id,
		user_id=new_event_staff.user_id,
		role=new_event_staff.role,
	)
	db.add(member)
	db.commit()
	db.refresh(member)
	return member

def get_list_members_event_service(db: Session, event_id: int, user_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sự kiện",
        )
    is_owner = event.owner_id == user_id
    is_member = db.query(EventStaff).filter(
        EventStaff.event_id == event_id,
        EventStaff.user_id == user_id,
    ).first() is not None
    if not (is_owner or is_member):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của sự kiện này",
        )
    members = db.query(EventStaff).filter(EventStaff.event_id == event_id).all()
    return members