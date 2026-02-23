import os
import pandas as pd
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv
import datetime

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
    """提取节点：遍历文件并分类识别数据"""
    all_data = []
    extractor = InformationExtractor()
    
    for path in state["file_paths"]:
        print(f"📄 正在处理文件: {path}")
        
        if path.endswith(('.xlsx', '.csv')):
            # 1. 处理表格流水
            loader = UniversalLoader(path)
            df = loader.load_as_dataframe()
            temp_data = df.to_dict(orient='records')
            all_data.extend(temp_data)
            
        elif path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 2. 【新增】处理图片扫描件
            print(f"   👁️ 启动视觉智能体解析图片...")
            contract = extractor.extract_from_image(path)
            all_data.append(contract.model_dump())
            
        else:
            # 3. 处理纯文本/PDF/Word合同
            print(f"   📝 启动文本智能体解析文档...")
            loader = UniversalLoader(path)
            text_doc = loader.load_as_text()
            contract = extractor.extract_contract(text_doc.page_content) 
            all_data.append(contract.model_dump())
            
    return {"extracted_records": all_data}

def analytics_node(state: GraphState):
    """分析节点：执行曲线拟合与保存图表"""
    df = pd.DataFrame(state["extracted_records"])
    target_column = '支出金额(万元)'
    
    if target_column in df.columns:
        # 过滤掉没有成本流水的数据（如文本合同）
        clean_df = df.dropna(subset=[target_column]).copy()
        
        forecaster = CostForecaster(degree=2)
        predictions = forecaster.fit_and_predict(clean_df, target_column)
        
        # 【新增】调用画图保存功能
        forecaster.save_plot(clean_df, predictions, target_column, save_path="data/forecast_plot.png")
        
        return {"forecast_results": predictions.tolist()}
    else:
        return {"forecast_results": []}

def report_node(state: GraphState):
    """报告节点：智能组装 Markdown 评估报告"""
    records = state["extracted_records"]
    forecast = state.get("forecast_results", [])
    
    # 将异构数据分类：包含 project_name 的是合同/工单，否则是历史台账
    contracts = [r for r in records if 'project_name' in r]
    history_count = len(records) - len(contracts)
    
    # --- 开始组装 Markdown 内容 ---
    md = f"# ⚡ 电网资产全生命周期成本评估报告\n\n"
    md += f"**生成时间：** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    md += f"---\n\n"
    
    # 模块 1：预测结果
    md += f"## 1. 资产历史与未来成本预测\n\n"
    md += f"系统成功解析了 **{history_count}** 条历史台账记录，并采用二项式回归模型进行了非线性拟合。未来 4 个周期的预计运维成本如下：\n\n"
    
    for i, val in enumerate(forecast, 1):
        md += f"- **T+{i} 周期**: 预计支出 **{val:.2f}** 万元\n"
        
    md += f"\n![成本预测趋势图](forecast_plot.png)\n"
    md += f"*(注：上图由 Scikit-Learn 后台自动化生成)*\n\n"
    
    # 模块 2：审计的异构文件汇总
    md += f"## 2. 关键合同与现场工单审计汇总\n\n"
    md += f"本次分析共通过多模态大模型从 Word、PDF、TXT 以及图片扫描件中成功提取并校验了 **{len(contracts)}** 份外部文件。关键财务信息如下：\n\n"
    
    # 绘制 Markdown 表格
    md += "| 项目名称 | 合同/工单编号 | 提取总金额 (元) | 签署日期 |\n"
    md += "| :--- | :--- | :--- | :--- |\n"
    for c in contracts:
        # 格式化金额，加上千分位逗号
        amt = f"{c.get('total_amount', 0):,.2f}"
        md += f"| {c.get('project_name')} | {c.get('contract_id')} | **¥ {amt}** | {c.get('sign_date')} |\n"
        
    md += f"\n---\n*报告由 GALCA (Grid Asset Lifecycle Cost Agents) 自动生成。*"
    
    # 写入文件
    report_path = "data/电网资产成本预测评估报告.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    res = f"✅ 分析完成！\n📊 曲线图已保存至: data/forecast_plot.png\n📄 报告已生成至: {report_path}"
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
    # 终极测试：同时丢入 Excel账单、TXT合同、JPG发票照片
    inputs = {
        "file_paths": [
            "data/maintenance_records.xlsx", 
            "data/sample_contract.txt",
            "data/sample_contract.docx",  # 新增的 Word 合同文件
            "data/sample_receipt.jpg"  # 新增的图片文件
        ]
    }
    config = {"recursion_limit": 50}
    for output in app.stream(inputs, config):
        print("--- 节点输出 ---")
        print(output)