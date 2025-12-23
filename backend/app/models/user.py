"""
User Model
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    HR = "hr"
    CANDIDATE = "candidate"


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CANDIDATE, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

