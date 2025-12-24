"""
Application and CV Models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    """Application status"""
    PENDING = "pending"
    REVIEWING = "reviewing"
    SHORTLISTED = "shortlisted"
    REJECTED = "rejected"
    ACCEPTED = "accepted"


class Application(Base):
    """Job application model"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_role = Column(String, nullable=False)  # Job role applied for
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    cv_file_path = Column(String, nullable=True)  # Path to uploaded CV
    cv_text = Column(Text, nullable=True)  # Extracted text from CV
    cv_analysis = Column(Text, nullable=True)  # AI analysis of CV
    cover_letter = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidate = relationship("User", foreign_keys=[candidate_id])
    interview = relationship("Interview", back_populates="application", uselist=False)


# Add relationship to Interview model
# This will be added to interview.py

