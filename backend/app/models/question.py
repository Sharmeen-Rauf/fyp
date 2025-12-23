"""
Question Bank Models
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.core.database import Base


class QuestionBank(Base):
    """Question bank model"""
    __tablename__ = "question_banks"
    
    id = Column(Integer, primary_key=True, index=True)
    role = Column(String, nullable=False, index=True)  # e.g., "developer", "designer", "manager"
    category = Column(String, nullable=False)  # e.g., "technical", "behavioral", "situational"
    question = Column(Text, nullable=False)
    expected_keywords = Column(JSON)  # Keywords that should be in good answers
    difficulty_level = Column(String, default="medium")  # easy, medium, hard
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

