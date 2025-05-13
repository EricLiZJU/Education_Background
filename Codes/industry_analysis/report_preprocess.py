import jieba.posseg as pseg
import re
import pandas as pd

def extract_short_content_sentences(text, min_len=3, max_len=20):
    # content_flags = {"n", "v", "a", "vn", "an", "ns", "nt", "nz", "nr", "eng"}
    content_flags = {"n"}
    sentences = []

    # 按中文标点切分为子句（防止长句）
    raw_clauses = re.split(r'[，；。！？\n]', text)
    for clause in raw_clauses:
        clause = clause.strip()
        if not clause:
            continue

        # 提取实词
        words = pseg.cut(clause)
        content_words = [w for w, f in words if f in content_flags]

        if min_len <= len(content_words) <= max_len:
            sentences.append(" ".join(content_words))

    return sentences

def preprocess(source_path, final_path):
    with open(source_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    cleaned_sentences = extract_short_content_sentences(raw_text)
    df = pd.DataFrame(cleaned_sentences)
    df.to_csv(final_path, index=False)
