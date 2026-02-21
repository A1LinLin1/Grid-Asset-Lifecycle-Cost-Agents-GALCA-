import pandas as pd
from unstructured.partition.auto import partition
from langchain_core.documents import Document

class UniversalLoader:
    """万能文档加载器：支持 PDF, DOCX, XLSX, JPG/PNG"""
    
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_as_dataframe(self):
        """专门针对 Excel 和 CSV 的表格数据"""
        if self.file_path.endswith(('.xlsx', '.xls')):
            return pd.read_excel(self.file_path)
        elif self.file_path.endswith('.csv'):
            return pd.read_csv(self.file_path)
        return None

    def load_as_text(self):
        """针对 PDF, Word 和 图片的非结构化提取"""
        # partition 函数会自动根据后缀选择解析器（包括 OCR）
        elements = partition(filename=self.file_path)
        content = "\n\n".join([str(el) for el in elements])
        return Document(page_content=content, metadata={"source": self.file_path})