import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===== Step 1：加载数据 =====
# 读取简化句子
df = pd.read_csv("test_data/cleaned_sentences.csv")
sentences = df.iloc[:, 0].dropna().tolist()

# 读取产业关键词 JSON
with open("utils/industry_keywords.json", "r", encoding="utf-8") as f:
    industry_data = json.load(f)

# ===== Step 2：提取产业叶子关键词 =====
def extract_leaf_keywords(data):
    keywords = set()
    for big_cat, mid_dict in data.items():
        for mid_cat, sub_cat in mid_dict.items():
            if isinstance(sub_cat, dict):
                for small_cat, kw_list in sub_cat.items():
                    if isinstance(kw_list, list):
                        keywords.update(kw_list)
                    elif isinstance(kw_list, str):
                        keywords.add(kw_list)
            elif isinstance(sub_cat, list):
                keywords.update(sub_cat)
            elif isinstance(sub_cat, str):
                keywords.add(sub_cat)
    return sorted(keywords)

industry_keywords = extract_leaf_keywords(industry_data)
keyword_doc = " ".join(industry_keywords)

# ===== Step 3：构建TF-IDF语料库并计算相似度 =====
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([keyword_doc] + sentences)
cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

# ===== Step 4：提取Top-N语义相关句子 =====
top_n = 1000
top_indices = cosine_scores.argsort()[::-1][:top_n]
top_sentences = [{"句子": sentences[i], "相似度": round(cosine_scores[i], 4)} for i in top_indices]

# 输出为变量（非文件）
top_df = pd.DataFrame(top_sentences)
top_df = top_df[top_df['相似度'] > 0]

top_df.to_csv("test_data/filted_sentences.csv", index=False)