"""
Interview Schemas
"""

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from app.models.interview import InterviewStatus


class InterviewBase(BaseModel):
    """Base interview schema"""
    role: str
    scheduled_at: Optional[datetime] = None


class InterviewCreate(InterviewBase):
    """Interview creation schema"""
    candidate_id: int
    hr_id: Optional[int] = None


class InterviewUpdate(BaseModel):
    """Interview update schema"""
    status: Optional[InterviewStatus] = None
    overall_score: Optional[float] = None


class InterviewResponse(BaseModel):
    """Interview response schema"""
    id: int
    candidate_id: int
    hr_id: Optional[int]
    role: str
    status: InterviewStatus
    scheduled_at: Optional[datetime]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    overall_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True


class InterviewResponseBase(BaseModel):
    """Base interview response schema"""
    question: str
    answer: str
    question_number: int


class InterviewResponseCreate(InterviewResponseBase):
    """Interview response creation schema"""
    interview_id: int


class InterviewResponseDetail(InterviewResponseBase):
    """Detailed interview response schema"""
    id: int
    interview_id: int
    sentiment_score: float
    confidence_score: float
    clarity_score: float
    relevance_score: float
    overall_score: float
    sentiment_analysis: Optional[dict] = None
    behavioral_cues: Optional[dict] = None
    ai_feedback: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class InterviewWithResponses(InterviewResponse):
    """Interview with responses"""
    responses: List[InterviewResponseDetail] = []

