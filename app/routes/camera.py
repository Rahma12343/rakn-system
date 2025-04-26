from fastapi import APIRouter
from typing import List
from fastapi import HTTPException
from app.models.camera import DroneCamera, GateCamera, UpdateGateCamera,UpdateDroneCamera
from app.services.camera_service import (
    add_drone_camera, add_gate_camera,
    get_all_drones, get_all_gate_cameras,
    delete_drone_camera, delete_gate_camera,
    update_drone_camera, update_gate_camera_data


)

router = APIRouter()

# ✅ إضافة درون
@router.post("/add-drone")
def create_drone_camera(camera: DroneCamera):
    camera_id = add_drone_camera(camera.dict())
    return {"message": "Drone camera added ✅", "camera_id": camera_id}

# ✅ إضافة كاميرا بوابة
@router.post("/add-gate")
def create_gate_camera(camera: GateCamera):
    camera_id = add_gate_camera(camera.dict())
    return {"message": "Gate camera added ✅", "camera_id": camera_id}

# ✅ عرض جميع الدرونز
@router.get("/drones", response_model=List[DroneCamera])
def list_drones():
    return get_all_drones()

# ✅ عرض جميع كاميرات البوابة
@router.get("/gates", response_model=List[GateCamera])
def list_gate_cameras():
    return get_all_gate_cameras()


# 🗑️ حذف كاميرا درون
@router.delete("/drone/{camera_id}")
def remove_drone_camera(camera_id: str):
    if delete_drone_camera(camera_id):
        return {"message": "Drone camera deleted ✅"}
    raise HTTPException(status_code=404, detail="Drone camera not found")

# 🗑️ حذف كاميرا بوابة
@router.delete("/gate/{camera_id}")
def remove_gate_camera(camera_id: str):
    if delete_gate_camera(camera_id):
        return {"message": "Gate camera deleted ✅"}
    raise HTTPException(status_code=404, detail="Gate camera not found")


# تعديل كاميرا درون

@router.put("/drone/{camera_id}")
def edit_drone_camera(camera_id: str, camera: UpdateDroneCamera):
    if update_drone_camera(camera_id, camera.dict()):
        return {"message": "Drone camera updated ✅"}
    raise HTTPException(status_code=404, detail="Drone camera not found")

# تعديل كاميرا بوابة
@router.put("/gate/{camera_id}")
def update_gate_camera(camera_id: str, camera: UpdateGateCamera):
    if update_gate_camera_data(camera_id, camera.dict()):
        return {"message": "Gate camera updated ✅"}
    raise HTTPException(status_code=404, detail="Gate camera not found")