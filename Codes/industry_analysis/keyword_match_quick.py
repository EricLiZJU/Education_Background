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

def match_to_dict(matches):
    top4 = sorted(matches, key=lambda x: x[-1], reverse=True)[:4]
    result = {mid: big for big, mid, score in top4 if score >= 0.5}
    return result

def match_industries_mid_fast(text, mid_class_embeddings, top_n_big=3, detail_threshold=0):
    text_vec = model.encode(text, convert_to_tensor=True)
    matches = []

    for (big_cat, mid_cat), mid_vec in mid_class_embeddings.items():
        score = util.cos_sim(text_vec, mid_vec).item()
        if score >= detail_threshold:
            matches.append((big_cat, mid_cat, round(score, 4)))

    return sorted(matches, key=lambda x: x[-1], reverse=True)

def quick_match(text):
    with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
        nested_industry_dict = json.load(f)

    mid_embeddings = build_mid_class_embeddings(nested_industry_dict)
    matches = match_industries_mid_fast(text, mid_embeddings, detail_threshold=0)
    """
    for big, mid, score in matches:
        print(f"{big} → {mid}  (score={score})")
    """
    # 示例用法
    result_dict = match_to_dict(matches)
    return result_dict
