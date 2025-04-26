# app/utils.py

def normalize_plate(text: str) -> str:
    """
    تقوم بتوحيد تنسيق لوحة السيارة:
    - إزالة الفراغات والشرطات
    - تحويل الأحرف إلى كبيرة
    """
    return text.replace("-", "").replace(" ", "").upper()