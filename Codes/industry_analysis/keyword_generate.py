import json


def build_nested_industry_keywords(data):
    nested_keywords = {}

    for section_code, section_info in data.items():
        section_name = section_info.get("name", "")
        nested_keywords[section_name] = {}

        for major_code, major_info in section_info.get("categories", {}).items():
            major_name = major_info.get("name", "")
            nested_keywords[section_name][major_name] = {}

            for mid_code, mid_info in major_info.get("categories", {}).items():
                if isinstance(mid_info, dict):
                    mid_name = mid_info.get("name", "")
                    leaf_names = []

                    for leaf_code, leaf_value in mid_info.get("categories", {}).items():
                        if isinstance(leaf_value, str):
                            leaf_names.append(leaf_value)
                        elif isinstance(leaf_value, dict):
                            leaf_names.append(leaf_value.get("name", ""))

                    nested_keywords[section_name][major_name][mid_name] = leaf_names
                elif isinstance(mid_info, str):
                    # 若直接是字符串，则中类本身就是关键词
                    nested_keywords[section_name][major_name][mid_info] = []

    return nested_keywords

# 加载你的 industry.json 文件
with open("utils/industry.json", "r", encoding="utf-8") as f:
    industry_data = json.load(f)

# 构建嵌套结构
nested_industry = build_nested_industry_keywords(industry_data)

with open("utils/industry_keywords.json", "w", encoding="utf-8") as f:
    json.dump(nested_industry, f, ensure_ascii=False, indent=2)