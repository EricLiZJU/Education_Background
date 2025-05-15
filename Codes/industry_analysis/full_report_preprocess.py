import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import report_preprocess

china_provinces = [
    # "北京市", "天津市", "上海市", "重庆市",  # 直辖市
    "河北省", "山西省", "辽宁省", "吉林省", "黑龙江省",  # 华北/东北
    "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省",  # 华东
    "河南省", "湖北省", "湖南省",  # 华中
    "广东省", "海南省",  # 华南
    "四川省", "贵州省", "云南省",  # 西南
    "陕西省", "甘肃省", "青海省",  # 西北
    "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区"  # 自治区
]
"""
for province in china_provinces:
    file_path = f'../../Source_Data/report/split/{province}.xlsx'

    df = pd.read_excel(file_path)
    cities = df['地区'].unique()
    print(cities)
    for city in cities:
        print(f"正在分析{province}-{city}")
        folder_path = f'../../Source_Data/report/individual_report_text/{province}/{city}'
        os.makedirs(f'../../Source_Data/report/cleaned_sentences/{province}/{city}', exist_ok=True)
        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in csv_files:
            path = f'{folder_path}/{file}'
            print(path)
            report_preprocess.preprocess(path, f"../../Source_Data/report/cleaned_sentences/{province}/{city}/{file}")
"""
for province in tqdm(china_provinces, desc="处理省份"):
    file_path = f'../../Source_Data/report/split/{province}.xlsx'
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"读取失败：{province} — {e}")
        continue

    cities = df['地区'].dropna().unique()

    for city in tqdm(cities, desc=f"{province}", leave=False):
        city = str(city).strip().replace("/", "_").replace("\\", "_")
        folder_path = f'../../Source_Data/report/individual_report_text/{province}/{city}'
        output_path = f'../../Source_Data/report/cleaned_sentences/{province}/{city}'
        os.makedirs(output_path, exist_ok=True)

        if not os.path.exists(folder_path):
            print(f"[警告] 缺少目录：{folder_path}")
            continue

        csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
        for file in tqdm(csv_files, desc=f"{city}", leave=False):
            input_file = os.path.join(folder_path, file)
            output_file = os.path.join(output_path, file)
            try:
                report_preprocess.preprocess(input_file, output_file)
            except Exception as e:
                print(f"处理失败：{province}-{city}-{file}：{e}")