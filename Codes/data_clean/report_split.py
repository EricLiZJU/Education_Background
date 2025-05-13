import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

china_provinces = [
    "北京市", "天津市", "上海市", "重庆市",  # 直辖市
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",  # 华北/东北
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",  # 华东
    "河南省", "湖北省", "湖南省",  # 华中
    "广东省", "海南省",  # 华南
    "四川省", "贵州省", "云南省",  # 西南
    "陕西省", "甘肃省", "青海省",  # 西北
    "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区"  # 自治区
]

for province in china_provinces:
    os.makedirs(f"../../Source_Data/report/filted_sentences/{province}", exist_ok=True)

print("所有省级行政区文件夹已创建。")
"""
for province in china_provinces:
    file_path = f'../../Source_Data/report/split/{province}.xlsx'
    try:
        df = pd.read_excel(file_path)
        cities = df['地区'].unique()
        print(cities)
        for city in cities:
            print(f"正在分析{province}-{city}")
            city_df = df[df['地区'] == city]
            for index, row in city_df.iterrows():
                full_text = row['报告全文']
                year = row['年份']
                with open(f'../../Source_Data/report/individual_report_text/{province}/{city}/{year}.csv', "w", encoding="utf-8") as f:
                    f.write(full_text)
    except:
        continue


"""

