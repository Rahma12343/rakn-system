import requests

# ⚙️ إعدادات API (تقدر تغيرها لاحقاً)
USE_REAL_API = False  # ⬅️ غيّرها إلى True لما تستخدم API فعلي
REAL_API_URL = "https://api.company.com/employees"

# --------- بيانات وهمية تمثل API خارجي (mock) ---------
mock_company_data = [
    {
        "employee_id": "EMP001",
        "password": "pass001",
        "F_Name": "Abdullah",
        "L_Name": "Al-Zahrani",
        "Phone_No": "+966555822583",
        "Face_Image": "https://i.postimg.cc/SNWZ8Qwr/Abdullah-Al-Zahrani.jpg",
        "job_title": "Security Officer",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP002",
        "password": "pass002",
        "F_Name": "Amani",
        "L_Name": "Saleh",
        "Phone_No": "+966557712903",
        "Face_Image": "https://i.postimg.cc/ZKRRv0Bk/Amani-Saleh.jpg",
        "job_title": "Software Engineer",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP003",
        "password": "pass003",
        "F_Name": "Khaled",
        "L_Name": "Nasser",
        "Phone_No": "+966555822583",
        "Face_Image": "https://i.postimg.cc/GmDbvDbf/Khaled-Nasser.jpg",
        "job_title": "Security Staff",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP004",
        "password": "pass004",
        "F_Name": "Reem",
        "L_Name": "AlHarbi",
        "Phone_No": "+966500000004",
        "Face_Image": "https://i.postimg.cc/LXbWyyT3/Reem-Al-Harbi.jpg",
        "job_title": "HR Specialist",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP005",
        "password": "pass005",
        "F_Name": "Nouf",
        "L_Name": "Alqahtani",
        "Phone_No": "+966555822583",
        "Face_Image": "https://i.postimg.cc/W4jcrfWD/Nouf-Alqahtani.jpg",
        "job_title": "Security Officer",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP006",
        "password": "pass006",
        "F_Name": "Tariq",
        "L_Name": "AlHarbi",
        "Phone_No": "+966548756241",
        "Face_Image": "https://i.postimg.cc/KcKcmwdF/Tariq-Al-Harbi.jpg",
        "job_title": "Receptionist",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP007",
        "password": "pass007",
        "F_Name": "Lama",
        "L_Name": "Alshammari",
        "Phone_No": "+966555822583",
        "Face_Image": "https://i.postimg.cc/vmdbhmBZ/Lama-Alshammari.jpg",
        "job_title": "Security Manager",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP008",
        "password": "pass008",
        "F_Name": "Omar",
        "L_Name": "Almutairi",
        "Phone_No": "+966500000008",
        "Face_Image": "https://i.postimg.cc/yN72W3xc/Omar-Almutairi.jpg",
        "job_title": "Network Engineer",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP009",
        "password": "pass009",
        "F_Name": "Fatimah",
        "L_Name": "Alqahtani",
        "Phone_No": "+966500000009",
        "Face_Image": "https://i.postimg.cc/Vs7sw-17K/Fatimah-Alqahtani.png",
        "job_title": "IT Support",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP010",
        "password": "pass010",
        "F_Name": "Yousef",
        "L_Name": "Bin Saud",
        "Phone_No": "+966500000010",
        "Face_Image": "https://i.postimg.cc/nhxnYzMc/Yousef-Bin-Saud.jpg",
        "job_title": "Security Staff",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP011",
        "password": "pass011",
        "F_Name": "Maha",
        "L_Name": "Alshehri",
        "Phone_No": "+966500000011",
        "Face_Image": "https://i.postimg.cc/ZRwmJFLW/Maha-Alshehri.jpg",
        "job_title": "HR Manager",
        "company_id": "MOCK001"
    },
    {
        "employee_id": "EMP012",
        "password": "pass012",
        "F_Name": "Fahad",
        "L_Name": "Almalki",
        "Phone_No": "+966500000012",
        "Face_Image": "https://i.postimg.cc/Vk0k4TWD/Fahad-Almalki.jpg",
        "job_title": "Security Officer",
        "company_id": "MOCK001"
    }
]

# ✅ جلب جميع الموظفين (mock أو API حقيقي)
def fetch_all_employees_from_company():
    if USE_REAL_API:
        try:
            response = requests.get(REAL_API_URL)
            response.raise_for_status()
            employees = response.json()
        except Exception as e:
            print("❌ Error fetching from real API:", e)
            return []
    else:
        employees = mock_company_data

    return employees

# ✅ جلب موظف معيّن (مثلاً مع Webhook)
def get_employee_by_id_from_company(employee_id: str):
    employees = fetch_all_employees_from_company()
    for emp in employees:
        if emp["employee_id"] == employee_id:
            return {
                "employee_id": emp["employee_id"],
                "name": f"{emp['F_Name']} {emp['L_Name']}",
                "phone": emp["Phone_No"],
                "face_image": emp.get("Face_Image", ""),
                "job_title": emp.get("job_title", ""),
                "company_id": emp.get("company_id", "")
            }
    return None

# ✅ التحقق من الدخول (مثلاً للموظفين الأمنيين فقط)
def verify_login_and_get_info(employee_id: str, password: str):
    employees = fetch_all_employees_from_company()

    for emp in employees:
        if emp["employee_id"] == employee_id and emp["password"] == password:
            job_title = emp.get("job_title", "")
            role = 0 if "security" in job_title.lower() else 1

            return {
                "employee_id": emp["employee_id"],
                "name": f"{emp['F_Name']} {emp['L_Name']}",
                "phone": emp["Phone_No"],
                "face_image": emp.get("Face_Image", ""),
                "job_title": job_title,
                "company_id": emp.get("company_id", ""),
                "role": role
            }
    return None
