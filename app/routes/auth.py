from fastapi import APIRouter, HTTPException
from app.services.firebase_db import db
from app.services.company_api import verify_login_and_get_info
from app.models.employee import SecurityLogin
from datetime import datetime

router = APIRouter()

@router.post("/login")
def login_employee(data: SecurityLogin):
    # ✅ تحقق من بيانات الموظف من الشركة
    employee_data = verify_login_and_get_info(data.employee_id, data.password)

    if not employee_data:
        raise HTTPException(status_code=401, detail="Incorrect ID or password")

    if employee_data.get("role") != 0:
        raise HTTPException(status_code=403, detail="Access denied: Not a security staff")

    # ✅ تأكد من أن الحساب غير موقوف
    existing_doc = db.collection("employees").document(data.employee_id).get()
    if existing_doc.exists and existing_doc.to_dict().get("active") == False:
        raise HTTPException(status_code=403, detail="Account is inactive")

    # ✅ حفظ بيانات الموظف (بدون الباسورد)
    db.collection("employees").document(data.employee_id).set(employee_data, merge=True)

    # ✅ حفظ سجل الدخول
    login_data = {
        **employee_data,
        "last_login": datetime.utcnow(),
        "is_logged_in": True  # ✅ أضفنا تسجيل الدخول
    }
    db.collection("security_staff_logins").document(data.employee_id).set(login_data)


    
    # ✅ إرسال البيانات بدون توكن
    return {
        "user": {
            "employee_id": employee_data["employee_id"],
            "name": employee_data["name"],
            "role": employee_data["role"],
            "phone": employee_data.get("phone", ""),
            "face_image": employee_data.get("face_image", "")
        }
    }
