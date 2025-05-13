import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os
from sentence_transformers import SentenceTransformer, util

# 模型初始化
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def build_mid_class_embeddings(nested_industry_dict):
    mid_class_embeddings = {}
    for big_cat, mid_dict in nested_industry_dict.items():
        for mid_cat in mid_dict.keys():
            mid_class_embeddings[(big_cat, mid_cat)] = model.encode(mid_cat, convert_to_tensor=True)
    return mid_class_embeddings

def match_industries_hierarchical(
    text,
    nested_industry_dict,
    top_n_big=3,
    detail_threshold=0.6
):
    text_embedding = model.encode(text, convert_to_tensor=True)
    matches = []

    # Step 1: 大类初筛
    big_cat_scores_all = {
        big_cat: util.cos_sim(text_embedding, model.encode(big_cat, convert_to_tensor=True)).item()
        for big_cat in nested_industry_dict.keys()
    }
    top_big_cats = dict(sorted(big_cat_scores_all.items(), key=lambda x: x[1], reverse=True)[:top_n_big])

    # Step 2: 在大类中匹配中类
    for big_cat in top_big_cats:
        mid_dict = nested_industry_dict[big_cat]
        for mid_cat in mid_dict.keys():
            score = util.cos_sim(text_embedding, model.encode(mid_cat, convert_to_tensor=True)).item()
            if score >= detail_threshold:
                matches.append((big_cat, mid_cat, round(score, 4)))

    return sorted(matches, key=lambda x: x[-1], reverse=True)


with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
    nested_industry_dict = json.load(f)

text = "蔬菜 产量 生猪 水产品 产量"

matches = match_industries_hierarchical(
    text,
    nested_industry_dict,
    top_n_big=3,
    detail_threshold=0.2
)

for big, mid, score in matches:
    print(f"{big} → {mid}  (score={score})")