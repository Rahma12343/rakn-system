import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase-adminsdk.json")

# تأكد أنه ما تم تهيئة Firebase مسبقًا
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ⬅️ يمثل الموظف الأمني الحالي الذي سجل الدخول
current_security_id = None