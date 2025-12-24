"""
Application and CV API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil
from pathlib import Path

from app.core.database import get_db
from app.schemas.application import ApplicationCreate, ApplicationResponse, ApplicationUpdate
from app.models.application import Application, ApplicationStatus
from app.models.user import User, UserRole
from app.core.security import get_current_user
from app.services.ai.cv_analyzer import CVAnalyzer

router = APIRouter()

# Create uploads directory
UPLOAD_DIR = Path("uploads/cvs")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

cv_analyzer = CVAnalyzer()


@router.post("/", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new job application"""
    if current_user.role != UserRole.CANDIDATE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only candidates can create applications"
        )
    
    db_application = Application(
        candidate_id=current_user.id,
        job_role=application.job_role,
        cover_letter=application.cover_letter,
        status=ApplicationStatus.PENDING
    )
    
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    return db_application


@router.post("/{application_id}/upload-cv", response_model=ApplicationResponse)
async def upload_cv(
    application_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload CV/resume for an application"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application.candidate_id != current_user.id and current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate file type
    allowed_extensions = {'.pdf', '.doc', '.docx', '.txt'}
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save file
    file_path = UPLOAD_DIR / f"{application_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Extract text from CV
    cv_text = cv_analyzer.extract_text(str(file_path), file_ext)
    
    # Analyze CV using AI
    cv_analysis = cv_analyzer.analyze_cv(cv_text, application.job_role)
    
    # Update application
    application.cv_file_path = str(file_path)
    application.cv_text = cv_text
    application.cv_analysis = cv_analysis
    application.status = ApplicationStatus.REVIEWING
    
    db.commit()
    db.refresh(application)
    
    return application


@router.get("/", response_model=List[ApplicationResponse])
def get_applications(
    status: Optional[ApplicationStatus] = None,
    job_role: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get applications"""
    query = db.query(Application)
    
    # Candidates can only see their own applications
    if current_user.role == UserRole.CANDIDATE:
        query = query.filter(Application.candidate_id == current_user.id)
    
    if status:
        query = query.filter(Application.status == status)
    if job_role:
        query = query.filter(Application.job_role == job_role)
    
    applications = query.offset(skip).limit(limit).all()
    return applications


@router.get("/{application_id}", response_model=ApplicationResponse)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get application by ID"""
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check authorization
    if application.candidate_id != current_user.id and current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return application


@router.patch("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application_update: ApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update application (HR/Admin only)"""
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    if application_update.status:
        application.status = application_update.status
    if application_update.cv_analysis:
        application.cv_analysis = application_update.cv_analysis
    
    db.commit()
    db.refresh(application)
    
    return application


@router.post("/{application_id}/accept")
def accept_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Accept an application (HR/Admin only)"""
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = ApplicationStatus.ACCEPTED
    db.commit()
    
    return {"message": "Application accepted", "application_id": application_id}


@router.post("/{application_id}/reject")
def reject_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject an application (HR/Admin only)"""
    if current_user.role not in [UserRole.HR, UserRole.ADMIN]:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = ApplicationStatus.REJECTED
    db.commit()
    
    return {"message": "Application rejected", "application_id": application_id}

