from fastapi import APIRouter, Request, HTTPException
from app.config import db
from app.services.company_api import get_employee_by_id_from_company
from app.ai_models.face_recognition.face_model import process_new_employee_face  # ✅

router = APIRouter()

@router.post("/employee_update")
async def handle_employee_webhook(request: Request):
    payload = await request.json()

    employee_id = payload.get("employee_id")
    change_type = payload.get("change_type")  # "added", "updated", "removed"

    if not employee_id or not change_type:
        raise HTTPException(status_code=400, detail="Invalid webhook payload")

    # ✅ حالة الإضافة أو التحديث
    if change_type in ["added", "updated"]:
        emp_data = get_employee_by_id_from_company(employee_id)

        if not emp_data:
            return {"message": f"❌ Employee {employee_id} not found in company source"}

        # 🔁 تحديد الدور حسب المسمى الوظيفي
        role = 0 if "security" in emp_data.get("job_title", "").lower() else 1
        emp_data["role"] = role

        # ✅ توليد embedding إذا صورة الوجه موجودة (فقط عند الإضافة)
        face_url = emp_data.get("face_image")
        if change_type == "added" and face_url:
            success = process_new_employee_face(employee_id, face_url)
            if success:
                print(f"✅ Face embedding saved for {employee_id}")
            else:
                print(f"⚠️ Failed to generate face embedding for {employee_id}")

        # ✅ حفظ أو تحديث بيانات الموظف
        db.collection("employees").document(employee_id).set(emp_data, merge=True)

        return {"message": f"✅ Employee {employee_id} {change_type} successfully"}

    # 🗑️ حالة الحذف
    elif change_type == "removed":
        db.collection("employees").document(employee_id).set(
            {"active": False},
            merge=True
        )
        return {"message": f"🛑 Employee {employee_id} marked as inactive"}

    else:
        raise HTTPException(status_code=400, detail="Unknown change_type")
