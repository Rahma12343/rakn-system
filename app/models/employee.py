from pydantic import BaseModel

class SecurityLogin(BaseModel):
    employee_id: str
    password: str

class SecurityInfo(BaseModel):
    Sec_ID: str
    F_Name: str
    L_Name: str
    phone: str
    face_image: str  # ✅ جديد

