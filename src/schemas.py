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

from pydantic import BaseModel, Field
from typing import List, Optional

class EquipmentCostRecord(BaseModel):
    """单条设备全生命周期成本记录 (LCC)"""
    equipment_type: str = Field(description="设备类型，例如：高压熔断器、隔离开关、交流避雷器、电缆终端")
    equipment_model: str = Field(description="设备规格或型号")
    cost_category: str = Field(
        description="成本类别，必须是以下之一：初始投资成本、运行成本、维护成本、故障成本、退役处理成本"
    )
    cost_subcategory: Optional[str] = Field(description="成本子项，例如：日常维护、停电损失、拆除费用等")
    amount: float = Field(description="发生的金额（万元或元，请统一转换为万元输出）")
    date: str = Field(description="费用发生或合同签署的日期 (YYYY-MM-DD)")
    source_document: str = Field(description="数据来源的合同编号或工单编号")

class DocumentExtractionResult(BaseModel):
    """从单个文件（合同/工单/发票）中提取的所有成本记录汇总"""
    records: List[EquipmentCostRecord]