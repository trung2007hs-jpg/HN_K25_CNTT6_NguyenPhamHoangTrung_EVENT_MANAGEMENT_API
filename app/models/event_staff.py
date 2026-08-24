from app.db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class EventStaff(Base):
    __tablename__ = "event_staff"
    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    role = Column(String(50), default="MEMBER")
    joined_at = Column(DateTime, server_default=func.now())
    
    event = relationship('Event', 
        back_populates='staffs',
        uselist=False
    )
    
    user = relationship(
        'User', 
        back_populates='staff_events',
        uselist=False
    )
    
    