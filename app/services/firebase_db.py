from firebase_admin import firestore
from datetime import date
from typing import Optional, List
from app.models.violation import Violation
from app.config import db

def get_all_violations(from_date: Optional[date] = None, to_date: Optional[date] = None) -> List[Violation]:
    violations_ref = db.collection("violations")
    query = violations_ref

    if from_date:
        query = query.where("date", ">=", from_date.isoformat())
    if to_date:
        query = query.where("date", "<=", to_date.isoformat())

    docs = query.stream()
    violations = []

    for doc in docs:
        data = doc.to_dict()
        violations.append(Violation(**data))

    return violations

def get_violation(violation_id: int) -> Optional[Violation]:
    query = db.collection("violations").where("violation_id", "==", violation_id).limit(1)
    docs = query.stream()

    for doc in docs:
        data = doc.to_dict()
        return Violation(**data)

    return None



def get_violations_by_phone(phone_number: str) -> List[dict]:
    try:
        # 🧼 تنظيف الرقم من أي فراغات أو فواصل
        normalized_phone = phone_number.replace(" ", "").replace("-", "").strip()
        print(f"🔍 نبحث عن مخالفات لرقم: {normalized_phone}")

        # ✅ سحب المخالفات بدون ترتيب عشان ما يحتاج Index
        docs = db.collection("violations") \
            .where("phone", "==", normalized_phone) \
            .stream()

        violations = []
        for doc in docs:
            data = doc.to_dict()
            print("✅ لقينا مخالفة لرقم:", data.get("phone"))

            violations.append({
                "violation_id": data.get("violation_id"),
                "license_plate": data.get("license_plate"),
                "employee_name": data.get("employee_name"),
                "type": data.get("violation_type"),
                "date": data.get("date"),
                "image_url": data.get("image_url")
            })

        return violations

    except Exception as e:
        print(f"❌ خطأ في get_violations_by_phone: {e}")
        return []