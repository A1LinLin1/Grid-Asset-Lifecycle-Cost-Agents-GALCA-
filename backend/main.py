import os
import shutil
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine, get_db

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GALCA Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_documents_background(file_paths: List[str], db: Session):
    print(f"🚀 [后台任务] 开始处理 {len(file_paths)} 个文件...")
    print("✅ [后台任务] 智能体提取完成！")

@app.post("/api/v1/upload")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    saved_paths = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
    background_tasks.add_task(process_documents_background, saved_paths, db)
    return {"status": "success", "message": f"成功接收 {len(files)} 个文件。"}

@app.get("/api/v1/records")
def get_historical_records(db: Session = Depends(get_db)):
    return db.query(models.EquipmentCostRecord).limit(100).all()

@app.get("/api/v1/forecast/{equipment_type}")
def get_equipment_forecast(equipment_type: str, db: Session = Depends(get_db)):
    forecast = db.query(models.ForecastResult).filter(models.ForecastResult.equipment_type == equipment_type).first()
    if forecast:
        return {"equipment": equipment_type, "data": forecast}
    return {"error": "未找到"}

# 将前端 Vue 编译后的 dist 目录挂载到根路径
app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")
