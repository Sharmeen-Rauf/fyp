"""
Reminder Model
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ReminderStatus(str, enum.Enum):
    """Reminder status"""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class Reminder(Base):
    """Reminder model"""
    __tablename__ = "reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reminder_type = Column(String, nullable=False)  # "interview_scheduled", "application_incomplete"
    scheduled_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReminderStatus), default=ReminderStatus.PENDING)
    sent_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interview = relationship("Interview")
    candidate = relationship("User")

