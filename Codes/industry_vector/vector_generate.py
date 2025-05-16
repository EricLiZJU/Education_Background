import os
import json
import pandas as pd
from collections import defaultdict
from tqdm import tqdm  # 实时进度条

def extract_industry_records(json_path, province, city):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = []

    for year, entry_list in data.items():
        mid_count = defaultdict(int)
        mid_to_big = {}

        for item in entry_list:
            for mid, big in item.items():
                mid_count[mid] += 1
                mid_to_big[mid] = big

        for mid, count in mid_count.items():
            records.append({
                "省份": province,
                "城市": city,
                "年份": int(year),
                "中类产业": mid,
                "大类产业": mid_to_big.get(mid, ""),
                "频次": count
            })

    return pd.DataFrame(records)

def build_and_save_city_industry_vectors(json_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    json_files = [f for f in os.listdir(json_folder) if f.endswith(".json") and "-" in f]

    for filename in tqdm(json_files, desc="正在处理城市产业JSON文件"):
        try:
            province, city = filename.replace(".json", "").split("-", maxsplit=1)
            json_path = os.path.join(json_folder, filename)
            df = extract_industry_records(json_path, province, city)

            output_path = os.path.join(output_folder, f"{province}-{city}.csv")
            df.to_csv(output_path, index=False, encoding="utf-8-sig")

        except Exception as e:
            print(f"[跳过] {filename} 错误：{e}")
            continue

# === 用法示例 ===
if __name__ == "__main__":
    input_folder = "../industry_analysis/industry_report"              # 原始 JSON 所在文件夹
    output_folder = "vectors"   # 输出 CSV 文件夹
    build_and_save_city_industry_vectors(input_folder, output_folder)