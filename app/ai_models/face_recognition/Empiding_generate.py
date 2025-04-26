import numpy as np
import requests
from PIL import Image
from io import BytesIO
from mtcnn.mtcnn import MTCNN
from keras_facenet import FaceNet
from app.services.company_api import fetch_all_employees_from_company
from app.config import db

# تحميل كاشف الوجه وموديل FaceNet
detector = MTCNN()
embedder = FaceNet()

def load_image_from_url(url):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        return np.array(img)
    except Exception as e:
        print(f"❌ Error loading image from {url}: {e}")
        return None

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

def save_face_embedding(employee_id, embedding):
    try:
        doc_ref = db.collection("face_embeddings").document(employee_id)
        doc = doc_ref.get()

        if doc.exists:
            print(f"⚠ Embedding already exists for {employee_id}, skipping.")
            return

        doc_ref.set({
            "employee_id": employee_id,
            "embedding": embedding
        })
        print(f"✅ Saved embedding for {employee_id}")

    except Exception as e:
        print(f"❌ Failed to save embedding for {employee_id}: {e}")

def generate_and_save_all_embeddings():
    employees = fetch_all_employees_from_company()
    for emp in employees:
        image_url = emp.get("Face_Image", "")
        if not image_url:
            continue

        img_array = load_image_from_url(image_url)
        if img_array is None:
            continue

        face = detect_face(img_array)
        if face is None:
            print(f"🚫 No face detected for {emp['employee_id']}")
            continue

        embedding = embedder.embeddings([face])[0]
        save_face_embedding(emp["employee_id"], embedding.tolist())
