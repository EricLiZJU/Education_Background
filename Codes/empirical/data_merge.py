import os
import pandas as pd

# ========== 1. 读取官员数据 ==========
edu_df = pd.read_excel("../../Source_Data/education/major_classified_data.xlsx")
edu_df["城市"] = edu_df["citychn"].astype(str).str.strip()
edu_df["年份"] = edu_df["year"].astype(int)

# 按 城市+年份 分组，聚合为列表形式
grouped_edu = edu_df.groupby(["城市", "年份"]).agg({
    "leadername": lambda x: list(x.dropna().unique()),
    "cleaned_major_names": lambda x: list(x.dropna().unique()),
    "major_category": lambda x: list(x.dropna().unique())
}).reset_index()

# ========== 2. 处理每个产业 CSV 文件 ==========
def extract_from_csv(csv_path, province, city):
    df = pd.read_csv(csv_path)
    df["省份"] = province
    df["城市"] = city
    df["年份"] = df["年份"].astype(int)
    return df[["省份", "城市", "年份", "中类产业", "大类产业", "频次"]]

# ========== 3. 批量读取所有城市的 CSV ==========
def build_full_vector(csv_folder):
    all_data = []
    for filename in os.listdir(csv_folder):
        print(filename)
        if filename.endswith(".csv") and "-" in filename:
            try:
                province, city = filename.replace(".csv", "").split("-", maxsplit=1)
                path = os.path.join(csv_folder, filename)
                df = extract_from_csv(path, province, city)
                all_data.append(df)
            except Exception as e:
                print(f"[跳过] {filename} 出错：{e}")
    return pd.concat(all_data, ignore_index=True)

csv_folder = "../industry_vector/vectors"
vector_df = build_full_vector(csv_folder)

# ========== 4. 合并领导信息 ==========
merged_df = pd.merge(vector_df, grouped_edu, how="left", on=["城市", "年份"])

# ========== 5. 输出 ==========
merged_df = merged_df[[
    "省份", "城市", "年份",
    "中类产业", "大类产业", "频次",
    "leadername", "cleaned_major_names", "major_category"
]]

merged_df.to_csv("merged_data.csv", index=False, encoding="utf-8-sig")
print("✅ 已输出：merged_data.csv")