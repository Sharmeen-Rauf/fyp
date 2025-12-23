"""
HR Dashboard API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, desc

from app.core.database import get_db
from app.models.interview import Interview, InterviewStatus
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.schemas.interview import InterviewWithResponses

router = APIRouter()


@router.get("/candidates")
def get_candidates(
    role: Optional[str] = None,
    min_score: Optional[float] = None,
    status: Optional[InterviewStatus] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get candidates with filtering options"""
    # Only HR and Admin can access
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    query = db.query(Interview)
    
    if role:
        query = query.filter(Interview.role == role)
    if min_score is not None:
        query = query.filter(Interview.overall_score >= min_score)
    if status:
        query = query.filter(Interview.status == status)
    
    interviews = query.order_by(desc(Interview.overall_score)).offset(skip).limit(limit).all()
    
    return [
        {
            "interview_id": i.id,
            "candidate_id": i.candidate_id,
            "candidate_name": i.candidate.full_name if i.candidate else "Unknown",
            "role": i.role,
            "status": i.status,
            "overall_score": i.overall_score,
            "completed_at": i.completed_at
        }
        for i in interviews
    ]


@router.get("/statistics")
def get_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics"""
    # Only HR and Admin can access
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    total_interviews = db.query(func.count(Interview.id)).scalar()
    completed_interviews = db.query(func.count(Interview.id)).filter(
        Interview.status == InterviewStatus.COMPLETED
    ).scalar()
    
    avg_score = db.query(func.avg(Interview.overall_score)).filter(
        Interview.status == InterviewStatus.COMPLETED
    ).scalar() or 0.0
    
    # Interviews by role
    role_stats = db.query(
        Interview.role,
        func.count(Interview.id).label("count"),
        func.avg(Interview.overall_score).label("avg_score")
    ).filter(
        Interview.status == InterviewStatus.COMPLETED
    ).group_by(Interview.role).all()
    
    return {
        "total_interviews": total_interviews,
        "completed_interviews": completed_interviews,
        "average_score": round(avg_score, 2),
        "by_role": [
            {"role": role, "count": count, "avg_score": round(avg_score or 0.0, 2)}
            for role, count, avg_score in role_stats
        ]
    }


@router.get("/candidates/{interview_id}")
def get_candidate_detail(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed candidate information"""
    # Only HR and Admin can access
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    return interview

