import cloudinary
import cloudinary.uploader
import uuid

# ⚙️ إعداد Cloudinary (تأكدي إنك تحفظيها .env لاحقًا للإنتاج)
cloudinary.config( 
    cloud_name = "CLOUDINARY_CLOUD_NAME", 
    api_key = "CLOUDINARY_API_KEY", 
    api_secret = "CLOUDINARY_API_SECRET"
)

# 📤 دالة رفع صورة وإرجاع الرابط
def upload_image_to_cloudinary(image_bytes: bytes, folder: str = "rakn") -> str:
    # نولّد اسم عشوائي
    public_id = str(uuid.uuid4())
    full_id = f"{folder}/{public_id}"

    # رفع الصورة
    result = cloudinary.uploader.upload(image_bytes, public_id=full_id)
    return result["secure_url"]
