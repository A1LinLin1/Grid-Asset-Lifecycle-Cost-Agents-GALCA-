from pydantic import BaseModel, Field
from typing import List, Optional

class ContractInfo(BaseModel):
    """从合同中提取的关键财务信息"""
    project_name: str = Field(description="合同或项目名称")
    contract_id: str = Field(description="合同编号")
    total_amount: float = Field(description="合同总金额（单位：元）")
    sign_date: str = Field(description="签署日期，格式通常为 YYYY-MM-DD")

class CostPoint(BaseModel):
    """单条成本记录"""
    date: str = Field(description="发生日期")
    amount: float = Field(description="金额")
    description: Optional[str] = Field(description="费用描述")

class CostDataList(BaseModel):
    """一系列成本数据，用于曲线拟合"""
    items: List[CostPoint]