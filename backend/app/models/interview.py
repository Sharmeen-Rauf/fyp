"""
Interview Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class InterviewStatus(str, enum.Enum):
    """Interview status"""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Interview(Base):
    """Interview model"""
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hr_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    role = Column(String, nullable=False)  # Job role (e.g., "developer", "designer")
    status = Column(Enum(InterviewStatus), default=InterviewStatus.SCHEDULED)
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    overall_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    candidate = relationship("User", foreign_keys=[candidate_id])
    responses = relationship("InterviewResponse", back_populates="interview", cascade="all, delete-orphan")


class InterviewResponse(Base):
    """Interview response model"""
    __tablename__ = "interview_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    interview_id = Column(Integer, ForeignKey("interviews.id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    question_number = Column(Integer, nullable=False)
    
    # Scoring metrics
    sentiment_score = Column(Float, default=0.0)
    confidence_score = Column(Float, default=0.0)
    clarity_score = Column(Float, default=0.0)
    relevance_score = Column(Float, default=0.0)
    overall_score = Column(Float, default=0.0)
    
    # Analysis data
    sentiment_analysis = Column(JSON)  # Detailed sentiment analysis
    behavioral_cues = Column(JSON)  # Behavioral indicators
    ai_feedback = Column(Text)  # AI-generated feedback
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    interview = relationship("Interview", back_populates="responses")

