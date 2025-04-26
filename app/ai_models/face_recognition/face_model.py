import numpy as np
import requests
from PIL import Image
from io import BytesIO
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
from app.config import db
from sklearn.metrics.pairwise import cosine_similarity

# تحميل MTCNN و FaceNet
detector = MTCNN()
embedder = FaceNet()

# تحميل الصورة من URL أو من ملف/بايتات
def load_image(image_input):
    try:
        if isinstance(image_input, str):  # URL
            response = requests.get(image_input)
            img = Image.open(BytesIO(response.content)).convert('RGB')
        else:  # BytesIO أو ملف
            img = Image.open(image_input).convert('RGB')
        return np.array(img)
    except Exception as e:
        print(f"❌ Error loading image: {e}")
        return None

# استخراج الوجه من الصورة
def detect_face(image):
    try:
        results = detector.detect_faces(image)
        if results:
            x, y, w, h = results[0]["box"]
            x, y = abs(x), abs(y)
            face = image[y:y+h, x:x+w]
            return face
    except Exception as e:
        print(f"❌ Error detecting face: {e}")
    return None

# مقارنة الوجه الجديد مع الموظفين في قاعدة البيانات
def compare_face(input_image, threshold=0.5):
    img_array = load_image(input_image)
    if img_array is None:
        return None

    face = detect_face(img_array)
    if face is None:
        print("🚫 No face detected")
        return None

    input_embedding = embedder.embeddings([face])[0]

    # استرجاع كل embeddings من Firestore
    embeddings_ref = db.collection("face_embeddings").stream()
    best_match = None
    highest_similarity = -1

    for doc in embeddings_ref:
        data = doc.to_dict()
        stored_embedding = np.array(data["embedding"])
        similarity = cosine_similarity([input_embedding], [stored_embedding])[0][0]

        if similarity > highest_similarity and similarity >= threshold:
            highest_similarity = similarity
            best_match = {
                "employee_id": data["employee_id"],
                "similarity": similarity
            }

    if best_match:
        print(f"✅ Match found: {best_match}")
        return best_match
    else:
        print("❌ No matching face found")
        return None

# 📌 إضافة موظف جديد للنظام بوجهه
def process_new_employee_face(image_input, employee_id):
    img_array = load_image(image_input)
    if img_array is None:
        return False

    face = detect_face(img_array)
    if face is None:
        print("🚫 No face detected")
        return False

    embedding = embedder.embeddings([face])[0]

    # حفظ في Firebase
    db.collection("face_embeddings").add({
        "employee_id": employee_id,
        "embedding": embedding.tolist()
    })

    print(f"✅ تم تسجيل الموظف {employee_id}")
    return True
