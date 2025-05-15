import json
from collections import defaultdict
import pandas as pd

def build_industry_vector_from_simple_json(json_path, city="未知城市", province="未知省"):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []

    for year, industry_blocks in data.items():
        mid_count = defaultdict(int)
        big_count = defaultdict(int)

        for block in industry_blocks:
            for mid, big in block.items():
                mid_count[mid] += 1
                big_count[big] += 1

        result.append({
            "省份": province,
            "城市": city,
            "年份": int(year),
            "中类产业频次": dict(mid_count),
            "大类产业频次": dict(big_count)
        })

    return pd.DataFrame(result)

df = build_industry_vector_from_simple_json("浙江省-杭州市.json", city="杭州市", province="浙江省")
print(df)
df.to_csv("industry_vector.csv", index=False)