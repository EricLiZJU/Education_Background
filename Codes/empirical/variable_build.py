import pandas as pd
import json

# === 1. 读取数据 ===
df = pd.read_csv("data/merged_data.csv")

# === 3. 加载 mapping.json 文件（专业门类 ↔ 中类产业） ===
with open("utils/mapping.json", "r", encoding="utf-8") as f:
    mapping = json.load(f)

# === 4. 构造“是否专业匹配”变量 ===
def check_profession_match(row):
    try:
        majors = row["major_category"]
        industry = row["中类产业"]

        if pd.isna(majors) or pd.isna(industry):
            return 0

        if isinstance(majors, str):
            majors = eval(majors)
        if not isinstance(majors, list):
            return 0

        for m in majors:
            if m in mapping:
                for mapped_ind in mapping[m]:
                    if mapped_ind in industry:
                        return 1
        return 0
    except Exception as e:
        print(f"匹配出错：{e}")
        return 0

df["是否专业匹配"] = df.apply(check_profession_match, axis=1)

# === 5. 保存结果 ===
df.to_csv("final_data_with_variables.csv", index=False, encoding="utf-8-sig")
print("✅ 已生成带变量的数据，保存为 final_data_with_variables.csv")