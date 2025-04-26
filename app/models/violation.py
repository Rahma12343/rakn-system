from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional

class Violation(BaseModel):
    violation_id: int
    violation_type: str
    employee_id: str
    employee_name: str
    license_plate: str
    date: str
    time: str
    image_url: str
    phone: str  # ✅ أضف هذا السطر
