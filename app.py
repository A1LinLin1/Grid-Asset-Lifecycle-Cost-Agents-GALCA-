import streamlit as st
import os
import glob
from src.main_graph import app as galca_app  # 导入我们编译好的 LangGraph 多智能体工作流

# 1. 页面基本配置
st.set_page_config(
    page_title="GALCA | 电网装备LCC分析",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ GALCA 装备全生命周期成本智能分析平台")
st.markdown("上传多模态的**台账表格(Excel)、采购合同(Word/TXT)、或现场维修发票(图片)**，系统将利用 Vision-LLM 智能体提取数据，并动态路由至专用的 LCC 数学模型进行趋势预测。")

# 2. 文件上传区
uploaded_files = st.file_uploader(
    "请拖拽或选择文件上传", 
    type=["xlsx", "csv", "txt", "docx", "pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# 3. 运行控制按钮
# 3. 运行控制按钮
if st.button("🚀 启动多智能体分析引擎", type="primary"):
    if not uploaded_files:
        st.warning("⚠️ 请先上传至少一个数据文件！")
    else:
        # --- 【新增修复】清理旧的上传文件、旧图表和旧报告 ---
        upload_dir = "data/uploads"
        os.makedirs(upload_dir, exist_ok=True)
        
        # 1. 清理旧图表
        for old_img in glob.glob("data/forecast_*.png"):
            os.remove(old_img)
            
        # 2. 清理旧报告
        old_report = "data/电网装备LCC综合评估报告.md"
        if os.path.exists(old_report):
            os.remove(old_report)
            
        # 3. 清理旧上传文件 (可选，防止文件夹无限变大)
        for old_file in glob.glob(os.path.join(upload_dir, "*")):
            os.remove(old_file)
        # --------------------------------------------------

        # 进度提示
        with st.status("正在唤醒多智能体工作流...", expanded=True) as status:
            file_paths = []
            st.write("📥 正在暂存本次上传的文件...")
            for f in uploaded_files:
                file_path = os.path.join(upload_dir, f.name)
                with open(file_path, "wb") as out_file:
                    out_file.write(f.read())
                file_paths.append(file_path)
            
            st.write("🧠 智能体正在跨模态提取特征并进行数学拟合 (这可能需要几十秒)...")
            
            # --- 调用 LangGraph 主流程 ---
            inputs = {"file_paths": file_paths}
            config = {"recursion_limit": 50}
            
            try:
                for output in galca_app.stream(inputs, config):
                    if "extract" in output:
                        st.write(f"✅ 数据提取完成，共识别 {len(output['extract']['extracted_records'])} 条有效记录。")
                    elif "analyze" in output:
                        st.write("✅ LCC 动态拟合完成，专属图表已生成。")
                    elif "report" in output:
                        st.write("✅ 专家评估报告生成完毕。")
                status.update(label="分析流程全部完成！", state="complete", expanded=False)
            except Exception as e:
                status.update(label="运行出错", state="error", expanded=True)
                st.error(f"系统运行遇到错误: {str(e)}")
                st.stop()

        # 4. 结果展示区
        st.divider()
        st.subheader("📊 分析结果展示")
        
        col1, col2 = st.columns([1, 1.2])
        
        # 左侧：展示生成的拟合图表
        with col1:
            st.markdown("### 📈 成本预测拟合图")
            # 此时 glob 抓到的绝对只有本次新生成的图表！
            plot_files = glob.glob("data/forecast_*.png")
            if plot_files:
                for img_path in plot_files:
                    st.image(img_path, use_container_width=True)
            else:
                st.info("本次分析未生成足够的历史趋势图表（可能是上传的数据不足 3 个周期）。")
                
        # 右侧：展示 Markdown 报告
        with col2:
            report_path = "data/电网装备LCC综合评估报告.md"
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as f:
                    report_content = f.read()
                with st.container(border=True):
                    st.markdown(report_content)
            else:
                st.error("未能找到生成的 Markdown 报告文件。")
            