from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

# 自动创建所有数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GALCA (Grid Asset Lifecycle Cost Agents) API",
    description="电网资产全寿命成本多智能体平台的后端引擎",
    version="2.0.0"
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "GALCA 核心工业智能体平台后端已启动 ⚡"}

@app.post("/api/v1/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    # 占位：接收前端拖拽的台账表格和JPG工单
    return {"message": f"成功接收 {len(files)} 个文件，准备进入多模态智能体提取队列"}

@app.get("/api/v1/records")
def get_historical_records(db: Session = Depends(get_db)):
    # 读取历史的提取记录 (供前端表格展示)
    records = db.query(models.EquipmentCostRecord).limit(100).all()
    return records

@app.get("/api/v1/forecast/{equipment_type}")
def get_equipment_forecast(equipment_type: str, db: Session = Depends(get_db)):
    # 读取机器学习引擎计算好的多项式曲线
    forecast = db.query(models.ForecastResult).filter(models.ForecastResult.equipment_type == equipment_type).first()
    if forecast:
        return {"equipment": equipment_type, "data": forecast}
    return {"error": "尚未生成预测结果，请先上传数据分析"}
