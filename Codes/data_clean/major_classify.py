import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'class_major_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    categories = json.load(f)

file_path = '../../Source_Data/education/data.xlsx'
df = pd.read_excel(file_path)

def clean_major(text):
    if pd.isnull(text):
        return ""
    text = re.sub(r'[专业系学部所院]', '', text)  # 去除常见修饰词
    text = re.sub(r'\s+', '', text)  # 去除空格
    return text.strip().lower()

def classify_major(major):
    if major == "":
        return "其他"
    major_vec = model.encode(major, convert_to_tensor=True)
    sims = {cat: float(util.cos_sim(major_vec, emb)) for cat, emb in category_embeddings.items()}
    best_cat = max(sims, key=sims.get)
    return best_cat if sims[best_cat] >= 0.5 else "其他"


df['cleaned_major_names'] = df['major_names'].apply(clean_major)

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
category_embeddings = {cat: model.encode(desc, convert_to_tensor=True) for cat, desc in categories.items()}
