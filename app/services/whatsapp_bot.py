from twilio.rest import Client
from app.services.firebase_db import get_violations_by_phone


ACCOUNT_SID = "TWILIO_ACCOUNT_SID"
AUTH_TOKEN = "TWILIO_AUTH_TOKEN"
FROM_WHATSAPP = "TWILIO_WHATSAPP_NUMBER"

client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_violation_whatsapp(
    to_number: str,
    plate_number: str,
    date: str,
    violation_type: str,
    image_url: str,
    violation_id: str,
    employee_name: str,
):
    if violation_type == "Warning":
        message = f"""
👋 مرحبًا، نحن فريق *ركن* لرصد وتنظيم مواقف السيارات.

⚠️ تم رصد *إنذار* على سيارتك بسبب وقوف غير نظامي.

👤 الموظف: {employee_name}
🔢 رقم اللوحة: {plate_number}
🆔 رقم الإنذار: {violation_id}
📆 التاريخ: {date}

📷 صورة مرفقة

📌 يرجى الانتباه لتفادي تسجيل مخالفة في المرة القادمة.

📋 لعرض جميع مخالفاتك السابقة، أرسل: عرض المخالفات
""".strip()
    else:
        message = f"""
👋 مرحبًا، نحن فريق *ركن* لرصد وتنظيم مواقف السيارات.

🚨 تم تسجيل *مخالفة* على سيارتك بسبب وقوف غير نظامي.

👤 الموظف: {employee_name}
🔢 رقم اللوحة: {plate_number}
🆔 رقم المخالفة: {violation_id}
📆 التاريخ: {date}


⚠️ يرجى مراجعة الإدارة لمزيد من التفاصيل.

📋 لعرض جميع مخالفاتك السابقة، أرسل: عرض المخالفات
""".strip()

    try:
        client.messages.create(
            from_=FROM_WHATSAPP,
            to=f"whatsapp:{to_number}",
            body=message,
            media_url=[image_url]
        )
        print(f"✅ تم إرسال إشعار WhatsApp ({violation_type}) إلى {to_number}")
    except Exception as e:
        print(f"❌ فشل إرسال WhatsApp: {e}")
