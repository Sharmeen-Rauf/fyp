"""
Video API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict

from app.models.user import User
from app.core.security import get_current_user
from app.services.video.twilio_service import TwilioVideoService

router = APIRouter()
video_service = TwilioVideoService()


@router.post("/rooms")
def create_room(
    room_name: str,
    max_participants: int = 2,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Create a video room"""
    result = video_service.create_room(room_name, max_participants)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/tokens")
def generate_token(
    room_name: str,
    identity: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Generate access token for video room"""
    token = video_service.generate_access_token(identity, room_name)
    if not token:
        raise HTTPException(status_code=500, detail="Failed to generate token")
    return {"token": token, "room_name": room_name}


@router.get("/rooms/{room_sid}")
def get_room(
    room_sid: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get room information"""
    result = video_service.get_room(room_sid)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

