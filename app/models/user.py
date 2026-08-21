from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), default='USER')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    events = relationship(
        'Event',
        back_populates='user'
    )
    
    staff_events = relationship(
        'EventStaff', 
        back_populates='user', 
        cascade='all, delete-orphan'
    )
    
    assigned_tasks = relationship(
        'EventTask', 
        back_populates='assignee'
    )