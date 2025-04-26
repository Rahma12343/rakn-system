# services/camera_service.py
import uuid
from typing import List
from app.config import db
from app.models.camera import DroneCamera, GateCamera

# إضافة كاميرا

def add_drone_camera(data: dict) -> str:
    camera_id = str(uuid.uuid4())
    data["camera_id"] = camera_id
    db.collection("drone_cameras").document(camera_id).set(data)
    return camera_id

def add_gate_camera(data: dict) -> str:
    camera_id = str(uuid.uuid4())
    data["camera_id"] = camera_id
    db.collection("gate_cameras").document(camera_id).set(data)
    return camera_id

# عرض جميع الدرونز

def get_all_drones() -> List[DroneCamera]:
    docs = db.collection("drone_cameras").stream()
    return [DroneCamera(**doc.to_dict()) for doc in docs]

# عرض جميع كاميرات البوابة

def get_all_gate_cameras() -> List[GateCamera]:
    docs = db.collection("gate_cameras").stream()
    return [GateCamera(**doc.to_dict()) for doc in docs]


# حذف درون
def delete_drone_camera(camera_id: str) -> bool:
    doc_ref = db.collection("drone_cameras").document(camera_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        return True
    return False

# حذف كاميرا بوابة
def delete_gate_camera(camera_id: str) -> bool:
    doc_ref = db.collection("gate_cameras").document(camera_id)
    if doc_ref.get().exists:
        doc_ref.delete()
        return True
    return False


# تعديل درون
def update_drone_camera(camera_id: str, data: dict) -> bool:
    doc_ref = db.collection("drone_cameras").document(camera_id)
    if doc_ref.get().exists:
        doc_ref.update(data)
        return True
    return False

# تعديل كاميرا بوابة
def update_gate_camera_data(camera_id: str, data: dict) -> bool:
    doc_ref = db.collection("gate_cameras").document(camera_id)
    if doc_ref.get().exists:
        doc_ref.update(data)
        return True
    return False
