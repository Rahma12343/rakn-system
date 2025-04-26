from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Notification(BaseModel):
    id: str                    # Unique notification ID
    employee_id: str          # For whom this notification is targeted (security staff ID)
    message: str              # Notification content
    is_read: bool = False     # Track whether the notification was viewed
    type: Optional[str] = "general"  # مثال: "violation", "warning", "general"
    timestamp: Optional[datetime]
