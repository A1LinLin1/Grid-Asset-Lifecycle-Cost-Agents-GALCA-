from typing import Annotated, List, Dict, Union
from typing_extensions import TypedDict
import operator

class GALCAState(TypedDict):
    # 文件路径列表
    file_paths: List[str]
    # 提取出的结构化合同信息
    contracts: List[Dict]
    # 提取出的所有成本流水
    all_costs: Annotated[List[Dict], operator.add]
    # 预测结果
    forecast_report: Dict
    # 下一步去哪里的决策标志
    next_step: str