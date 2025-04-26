from datetime import datetime
from app.config import db, current_security_id
from app.models.violation import Violation
from app.models.notification import Notification
from app.utils import normalize_plate
from app.services.whatsapp_bot import send_violation_whatsapp
from firebase_admin import firestore

def find_employee_by_plate(plate_number: str):
    normalized_plate = normalize_plate(plate_number)

    docs = db.collection("entry_logs") \
             .where("license_plate", "==", normalized_plate) \
             .order_by("entry_time", direction=firestore.Query.DESCENDING) \
             .limit(1) \
             .stream()

    for doc in docs:
        entry = doc.to_dict()
        return {
            "employee_id": entry["employee_id"],
            "name": entry["name"]
        }

    return None

def log_violation_by_drone(plate_number: str, violation_class: str, image_bytes: bytes) -> dict:
    try:
        from app.services.cloudinary_uploader import upload_image_to_cloudinary
        from app.services.whatsapp_bot import send_violation_whatsapp

        # ✅ استخدم ID موظف الأمن إذا موجود، أو خليه فاضي
        security_id = current_security_id if current_security_id else ""

        license_plate = normalize_plate(plate_number)
        now = datetime.now()

        matched_employee = find_employee_by_plate(license_plate)
        if not matched_employee:
            return {"error": "❌ لا يوجد دخول سابق مرتبط بهذه اللوحة"}

        employee_doc = db.collection("employees").document(matched_employee["employee_id"]).get()
        if not employee_doc.exists:
            return {"error": "🚫 الموظف غير موجود"}

        employee_data = employee_doc.to_dict()

        # ✅ تحديد نوع المخالفة بناءً على وجود تحذير سابق أو لا
        existing_warning = db.collection("violations") \
            .where("license_plate", "==", license_plate) \
            .where("violation_type", "==", "Warning") \
            .limit(1) \
            .stream()

        has_warning = any(existing_warning)

        violation_type = "Violation" if has_warning else "Warning"

        # ✅ إنشاء بيانات المخالفة
        violation_id = int(now.timestamp())
        image_url = upload_image_to_cloudinary(image_bytes)

        print(f"✅ رقم الجوال اللي بنخزنه في violation: {employee_data['phone']}")

        violation = Violation(
            violation_id=violation_id,
            violation_type=violation_type,
            employee_id=matched_employee["employee_id"],
            employee_name=matched_employee["name"],
            license_plate=license_plate,
            date=now.date().isoformat(),
            time=now.time().strftime("%H:%M:%S"),
            image_url=image_url,
            phone=employee_data["phone"]
        )

        db.collection("violations").add(violation.dict())

        # ✅ أرسل إشعار واتساب للموظف
        send_violation_whatsapp(
            to_number=employee_data["phone"].replace(" ", ""),
            plate_number=license_plate,
            date=now.date().isoformat(),
            violation_type=violation_type,
            image_url=image_url,
            violation_id=str(violation_id),
            employee_name=employee_data["name"],
        )

        # ✅ أرسل إشعار داخل النظام لكل موظف أمن شغال حالياً
        security_staff_ref = db.collection("security_staff_logins")
        security_staff_docs = security_staff_ref.stream()

        for staff_doc in security_staff_docs:
            staff = staff_doc.to_dict()
            if staff.get("role") == 0 and staff.get("is_logged_in", False):
                notification = Notification(
                    id=str(int(now.timestamp() * 1000)),
                    message=f"{'⚠️' if violation_type == 'Warning' else '🚨'} تم تسجيل {violation_type} على الموظف {employee_data['name']} (لوحة: {license_plate})",
                    employee_id=staff["employee_id"],
                    is_read=False,
                    timestamp=now.isoformat()
                )
                db.collection("notifications").add(notification.dict())

        return {
            "violation": violation.dict()
        }

    except Exception as e:
        return {"error": str(e)}
