# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.equipment import router as equipment_router
from .config import settings

app = FastAPI(title=settings.app_name, version=settings.version)


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:1420",
    "http://127.0.0.1:1420",
    "tauri://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,  # creds не нужны; можно оставить True при необходимости
    allow_methods=["*"],  # разрешаем OPTIONS/POST/PATCH/DELETE/GET
    allow_headers=["*"],  # Content-Type, Authorization и пр.
)

app.include_router(equipment_router)


@app.get("/")
def root():
    return {"app": settings.app_name, "version": settings.version}
