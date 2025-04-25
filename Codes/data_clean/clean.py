import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('/Users/lihongyang/Desktop/SOPSourceData/工作报告汇总（2024.5更新）/工作报告面板数据-地级市.csv')
print(df.head())
print(df.describe())
print(df.info())
print(df.columns)

new_df = df.head(200)
new_df.to_excel('example_data.xlsx', index=False)