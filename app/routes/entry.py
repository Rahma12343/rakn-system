from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from app.ai_models.license_plate.license_plate_model import recognize_license_plate
from app.services.temp_plate_store import save_temp_plate
from app.services.cloudinary_uploader import upload_image_to_cloudinary

router = APIRouter()

@router.post("/plate")
async def save_plate(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()

        # ⏫ رفع الصورة إلى Cloudinary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plate_url = upload_image_to_cloudinary(image_bytes, folder="plates")

        # 🚘 التعرف على اللوحة
        plate_number = recognize_license_plate(image_bytes)
        if plate_number == "UNKNOWN" or plate_number == "ERROR":
            raise HTTPException(status_code=400, detail="❌ لم يتم التعرف على اللوحة")

        # 📝 حفظ الرقم والرابط مؤقتًا
        save_temp_plate(plate_number, plate_url)

        return {
            "status": "✅ plate saved",
            "plate_number": plate_number,
            "plate_image_url": plate_url
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Internal Error: {str(e)}")











#router = APIRouter()

#class EntryInput(BaseModel):
    #plate_image: str
    #face_image: str

#@router.post("/entry")
#def simulate_entry(data: EntryInput):
    #return log_parking_entry(data.plate_image, data.face_image)

