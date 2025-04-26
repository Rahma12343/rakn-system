import numpy as np
import cv2
from tensorflow.keras.models import load_model

# تحميل المودل المدرب مرة واحدة فقط
model = load_model('app/ai_models/violation_detector/parking_model_rakn.h5')
classes = ['correct', 'double', 'not_parking_zone']

def predict_violation(image_bytes: bytes) -> dict:
    try:
        # تحويل الصورة من bytes إلى مصفوفة NumPy
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("❌ Failed to decode image.")

        # تجهيز الصورة
        img_resized = cv2.resize(img, (224, 224)) / 255.0
        img_input = np.expand_dims(img_resized, axis=0)

        # التنبؤ
        prediction = model.predict(img_input)[0]
        class_index = int(np.argmax(prediction))
        confidence = float(prediction[class_index])

        return {
            "class": classes[class_index],
            "confidence": confidence
        }

    except Exception as e:
        return {
            "error": f"⚠️ Prediction failed: {str(e)}"
        }
