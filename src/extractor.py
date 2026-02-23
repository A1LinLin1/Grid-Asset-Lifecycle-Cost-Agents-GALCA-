import os
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from src.schemas import ContractInfo
from dotenv import load_dotenv

# 配置 API KEY
load_dotenv()
os.environ["http_proxy"] = os.getenv("HTTP_PROXY", "")
os.environ["https_proxy"] = os.getenv("HTTPS_PROXY", "")
google_api_key = os.getenv("GOOGLE_API_KEY", "")
if google_api_key:
    os.environ["GOOGLE_API_KEY"] = google_api_key

class InformationExtractor:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            timeout = 120,
            transport = "rest",
            max_retries = 2                              
        )

    def extract_contract(self, text: str) -> ContractInfo:
        # 使用结构化输出功能
        structured_llm = self.llm.with_structured_output(ContractInfo)
        
        prompt = ChatPromptTemplate.from_template(
            "你是一个专业的电网财务审计助手。请从以下文本中提取关键合同信息：\n\n{text}"
        )
        
        chain = prompt | structured_llm
        return chain.invoke({"text": text})
    
    def extract_from_image(self, image_path: str) -> ContractInfo:
        """【新增】直接从图片中提取结构化信息"""
        # 1. 将图片转为 Base64 编码
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode("utf-8")
        
        # 2. 构造多模态提示词
        message = HumanMessage(
            content=[
                {"type": "text", "text": "你是一个专业的电网审计员。请提取这张工单/发票图片中的关键信息。如果没有合同号，请用工单号代替；总金额请提取数字。"},
                {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}"}
            ]
        )
        
        # 3. 调用带有结构化输出的模型
        structured_llm = self.llm.with_structured_output(ContractInfo)
        return structured_llm.invoke([message])

# # 测试代码
# if __name__ == "__main__":
#     with open('data/sample_contract.txt', 'r', encoding='utf-8') as f:
#         content = f.read()
    
#     extractor = InformationExtractor()
#     result = extractor.extract_contract(content)
#     # 测试图片提取
#     image_file = 'data/sample_receipt.jpg'
#     if os.path.exists(image_file):
#         print("正在让 Gemini 看图提取数据，请稍候...")
#         result = extractor.extract_from_image(image_file)
#         print(f"🖼️ 图片提取结果: {result}")
#     else:
#         print(f"找不到图片 {image_file}，请先运行 generate_image.py")
#     print(f"提取结果: {result}")