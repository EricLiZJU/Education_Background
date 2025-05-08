import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'utils/class_major_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    categories = json.load(f)

file_path = '../../Source_Data/education/data.xlsx'
df = pd.read_excel(file_path)

def clean_major(text):
    if pd.isna(text):
        return ""
    text = str(text).strip()
    # 正则：仅删除末尾的“专业”、“系”、“班”
    text = re.sub(r'(专业|系|班)$', '', text)
    if "系" in text:
        # 如果有“系”，只取“系”字后的部分
        text = text.split("系", 1)[-1]
    # 再统一去除末尾和开头的空格
    text = text.strip().lower()
    return text



df['cleaned_major_names'] = df['major_names'].apply(clean_major)
print(df)
df.to_excel('initial_classfied_data.xlsx', index=False)