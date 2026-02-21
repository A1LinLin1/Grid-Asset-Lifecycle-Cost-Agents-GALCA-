import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
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
        # 使用 Gemini 1.5 Flash (速度快且便宜)
        self.llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview")

    def extract_contract(self, text: str) -> ContractInfo:
        # 使用结构化输出功能
        structured_llm = self.llm.with_structured_output(ContractInfo)
        
        prompt = ChatPromptTemplate.from_template(
            "你是一个专业的电网财务审计助手。请从以下文本中提取关键合同信息：\n\n{text}"
        )
        
        chain = prompt | structured_llm
        return chain.invoke({"text": text})

# 测试代码
if __name__ == "__main__":
    with open('data/sample_contract.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    extractor = InformationExtractor()
    result = extractor.extract_contract(content)
    print(f"提取结果: {result}")