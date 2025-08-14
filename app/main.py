# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.equipment import router as equipment_router
from .config import settings

app = FastAPI(title=settings.app_name, version=settings.version)

# CORS для фронта (Vite/Tauri) в dev
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:1420",  # часто порт Tauri dev
    "http://127.0.0.1:1420",
    "tauri://localhost",  # схема Tauri
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],  # сейчас только read-only
    allow_headers=["*"],
)

app.include_router(equipment_router)


@app.get("/")
def root():
    return {"app": settings.app_name, "version": settings.version}
