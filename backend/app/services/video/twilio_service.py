"""
Twilio Video Service
Handles video interview room creation and management
"""

from typing import Dict, Optional
from twilio.rest import Client
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant
from app.core.config import settings


class TwilioVideoService:
    """Service for managing Twilio video rooms"""
    
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.api_key = settings.TWILIO_API_KEY
        self.api_secret = settings.TWILIO_API_SECRET
        self.client = Client(self.account_sid, self.auth_token) if self.account_sid else None
    
    def create_room(self, room_name: str, max_participants: int = 2) -> Dict:
        """
        Create a video room
        
        Args:
            room_name: Unique room name
            max_participants: Maximum participants
        
        Returns:
            Room information
        """
        if not self.client:
            return {"error": "Twilio not configured"}
        
        try:
            room = self.client.video.rooms.create(
                unique_name=room_name,
                max_participants=max_participants,
                type='go'  # Group room
            )
            
            return {
                "room_sid": room.sid,
                "room_name": room.unique_name,
                "status": room.status,
                "max_participants": room.max_participants
            }
        except Exception as e:
            return {"error": str(e)}
    
    def generate_access_token(
        self,
        identity: str,
        room_name: str,
        ttl: int = 3600
    ) -> Optional[str]:
        """
        Generate access token for video room
        
        Args:
            identity: User identity (user ID or email)
            room_name: Room name
            ttl: Time to live in seconds
        
        Returns:
            JWT access token
        """
        if not self.api_key or not self.api_secret:
            return None
        
        try:
            token = AccessToken(
                self.account_sid,
                self.api_key,
                self.api_secret,
                identity=identity
            )
            
            video_grant = VideoGrant(room=room_name)
            token.add_grant(video_grant)
            
            return token.to_jwt()
        except Exception as e:
            print(f"Error generating token: {e}")
            return None
    
    def get_room(self, room_sid: str) -> Dict:
        """Get room information"""
        if not self.client:
            return {"error": "Twilio not configured"}
        
        try:
            room = self.client.video.rooms(room_sid).fetch()
            return {
                "room_sid": room.sid,
                "room_name": room.unique_name,
                "status": room.status,
                "max_participants": room.max_participants
            }
        except Exception as e:
            return {"error": str(e)}
    
    def end_room(self, room_sid: str) -> bool:
        """End a video room"""
        if not self.client:
            return False
        
        try:
            room = self.client.video.rooms(room_sid).update(status='completed')
            return room.status == 'completed'
        except Exception as e:
            print(f"Error ending room: {e}")
            return False

