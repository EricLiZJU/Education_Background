import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os

# 加载中文兼容的 BERT 模型（推荐）
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

def get_all_industry_keywords(industry_dict):
    keywords = set()

    for big_cat, mid_dict in industry_dict.items():
        for mid_cat, sub_cat in mid_dict.items():
            if isinstance(sub_cat, dict):  # 三层结构
                for small_cat, kw_list in sub_cat.items():
                    if isinstance(kw_list, list):
                        keywords.update(kw_list)
                    elif isinstance(kw_list, str):
                        keywords.add(kw_list)
            elif isinstance(sub_cat, list):  # 二层结构
                keywords.update(sub_cat)
            elif isinstance(sub_cat, str):  # 少数字符串节点
                keywords.add(sub_cat)

    return sorted(keywords)

def filter_candidate_sentences(sentences, keywords):
    return [s for s in sentences if any(k in s for k in keywords)]

def match_industries_hierarchical(
    text,
    nested_industry_dict,
    top_n_big=3,
    top_m_mid=3,
    detail_threshold=0.6
):
    text_embedding = model.encode(text, convert_to_tensor=True)
    matches = []

    # Step 1: Top-N 大类筛选
    big_cat_scores_all = {
        big_cat: util.cos_sim(text_embedding, model.encode(big_cat, convert_to_tensor=True)).item()
        for big_cat in nested_industry_dict.keys()
    }
    top_big_cats = dict(sorted(big_cat_scores_all.items(), key=lambda x: x[1], reverse=True)[:top_n_big])
    print(top_big_cats)

    for big_cat in top_big_cats:
        mid_dict = nested_industry_dict[big_cat]

        # Step 2: Top-M 中类筛选
        mid_cat_scores_all = {
            mid_cat: util.cos_sim(text_embedding, model.encode(mid_cat, convert_to_tensor=True)).item()
            for mid_cat in mid_dict.keys()
        }
        top_mid_cats = dict(sorted(mid_cat_scores_all.items(), key=lambda x: x[1], reverse=True)[:top_m_mid])
        print(f'{big_cat}-{top_mid_cats}')

        for mid_cat in top_mid_cats:
            small_level = mid_dict[mid_cat]

            if isinstance(small_level, list):
                for keyword in [mid_cat] + small_level:
                    score = util.cos_sim(text_embedding, model.encode(keyword, convert_to_tensor=True)).item()
                    print(f'{big_cat}-{mid_cat}-{keyword}-{score}')
                    if score >= detail_threshold:
                        matches.append((big_cat, mid_cat, keyword, round(score, 4)))

            elif isinstance(small_level, dict):
                for small_cat, keywords in small_level.items():
                    for keyword in [small_cat] + keywords:
                        score = util.cos_sim(text_embedding, model.encode(keyword, convert_to_tensor=True)).item()
                        print(f'{big_cat}-{small_cat}-{keyword}-{round(score, 4)}')
                        if score >= detail_threshold:
                            matches.append((big_cat, mid_cat, keyword, round(score, 4)))

    return sorted(matches, key=lambda x: x[-1], reverse=True)

with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
    nested_industry_dict = json.load(f)

print(nested_industry_dict)

report_content = pd.read_csv('test_data/cleaned_sentences.csv')
print(report_content)

keywords = get_all_industry_keywords(nested_industry_dict)
print(keywords)
filted_sentences = filter_candidate_sentences(report_content, keywords)
print(filted_sentences)
"""
for text in report_content['0']:
    matches = match_industries_hierarchical(
        text,
        nested_industry_dict,
        top_n_big=3,
        top_m_mid=3,
        detail_threshold=0.2
    )

    for big, mid, kw, score in matches:
        print(f"{big} → {mid} → {kw}  (score={score})")"""