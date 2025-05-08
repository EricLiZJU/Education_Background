import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'utils/class_major_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    categories = json.load(f)

file_path = 'initial_classfied_data.xlsx'
df = pd.read_excel(file_path)
df = df

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
category_embeddings = {
    cat: model.encode(" ".join(keywords), convert_to_tensor=True)
    for cat, keywords in categories.items()
}
sim_records = []
def classify_major(major):
    if not major or pd.isna(major):
        return "其他"
    # 确保输入是字符串
    major = str(major)
    # 编码当前专业向量
    major_vec = model.encode(major, convert_to_tensor=True)
    print(f"当前分类专业：{major}，向量维度：{major_vec.shape}")
    # 对每个门类计算余弦相似度（返回的是 1x1 Tensor，因此 .item() 可行）
    sims = {
        cat: util.cos_sim(major_vec, emb).item()
        for cat, emb in category_embeddings.items()
    }

    best_cat = max(sims, key=sims.get)
    classified = best_cat if sims[best_cat] >= 0.2 else "其他"
    print(sims)
    # 存储一行结果
    sim_row = {"original_major": f"{major}"}
    sim_row.update(sims)
    sim_row["classified"] = classified
    sim_records.append(sim_row)
    return best_cat if sims[best_cat] >= 0.2 else "其他"
df['major_category'] = df['cleaned_major_names'].apply(classify_major)
sim_df = pd.DataFrame(sim_records)
print(df['major_category'].value_counts())
df.to_excel("major_classified_data.xlsx", index=False)
sim_df.to_excel("major_sim_value.xlsx", index=False)

