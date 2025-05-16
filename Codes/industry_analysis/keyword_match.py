import pandas as pd
import re
from sentence_transformers import SentenceTransformer, util
import json
import os

# develop_area_dict = ['园区', '产业园区', '高新技术产业开发区', '经济技术开发区', '经济开发区', '高新园区', '科技园区', '科技产业园区',
#                      '科技创新园区', '新城', '新区', '新兴产业园区', '新兴产业基地', '新兴产业集聚区', '新兴产业集群区', '新兴产业集聚地', '新兴产业集群地',
#                      '云城', '云谷', '云基地', '云集聚区', '云集群区', '云集聚地', '云集群地', '云产业园区', '云产业基地',]
# 识别园区位置（经纬度数据）
# 提及方向（东西南北中）
"""
urban_space_dict = [
    '城市空间', '都市圈', '大都市区', '城市群', '都市核心区', '城市副中心', '城市新区', '城市新城',
    '中央商务区', 'CBD', '科创走廊', '城市走廊', '生态城区', '智慧城区', '创新城区', '未来城区',
    '数字城区', '数字空间', '云城区', '智慧园区', '数字园区', '绿色园区', '生态园区',
    '总部基地', '创新基地', '研发基地', '双创基地', '数字经济基地', '人工智能基地', '物联网基地',
    '创新集聚区', '科技集聚区', '数字集聚区', '研发集聚区', '创意产业园', '文化产业园', '设计园区',
    '创意街区', '科创街区', '产业街区', '城市客厅', '城市会客厅', '复合功能区', '高端服务区',
    '未来科技城', '未来产业城', '未来之城', '智慧之城', '科创新城', '数字新城'
]
"""
# 加载中文兼容的 BERT 模型（推荐）
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


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
    #print(top_big_cats)

    for big_cat in top_big_cats:
        mid_dict = nested_industry_dict[big_cat]

        # Step 2: Top-M 中类筛选
        mid_cat_scores_all = {
            mid_cat: util.cos_sim(text_embedding, model.encode(mid_cat, convert_to_tensor=True)).item()
            for mid_cat in mid_dict.keys()
        }
        top_mid_cats = dict(sorted(mid_cat_scores_all.items(), key=lambda x: x[1], reverse=True)[:top_m_mid])
        #print(f'{big_cat}-{top_mid_cats}')

        for mid_cat in top_mid_cats:
            small_level = mid_dict[mid_cat]

            if isinstance(small_level, list):
                for keyword in [mid_cat] + small_level:
                    score = util.cos_sim(text_embedding, model.encode(keyword, convert_to_tensor=True)).item()
                    #print(f'{big_cat}-{mid_cat}-{keyword}-{score}')
                    if score >= detail_threshold:
                        matches.append((big_cat, mid_cat, keyword, round(score, 4)))

            elif isinstance(small_level, dict):
                for small_cat, keywords in small_level.items():
                    for keyword in [small_cat] + keywords:
                        score = util.cos_sim(text_embedding, model.encode(keyword, convert_to_tensor=True)).item()
                        #print(f'{big_cat}-{small_cat}-{keyword}-{round(score, 4)}')
                        if score >= detail_threshold:
                            matches.append((big_cat, mid_cat, keyword, round(score, 4)))

    return sorted(matches, key=lambda x: x[-1], reverse=True)

with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
    nested_industry_dict = json.load(f)

text = "壮大 数字 内容 影视 动漫 游戏 创意设计 演艺 优势产业"

matches = match_industries_hierarchical(
    text,
    nested_industry_dict,
    top_n_big=3,
    top_m_mid=3,
    detail_threshold=0.2
)

for big, mid, kw, score in matches:
    print(f"{big} → {mid} → {kw}  (score={score})")