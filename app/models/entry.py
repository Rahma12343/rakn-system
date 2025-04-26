from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EntryLog(BaseModel):
    employee_id: str
    name: str
    license_plate: str
    entry_time: datetime
    plate_image: Optional[str] = None  # صورة اللوحة
    face_image: Optional[str] = None   # صورة الوجه
