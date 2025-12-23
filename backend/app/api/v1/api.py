"""
API v1 Router
"""

from fastapi import APIRouter

from app.api.v1.endpoints import interviews, questions, users, video, dashboard

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(questions.router, prefix="/questions", tags=["questions"])
api_router.include_router(video.router, prefix="/video", tags=["video"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])

