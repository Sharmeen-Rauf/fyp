"""
Reminder Service
Handles automated reminders for interviews and incomplete applications
"""

from datetime import datetime, timedelta
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.reminder import Reminder, ReminderStatus
from app.models.interview import Interview
from app.models.user import User


class ReminderService:
    """Service for managing interview reminders"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_interview_reminder(
        self,
        interview_id: int,
        candidate_id: int,
        scheduled_time: datetime
    ) -> Reminder:
        """Create a reminder for an upcoming interview"""
        # Create reminder 24 hours before interview
        reminder_time = scheduled_time - timedelta(hours=24)
        
        reminder = Reminder(
            interview_id=interview_id,
            candidate_id=candidate_id,
            reminder_type="interview_scheduled",
            scheduled_time=reminder_time,
            status=ReminderStatus.PENDING
        )
        
        self.db.add(reminder)
        self.db.commit()
        self.db.refresh(reminder)
        return reminder
    
    def get_pending_reminders(self) -> List[Reminder]:
        """Get all pending reminders that are due"""
        now = datetime.utcnow()
        reminders = self.db.query(Reminder).filter(
            and_(
                Reminder.status == ReminderStatus.PENDING,
                Reminder.scheduled_time <= now
            )
        ).all()
        return reminders
    
    def send_reminder(self, reminder: Reminder) -> bool:
        """Send a reminder (email/SMS)"""
        try:
            # Get candidate information
            candidate = self.db.query(User).filter(User.id == reminder.candidate_id).first()
            interview = self.db.query(Interview).filter(Interview.id == reminder.interview_id).first()
            
            if not candidate or not interview:
                return False
            
            # TODO: Implement actual email/SMS sending
            # For now, just mark as sent
            reminder.status = ReminderStatus.SENT
            reminder.sent_at = datetime.utcnow()
            self.db.commit()
            
            return True
        except Exception as e:
            print(f"Error sending reminder: {e}")
            reminder.status = ReminderStatus.FAILED
            self.db.commit()
            return False
    
    def process_pending_reminders(self) -> int:
        """Process all pending reminders"""
        reminders = self.get_pending_reminders()
        sent_count = 0
        
        for reminder in reminders:
            if self.send_reminder(reminder):
                sent_count += 1
        
        return sent_count

