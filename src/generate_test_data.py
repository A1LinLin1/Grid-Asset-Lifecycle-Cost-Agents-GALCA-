import pandas as pd
import os

# 确保 data 目录存在
os.makedirs('data', exist_ok=True)

def create_test_files():
    # 1. 生成 Excel: 变电站过去 5 年的运维工单数据
    df = pd.DataFrame({
        '日期': pd.date_range(start='2020-01-01', periods=20, freq='QE'),
        '资产名称': ['变压器-T1'] * 20,
        '维护类型': ['定期检查', '零件更换', '油质检测', '故障维修'] * 5,
        '支出金额(万元)': [12.5, 15.2, 14.8, 20.1, 13.0, 16.5, 15.9, 22.0, 
                        14.2, 18.1, 17.5, 25.4, 16.8, 20.2, 19.5, 28.1,
                        18.5, 22.4, 21.0, 32.0]
    })
    df.to_excel('data/maintenance_records.xlsx', index=False)
    print("✅ 已生成: data/maintenance_records.xlsx")

    # 2. 生成 模拟合同文本 (txt 模拟 pdf 提取后的效果)
    contract_text = """
    项目名称：2024年度电网设备资产更新协议
    合同编号：SG-2024-088
    甲方：国家电网XX分公司
    乙方：XX电力设备制造厂
    关键条款：
    1. 采购设备：特高压换流阀
    2. 合同总价：人民币 1,250,000.00 元
    3. 支付方式：首付 30%，验收后支付 60%，质保期满支付 10%
    4. 签署日期：2024年3月15日
    """
    with open('data/sample_contract.txt', 'w', encoding='utf-8') as f:
        f.write(contract_text)
    print("✅ 已生成: data/sample_contract.txt")

if __name__ == "__main__":
    create_test_files()