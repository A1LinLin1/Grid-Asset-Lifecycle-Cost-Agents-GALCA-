from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('data', exist_ok=True)

# 创建一张白底图片
img = Image.new('RGB', (600, 400), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# 写入模拟的工单文本
text = """
国家电网 - 现场维修工单 (扫描件)
--------------------------------
工单号: REP-2024-992
日期: 2024-05-12
维修设备: 10kV 开关柜
故障描述: 绝缘老化导致放电
维修费用 (人工+材料): 45000.00 元
负责人: 张工
"""
# 简单绘制文本（不使用特殊字体以防报错）
d.text((20, 20), text, fill=(0, 0, 0))

img.save('data/sample_receipt.jpg')
print("✅ 已生成模拟工单图片: data/sample_receipt.jpg")
