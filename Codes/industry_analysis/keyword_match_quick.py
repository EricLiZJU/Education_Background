import os
import json
import re
from sentence_transformers import SentenceTransformer, util
import torch
from tqdm import tqdm
import pandas as pd

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print(f"Using device: {device}")

# 初始化模型
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2", device=device)

# 加载关键词字典
with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
    nested_industry_dict = json.load(f)

# 构建中类嵌入向量
def build_mid_class_embeddings(nested_industry_dict):
    mid_class_embeddings = {}
    for big_cat, mid_dict in nested_industry_dict.items():
        for mid_cat in mid_dict.keys():
            mid_class_embeddings[(big_cat, mid_cat)] = model.encode(mid_cat, convert_to_tensor=True)
    return mid_class_embeddings

# 匹配前4个得分 >= 0.5 的分类
def match_to_dict(matches):
    top4 = sorted(matches, key=lambda x: x[-1], reverse=True)[:4]
    result = {mid: big for big, mid, score in top4 if score >= 0.5}
    return result

# 匹配文本到产业
def match_industries_mid_fast(text, mid_class_embeddings, detail_threshold=0):
    text_vec = model.encode(text, convert_to_tensor=True).to(device)
    matches = []
    for (big_cat, mid_cat), mid_vec in mid_class_embeddings.items():
        score = util.cos_sim(text_vec, mid_vec).item()
        if score >= detail_threshold:
            matches.append((big_cat, mid_cat, round(score, 4)))
    return sorted(matches, key=lambda x: x[-1], reverse=True)

# 快速匹配入口
def quick_match(text, mid_class_embeddings):
    matches = match_industries_mid_fast(text, mid_class_embeddings)
    return match_to_dict(matches)

# 主处理函数：读取文件 → 匹配 → 保存结果
def process_sentences_top4_only(input_root, output_folder, text_column="text"):
    os.makedirs(output_folder, exist_ok=True)
    mid_embeddings = build_mid_class_embeddings(nested_industry_dict)
    city_results = {}
    last_province = None

    for root, dirs, files in os.walk(input_root):
        csv_files = [f for f in files if f.endswith(".csv")]
        if not csv_files:
            continue

        path_parts = root.split(os.sep)
        if len(path_parts) < 2:
            continue
        province = path_parts[-2]
        city = path_parts[-1]

        if province != last_province:
            tqdm.write(f"\n🗂️ 正在处理省份：{province}")
            last_province = province

        tqdm.write(f"📍 处理城市：{province} - {city}")

        for csv_file in tqdm(csv_files, desc=f"{city}", leave=False):
            year_match = re.match(r"(\d{4})\.csv", csv_file)
            if not year_match:
                continue
            year = year_match.group(1)
            csv_path = os.path.join(root, csv_file)

            try:
                df = pd.read_csv(csv_path)
            except Exception as e:
                tqdm.write(f"❌ 读取失败: {csv_path} - {e}")
                continue

            city_key = f"{province}-{city}"
            if city_key not in city_results:
                city_results[city_key] = {}
            if year not in city_results[city_key]:
                city_results[city_key][year] = []

            for sentence in df[text_column].dropna().astype(str).tolist():
                matches = match_industries_mid_fast(sentence, mid_embeddings, detail_threshold=0)
                top4 = sorted(matches, key=lambda x: x[-1], reverse=True)[:4]
                result = {mid: big for big, mid, score in top4 if score >= 0.5}
                if result:
                    city_results[city_key][year].append(result)

    for city_key, year_data in city_results.items():
        output_path = os.path.join(output_folder, f"{city_key}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(year_data, f, ensure_ascii=False, indent=2)

# 使用示例
process_sentences_top4_only(
    input_root="../../Source_Data/report/filted_sentences",
    output_folder="industry_report",
    text_column="句子"  # 如果列名不是 "text"，请替换
)