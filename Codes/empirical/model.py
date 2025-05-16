import pandas as pd
from linearmodels.panel import PanelOLS
from linearmodels.panel import compare
import statsmodels.api as sm

# === 1. 读取数据 ===
df = pd.read_csv("data/final_data_with_variables.csv")

# === 2. 准备数据结构 ===
# 保证三个主维度为字符串
df["城市"] = df["城市"].astype(str)
df["中类产业"] = df["中类产业"].astype(str)
df["年份"] = df["年份"].astype(int)

# 创建城市-产业联合键（用于实体固定效应）
df["entity"] = df["城市"] + "_" + df["中类产业"]

# 设置多重索引：实体（城市_产业） × 年份
df = df.set_index(["entity", "年份"])

# === 3. 指定因变量和解释变量 ===
df["是否专业匹配"] = df["是否专业匹配"].astype(int)
df["频次"] = df["频次"].astype(float)

# === 4. 回归模型（带城市×产业固定效应 + 年份固定效应）===
mod = PanelOLS.from_formula(
    formula="频次 ~ 是否专业匹配 + EntityEffects + TimeEffects",
    data=df
)

res = mod.fit(cov_type="clustered", cluster_entity=True)

# === 5. 输出结果 ===
print(res.summary)