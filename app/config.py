import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# ✅ أخذ بيانات الاعتماد من متغير البيئة بدل ملف
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
cred = credentials.Certificate(json.loads(firebase_credentials))

# مسجّلًا Firebase أنك لم تهيئه مسبقاً
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ➡️ يمثل الموظف الأمني الحالي الذي سجل الدخول
current_security_id = None
