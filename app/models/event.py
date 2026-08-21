from app.db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship(
        'User',
        back_populates='events',
        uselist=False
    )
    
    staffs = relationship(
        'EventStaff', 
        back_populates='event', 
        cascade='all, delete-orphan'
    )
    
    tasks = relationship(
        'EventTask', 
        back_populates='event', 
        cascade='all, delete-orphan'
    )