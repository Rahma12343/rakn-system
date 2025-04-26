import requests
from io import BytesIO
from PIL import Image
import numpy as np 
import re
import cv2
from ultralytics import YOLOv10
from paddleocr import PaddleOCR
from app.services.temp_plate_store import save_temp_plate


# تحميل نموذج YOLOv10
model = YOLOv10("app/ai_models/license_plate/best.pt")

# تهيئة OCR
ocr = PaddleOCR(use_angle_cls=True, use_gpu=False)

def recognize_license_plate(image_bytes: bytes) -> str:
    try:
        # فتح الصورة من الـ bytes
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        frame = np.array(img)

        # تمرير الصورة إلى الموديل
        results = model.predict(source=frame, conf=0.5, verbose=False)

        print("📦 YOLO Results:", results)

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cropped = frame[y1:y2, x1:x2]

                ocr_result = ocr.ocr(cropped, det=False, rec=True, cls=False)

                text = ""
                for r in ocr_result:
                    score = r[0][1]
                    score = int(score * 100) if not np.isnan(score) else 0
                    if score > 60:
                        text = r[0][0]

                text = re.sub(r'[\W]', '', text)
                text = text.replace("???", "").replace("O", "0").replace("粤", "")

                if text:
                    save_temp_plate(text)
                    return text

        return "UNKNOWN"
    
    except Exception as e:
        print("🚨 Error in recognize_license_plate:", e)
        return "ERROR"
