"""
Application Schemas
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.application import ApplicationStatus


class ApplicationBase(BaseModel):
    """Base application schema"""
    job_role: str
    cover_letter: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """Application creation schema"""
    pass


class ApplicationUpdate(BaseModel):
    """Application update schema"""
    status: Optional[ApplicationStatus] = None
    cv_analysis: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    """Application response schema"""
    id: int
    candidate_id: int
    status: ApplicationStatus
    cv_file_path: Optional[str] = None
    cv_text: Optional[str] = None
    cv_analysis: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

