from app.config import db
from app.services.company_api import mock_company_data
from app.ai_models.face_recognition.Empiding_generate import generate_and_save_all_embeddings  # ✅
# ما نحتاج face_model ولا firebase_db هنا بعد التعديل


def seed_mock_company():
    company_id = "MOCK001"
    company_ref = db.collection("companies").document(company_id)
    company_doc = company_ref.get()

    if company_doc.exists:
        print(f"⚠️ الشركة '{company_id}' موجودة بالفعل.")
        return

    company_data = {
        "company_name": "RAKN Test Company",
        "location": "Riyadh, KSA",
        "contact_person": {
            "name": "Test Manager",
            "phone": "+966500000000"
        },
        "created_at": "2025-04-13T00:00:00Z"
    }

    company_ref.set(company_data)
    print("✅ تم إنشاء الشركة MOCK001 بنجاح.")


def seed_mock_employees():
    for emp in mock_company_data:
        full_name = f"{emp['F_Name']} {emp['L_Name']}"
        job_title = emp["job_title"]
        role = 0 if "security" in job_title.lower() else 1

        emp_data = {
            "employee_id": emp["employee_id"],
            "name": full_name,
            "phone": emp["Phone_No"],
            "face_image": emp["Face_Image"],
            "job_title": job_title,
            "company_id": emp["company_id"],
            "role": role
        }

        db.collection("employees").document(emp["employee_id"]).set(emp_data)

    print("✅ تم إضافة جميع الموظفين بنجاح.")

    # ✅ توليد embeddings بعد الإدخال
    generate_and_save_all_embeddings()
    print("✅ تم توليد وحفظ جميع الـ embeddings بنجاح.")


def seed_all_mock_data():
    seed_mock_company()
    seed_mock_employees()
