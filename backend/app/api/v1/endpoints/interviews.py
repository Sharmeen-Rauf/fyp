"""
Interview API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.interview import (
    InterviewCreate, InterviewResponse, InterviewUpdate,
    InterviewResponseCreate, InterviewResponseDetail, InterviewWithResponses
)
from app.models.interview import Interview, InterviewResponse as InterviewResponseModel, InterviewStatus
from app.models.user import User
from app.core.security import get_current_user
from app.services.scoring.scoring_engine import ScoringEngine
from app.services.ai.interview_agent import InterviewAgent

router = APIRouter()
scoring_engine = ScoringEngine()
interview_agent = InterviewAgent()


@router.post("/", response_model=InterviewResponse, status_code=status.HTTP_201_CREATED)
def create_interview(
    interview: InterviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new interview"""
    db_interview = Interview(**interview.dict())
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview


@router.get("/", response_model=List[InterviewResponse])
def get_interviews(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all interviews"""
    interviews = db.query(Interview).offset(skip).limit(limit).all()
    return interviews


@router.get("/{interview_id}", response_model=InterviewWithResponses)
def get_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get interview by ID with responses"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview


@router.post("/{interview_id}/start")
def start_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start an interview"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    interview.status = InterviewStatus.IN_PROGRESS
    from datetime import datetime
    interview.started_at = datetime.utcnow()
    db.commit()
    
    # Generate questions if not already generated
    questions = interview_agent.generate_questions(role=interview.role, num_questions=5)
    return {"status": "started", "questions": questions}


@router.post("/{interview_id}/responses", response_model=InterviewResponseDetail)
def submit_response(
    interview_id: int,
    response: InterviewResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit an interview response"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Score the response
    scores = scoring_engine.score_response(
        question=response.question,
        answer=response.answer
    )
    
    # Create response record
    db_response = InterviewResponseModel(
        interview_id=interview_id,
        question=response.question,
        answer=response.answer,
        question_number=response.question_number,
        sentiment_score=scores["sentiment_score"],
        confidence_score=scores["confidence_score"],
        clarity_score=scores["clarity_score"],
        relevance_score=scores["relevance_score"],
        overall_score=scores["overall_score"],
        sentiment_analysis=scores["sentiment_analysis"],
        behavioral_cues=scores["behavioral_cues"],
        ai_feedback=scores["ai_feedback"]
    )
    
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    return db_response


@router.post("/{interview_id}/complete")
def complete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Complete an interview and calculate final score"""
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    
    # Get all responses
    responses = db.query(InterviewResponseModel).filter(
        InterviewResponseModel.interview_id == interview_id
    ).all()
    
    if not responses:
        raise HTTPException(status_code=400, detail="No responses found")
    
    # Calculate overall score
    response_scores = [r.overall_score for r in responses]
    overall_score = scoring_engine.calculate_interview_score(response_scores)
    
    interview.overall_score = overall_score
    interview.status = InterviewStatus.COMPLETED
    from datetime import datetime
    interview.completed_at = datetime.utcnow()
    db.commit()
    
    return {"status": "completed", "overall_score": overall_score}

