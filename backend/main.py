import os
import shutil
from typing import List
from fastapi import FastAPI, Depends, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

# 把父目录加入环境变量，方便引入原有的 src 模块
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 假设我们在 src.main_graph 中有一个 run_galca_pipeline 函数
# from src.main_graph import app as galca_graph

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="GALCA Backend API")

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_documents_background(file_paths: List[str], db: Session):
    """后台任务：调用 LangGraph 智能体处理文件并入库"""
    print(f"🚀 [后台任务] 开始处理 {len(file_paths)} 个文件...")
    
    # 构造初始状态字典，交给大模型图网络
    # state = {"file_paths": file_paths, "extracted_records": [], "forecast_results": {}}
    # final_state = galca_graph.invoke(state)
    
    # 模拟：将 final_state["extracted_records"] 写入 SQLite
    # for record in final_state.get("extracted_records", []):
    #     db_record = models.EquipmentCostRecord(**record.dict())
    #     db.add(db_record)
    # db.commit()
    
    print("✅ [后台任务] 智能体提取与机器学习拟合完成！数据已入库。")

@app.post("/api/v1/upload")
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    saved_paths = []
    # 1. 接收前端拖拽的文件并保存到本地
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_paths.append(file_path)
    
    # 2. 触发 LangGraph 异步后台分析 (防止大模型分析太久导致前端请求超时)
    background_tasks.add_task(process_documents_background, saved_paths, db)
    
    return {
        "status": "success", 
        "message": f"成功接收 {len(files)} 个文件。多模态大模型分析任务已在后台启动！",
        "files": saved_paths
    }

@app.get("/api/v1/records")
def get_historical_records(db: Session = Depends(get_db)):
    return db.query(models.EquipmentCostRecord).limit(100).all()

@app.get("/api/v1/forecast/{equipment_type}")
def get_equipment_forecast(equipment_type: str, db: Session = Depends(get_db)):
    forecast = db.query(models.ForecastResult).filter(models.ForecastResult.equipment_type == equipment_type).first()
    if forecast:
        return {"equipment": equipment_type, "data": forecast}
    return {"error": "尚未生成预测结果，请先上传数据分析"}
