from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from io import BytesIO
from app.ai_models.face_recognition.face_model import compare_face
from app.services.temp_plate_store import get_latest_plate, clear_temp_plate
from app.services.company_api import get_employee_by_id_from_company
from app.models.entry import EntryLog
from app.config import db
from app.utils import normalize_plate
from app.services.cloudinary_uploader import upload_image_to_cloudinary

router = APIRouter()

def open_gate(employee_id: str):
    print(f"🚪 تم فتح البوابة تلقائيًا للموظف {employee_id}")

@router.post("/verify")
async def verify_face(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # 🧠 مطابقة الوجه
        match = compare_face(BytesIO(image_bytes))
        if not match:
            raise HTTPException(status_code=401, detail="Unauthorized: No match found.")

        # ⏫ رفع صورة الوجه إلى Cloudinary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        face_url = upload_image_to_cloudinary(image_bytes, folder="faces")

        # 🚘 جلب اللوحة
        plate_data = get_latest_plate()
        if not plate_data:
            raise HTTPException(status_code=400, detail="❌ لم يتم العثور على لوحة مخزنة")

        raw_plate = plate_data["plate_number"]
        license_plate = normalize_plate(raw_plate)
        plate_url = plate_data["plate_image_url"]  # <-- تأكد أن الحقل موجود

        # 👤 بيانات الموظف
        employee = get_employee_by_id_from_company(match["employee_id"])
        if not employee:
            raise HTTPException(status_code=404, detail="الموظف غير موجود")

        # 📝 إنشاء سجل الدخول
        entry = EntryLog(
            employee_id=employee["employee_id"],
            name=employee["name"],
            license_plate=license_plate,
            entry_time=datetime.now(),
            plate_image=plate_url,
            face_image=face_url
        )
        db.collection("entry_logs").add(entry.dict())

        # 🚪 فتح البوابة
        open_gate(employee["employee_id"])

        # 🧹 مسح المؤقت
        clear_temp_plate()

        return {
            "status": "match",
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "license_plate": license_plate,
            "plate_image": plate_url,
            "face_image": face_url,
            "similarity": match["similarity"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Internal error: {str(e)}")
