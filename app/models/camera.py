from pydantic import BaseModel
from typing import Literal

class DroneCamera(BaseModel):
    camera_id: str =None
    model: str
    battery: str
    brand: str
    color: str
    status: Literal["On", "Off"]

class GateCamera(BaseModel):
    camera_id: str = None
    model: str
    resolution: str
    brand: str
    color: str
    status: Literal["On", "Off"]
    
class UpdateGateCamera(BaseModel):
    model: str
    resolution: str
    brand: str
    color: str
    status: Literal["On", "Off"]
    
class UpdateDroneCamera(BaseModel):
    model: str
    battery: str
    brand: str
    color: str
    status: Literal["On", "Off"]

