import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

folder_path = '../../Source_Data/education/split'
import os

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
dfs = []

for csv_file in csv_files:
    source_df = pd.read_csv(f'{folder_path}/{csv_file}')
    split_df = source_df[['year', 'provchn', 'citychn', 'leadername', 'school_names', 'major_names']]
    dfs.append(split_df)

df = dfs[0]
for i in range(1, len(dfs)):
    df = pd.concat([df, dfs[i]], ignore_index=True)

df.to_excel('../../Source_Data/education/data_without_drop.xlsx')

clean_df = df[df['major_names'] != 'missing'].reset_index(drop=True)
print(clean_df)
clean_df.to_excel('../../Source_Data/education/data.xlsx')

