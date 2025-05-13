import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os
from sentence_transformers import SentenceTransformer, util
import keyword_match_quick

folder_path = f'full_text_data/杭州市'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

data_df = pd.DataFrame()

for file in csv_files:
    file_path = f"{folder_path}/{file}"
    df = pd.read_csv(file_path, encoding="utf-8")
    sentences = df['句子'].to_list()
    industries = []
    for sentence in sentences:
        print(sentence)
        result_dict = keyword_match_quick.quick_match(sentence)
        print(result_dict)
        print("===" * 20)

        industries.append(result_dict)

    print(industries)
