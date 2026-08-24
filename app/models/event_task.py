from app.db.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class EventTask(Base):
    __tablename__ = 'event_tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    status = Column(String(50), default='TODO') # TODO / IN_PROGRESS / DONE
    priority = Column(String(50), default='MEDIUM')
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    event = relationship(
        'Event', 
        back_populates='tasks',
        uselist=False
    )

    assignee = relationship(
        'User', 
        back_populates='assigned_tasks',
        uselist=False
    )