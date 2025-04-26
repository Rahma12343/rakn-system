from fastapi import APIRouter, HTTPException
from app.models.notification import Notification
from app.config import db, current_security_id
from datetime import datetime
from firebase_admin import firestore  # تأكد إنها موجودة بالأعلى

router = APIRouter()

# ✅ إنشاء إشعار جديد
@router.post("/")
def create_notification(notification: Notification):
    try:
        now = datetime.now()

        if not notification.id:
            notification.id = str(int(now.timestamp() * 1000))

        if not notification.timestamp:
            notification.timestamp = now.isoformat()

        if not notification.type:
            notification.type = "general"

        notif_data = notification.dict()

        if "is_read" not in notif_data:
            notif_data["is_read"] = False  # ✅ تأكد أن كل إشعار جديد is_read=False

        db.collection("notifications").document(notification.id).set(notif_data)

        return {"message": "Notification created"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}")
def get_my_notifications(employee_id: str, unread_only: bool = False):
    try:
        query = db.collection("notifications").where("employee_id", "==", employee_id)

        if unread_only:
            query = query.where("is_read", "==", False)

        results = query.stream()

        notifications = [
            {**doc.to_dict(), "id": doc.id}
            for doc in results
        ]
        return {"notifications": notifications}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ✅ تعليم إشعار كمقروء
@router.patch("/{notification_id}/read")
def mark_as_read(notification_id: str):
    try:
        notif_ref = db.collection("notifications").document(notification_id)
        notif_ref.update({"is_read": True})
        return {"message": "Notification marked as read"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ تعليم جميع إشعارات الموظف كمقروءة دفعة وحدة
@router.post("/mark_read/{employee_id}")
def mark_all_as_read(employee_id: str):
    try:
        query = db.collection("notifications") \
            .where("employee_id", "==", employee_id) \
            .where("is_read", "==", False)
        
        notifications = query.stream()

        batch = db.batch()
        for noti in notifications:
            batch.update(noti.reference, {"is_read": True})

        batch.commit()

        return {"message": "✅ All notifications marked as read"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
