from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import auth, account, violation, camera, entry, notification, webhook
from app.routes import face  # ✅ جديد
from app.routes import whatsapp  # ✅ جديد

app = FastAPI(
    title="RAKN System API",
    description="Backend for the RAKN security parking violation system",
    version="1.0.0"
)

# ✅ السماح بالطلبات بين النطاقات
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ ربط المجلدات الثابتة (الفرونت)
app.mount("/Pages", StaticFiles(directory="frontend/Pages"), name="Pages")
app.mount("/Scripts", StaticFiles(directory="frontend/Scripts"), name="Scripts")
app.mount("/images", StaticFiles(directory="frontend/images"), name="images")
app.mount("/Global", StaticFiles(directory="frontend/Global"), name="Global")
app.mount("/sounds", StaticFiles(directory="frontend/sounds"), name="sounds")
app.mount("/videos", StaticFiles(directory="frontend/videos"), name="videos")
app.mount("/Txt", StaticFiles(directory="frontend/Txt"), name="Txt")
app.mount("/Docs", StaticFiles(directory="frontend/Docs"), name="Docs")

# ✅ ربط جميع الراوترات
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(account.router, prefix="/account", tags=["Account"])
app.include_router(violation.router, prefix="/violation", tags=["Violations"])
app.include_router(camera.router, prefix="/camera", tags=["Cameras"])
app.include_router(entry.router, prefix="/entry", tags=["Entry Logs"])
app.include_router(notification.router, prefix="/notification", tags=["Notifications"])
app.include_router(webhook.router, prefix="/webhook", tags=["Webhook"])
app.include_router(face.router, prefix="/face", tags=["Face Recognition"])
app.include_router(whatsapp.router, prefix="/whatsapp", tags=["WhatsApps"])


# ✅ عرض index.html لما يفتح رابط /
@app.get("/")
def root():
    return FileResponse("frontend/index.html")
