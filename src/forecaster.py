import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class CostForecaster:
    """成本预测智能体：执行曲线拟合与未来预测"""
    
    def __init__(self, degree=2):
        self.model = LinearRegression()
        self.poly = PolynomialFeatures(degree=degree)
        
    def fit_and_predict(self, df: pd.DataFrame, target_col: str, periods_to_forecast: int = 4):
        """
        df: 包含'日期'和金额的 DataFrame
        target_col: 需要拟合的列名
        periods_to_forecast: 预测未来的周期数（如未来4个季度）
        """
        # 1. 数据预处理：将日期转为序号（0, 1, 2...）
        df = df.sort_values('日期').reset_index()
        X = np.array(df.index).reshape(-1, 1)
        y = df[target_col].values
        
        # 2. 多项式特征转换 (捕捉非线性趋势)
        X_poly = self.poly.fit_transform(X)
        
        # 3. 训练模型
        self.model.fit(X_poly, y)
        
        # 4. 预测未来
        future_indices = np.arange(len(df), len(df) + periods_to_forecast).reshape(-1, 1)
        future_indices_poly = self.poly.transform(future_indices)
        predictions = self.model.predict(future_indices_poly)
        
        return predictions

    def plot_results(self, df, predictions, target_col):
        """可视化拟合效果"""
        plt.rcParams['font.sans-serif'] = ['SimHei'] # 解决中文显示问题
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df[target_col], 'o-', label='历史成本')
        
        future_x = np.arange(len(df), len(df) + len(predictions))
        plt.plot(future_x, predictions, 'r--', label='预测趋势')
        
        plt.title(f"电网资产成本趋势拟合预测 ({target_col})")
        plt.xlabel("时间周期 (季度)")
        plt.ylabel("金额 (万元)")
        plt.legend()
        plt.grid(True)
        plt.show()

# 测试运行
if __name__ == "__main__":
    # 读取之前生成的模拟数据
    data_path = 'data/maintenance_records.xlsx'
    if os.path.exists(data_path):
        test_df = pd.read_excel(data_path)
        forecaster = CostForecaster(degree=2) # 使用2次多项式拟合曲线
        
        forecast_results = forecaster.fit_and_predict(test_df, '支出金额(万元)')
        print(f"未来四个季度的预测支出为: {forecast_results}")
        
        # 如果在本地有图形界面，可以取消注释查看图表
        # forecaster.plot_results(test_df, forecast_results, '支出金额(万元)')
    else:
        print("请先运行 generate_test_data.py 生成测试数据！")