from fastapi import APIRouter, HTTPException
from app.services.firebase_db import db
from app.models.employee import SecurityInfo
from app.config import current_security_id  # ✅ استدعاء ID الموظف من الكونفيق

router = APIRouter()

# ✅ عرض بيانات الموظف الحالي بناءً على المتغير العام
@router.get("/me", response_model=SecurityInfo)
def get_account_info():
    if not current_security_id:
        raise HTTPException(status_code=401, detail="🚫 لا يوجد موظف مسجل حالياً")

    doc = db.collection("security_staff_logins").document(current_security_id).get()
    if doc.exists:
        data = doc.to_dict()
        return {
            "Sec_ID": current_security_id,
            "F_Name": data.get("name", "").split(" ")[0],
            "L_Name": data.get("name", "").split(" ")[-1],
            "phone": data.get("phone", ""),
            "face_image": data.get("face_image", "")
        }

    raise HTTPException(status_code=404, detail="Employee not found")
