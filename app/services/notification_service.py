from app.config import db, current_security_id
from app.models.notification import Notification
from datetime import datetime

def send_notification_to_current_security(message: str, notif_type: str = "general"):
    if not current_security_id:
        print("⚠️ لا يوجد موظف أمني حالي لإرسال الإشعار.")
        return

    now = datetime.now()
    notification = Notification(
        id=str(int(now.timestamp() * 1000)),
        message=message,
        employee_id=current_security_id,
        is_read=False,
        timestamp=now.isoformat(),
        type=notif_type
    )

    db.collection("notifications").document(notification.id).set(notification.dict())
    print("🔔 إشعار جديد تم إرساله لموظف الأمن الحالي:", notification.dict())

