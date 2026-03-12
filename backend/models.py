from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class EquipmentCostRecord(Base):
    __tablename__ = "equipment_cost_records"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index=True, comment="关联的分析批次ID")
    equipment_type = Column(String, index=True, comment="设备类型")
    equipment_model = Column(String, comment="设备规格或型号")
    cost_category = Column(String, comment="成本类别(初始/运行/维护等)")
    cost_subcategory = Column(String, nullable=True, comment="成本子项")
    amount = Column(Float, comment="发生金额(万元)")
    date = Column(String, comment="费用发生日期")
    source_document = Column(String, comment="数据来源(文件名或编号)")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ForecastResult(Base):
    __tablename__ = "forecast_results"
    
    id = Column(Integer, primary_key=True, index=True)
    equipment_type = Column(String, unique=True, index=True)
    algo_used = Column(String, comment="预测使用的算法模型(如 PolynomialRegression)")
    equation = Column(String, comment="拟合方程描述")
    forecast_json = Column(String, comment="未来预测点的序列化JSON数据")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
