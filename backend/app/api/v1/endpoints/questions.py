"""
Question Bank API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.question import QuestionBank
from app.models.user import User
from app.core.security import get_current_user
from app.services.ai.interview_agent import InterviewAgent

router = APIRouter()
interview_agent = InterviewAgent()


@router.get("/")
def get_questions(
    role: Optional[str] = None,
    category: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get questions from question bank"""
    query = db.query(QuestionBank).filter(QuestionBank.is_active == True)
    
    if role:
        query = query.filter(QuestionBank.role == role)
    if category:
        query = query.filter(QuestionBank.category == category)
    
    questions = query.offset(skip).limit(limit).all()
    return questions


@router.post("/generate")
def generate_questions(
    role: str,
    category: str = "mixed",
    num_questions: int = 5,
    difficulty: str = "medium",
    current_user: User = Depends(get_current_user)
):
    """Generate AI questions for a role"""
    questions = interview_agent.generate_questions(
        role=role,
        category=category,
        num_questions=num_questions,
        difficulty=difficulty
    )
    return {"questions": questions}

