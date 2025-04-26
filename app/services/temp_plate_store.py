from datetime import datetime

# تخزين مؤقت داخل الذاكرة
temp_plates = {}

def save_temp_plate(plate_number, plate_image_url=None, timestamp=None):
    if not timestamp:
        timestamp = datetime.utcnow().isoformat()
    
    temp_plates["latest_plate"] = {
        "plate_number": plate_number,
        "plate_image_url": plate_image_url,  # ✅ إضافة رابط الصورة
        "timestamp": timestamp
    }

def get_latest_plate():
    return temp_plates.get("latest_plate", None)

def clear_temp_plate():
    temp_plates.pop("latest_plate", None)
