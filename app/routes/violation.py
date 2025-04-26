from fastapi import APIRouter, Query, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import date
from app.models.violation import Violation
from app.services.firebase_db import get_all_violations, get_violation
from app.services.violation_service import log_violation_by_drone
from app.ai_models.violation_detector.violation_model import predict_violation
from app.services.cloudinary_uploader import upload_image_to_cloudinary
from app.ai_models.license_plate.license_plate_model import recognize_license_plate
from app import config

router = APIRouter()

# ✅ إرجاع كل المخالفات مع إمكانية الفلترة حسب التاريخ
@router.get("/violations", response_model=List[Violation])
def fetch_violations(from_date: date = Query(None), to_date: date = Query(None)):
    return get_all_violations(from_date, to_date)

# ✅ إرجاع تفاصيل مخالفة معينة
@router.get("/violations/{violation_id}", response_model=Violation)
def get_violation_by_id(violation_id: int):
    violation = get_violation(violation_id)
    if violation:
        return violation
    return {"error": "Violation not found"}


@router.post("/analyze")
async def analyze_violation_image(file: UploadFile = File(...)):
    # 🖼️ قراءة الصورة
    image_bytes = await file.read()

    # 🔍 تحليل نوع المخالفة
    result = predict_violation(image_bytes)
    violation_class = result["class"]

    if violation_class == "correct":
        return {"status": "ok", "result": result}

    # 🧠 استخراج رقم اللوحة من الصورة
    plate_number = recognize_license_plate(image_bytes)
    if plate_number in ["UNKNOWN", "ERROR"]:
        return {
            "status": "skipped",
            "reason": "❌ لم يتم التعرف على اللوحة",
            "result": result
        }

    # ✅ سجل المخالفة مباشرة بدون الحاجة لموظف أمني مسجل
    log_result = log_violation_by_drone(
        plate_number=plate_number,
        violation_class=violation_class,
        image_bytes=image_bytes
    )

    return {
        "status": "recorded",
        "plate_number": plate_number,
        "result": result,
        "log": log_result
    }
