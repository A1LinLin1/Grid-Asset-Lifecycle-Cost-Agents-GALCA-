import os
import pandas as pd
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# 导入我们之前写的组件
from src.loader import UniversalLoader
from src.extractor import InformationExtractor
from src.forecaster import CostForecaster

load_dotenv()

# 1. 定义状态结构
class GraphState(TypedDict):
    file_paths: List[str]
    extracted_records: List[dict]
    forecast_results: list
    final_output: str

# 2. 定义节点逻辑
def extraction_node(state: GraphState):
    """提取节点：遍历文件并识别数据"""
    all_data = []
    extractor = InformationExtractor()
    
    for path in state["file_paths"]:
        loader = UniversalLoader(path)
        if path.endswith(('.xlsx', '.csv')):
            df = loader.load_as_dataframe()
            # 简单清洗：假设我们需要日期和金额列
            temp_data = df.to_dict(orient='records')
            all_data.extend(temp_data)
        else:
            # 处理合同等文本
            text_doc = loader.load_as_text()
            contract = extractor.extract_contract(text_doc.page_content)
            all_data.append(contract.model_dump()) # 将 Pydantic 模型转为 dict 存储到状态中
            
    return {"extracted_records": all_data}

def analytics_node(state: GraphState):
    """分析节点：执行曲线拟合"""
    # 将提取的所有数据转为 DataFrame
    df = pd.DataFrame(state["extracted_records"])
    
    # 【新增的数据清洗逻辑】
    # 1. 过滤掉目标列为 NaN 的行，只保留真正包含运维支出数据的行
    target_column = '支出金额(万元)'
    if target_column in df.columns:
        # 丢弃没有金额的数据（比如合同数据）
        clean_df = df.dropna(subset=[target_column]).copy()
        
        # 2. 调用预测器
        forecaster = CostForecaster(degree=2)
        predictions = forecaster.fit_and_predict(clean_df, target_column)
        
        # 将 Numpy array 转为 list 以便存入状态
        return {"forecast_results": predictions.tolist()}
    else:
        # 如果根本没有找到目标列，返回空预测或错误提示
        return {"forecast_results": ["错误：未找到可拟合的成本列"]}

def report_node(state: GraphState):
    """报告节点：汇总结果"""
    res = f"分析完成。基于历史数据，未来 4 个周期的预计成本为: {state['forecast_results']}"
    return {"final_output": res}

# 3. 构建图 (Workflow)
workflow = StateGraph(GraphState)

# 添加节点
workflow.add_node("extract", extraction_node)
workflow.add_node("analyze", analytics_node)
workflow.add_node("report", report_node)

# 设置连线
workflow.set_entry_point("extract")
workflow.add_edge("extract", "analyze")
workflow.add_edge("analyze", "report")
workflow.add_edge("report", END)

# 编译
app = workflow.compile()

if __name__ == "__main__":
    # 测试运行
    inputs = {
        "file_paths": ["data/maintenance_records.xlsx", "data/sample_contract.txt"]
    }
    config = {"recursion_limit": 50}
    for output in app.stream(inputs, config):
        print("--- 节点输出 ---")
        print(output)