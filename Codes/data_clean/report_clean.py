import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils.province_city import city2province

folder_path = '../../Source_Data/report/split'


df = pd.read_csv('/Users/lihongyang/Desktop/SOPSourceData/工作报告汇总（2024.5更新）/工作报告面板数据-地级市.csv')
for index, row in df.iterrows():
    city = row['地区']
    province = city2province(city)
    df.at[index, '省份'] = province

province_list = set(df['省份'].tolist())
for province in province_list:
    split_df = df[df['省份'] == province]
    split_df.to_excel(f'{folder_path}/{province}.xlsx')