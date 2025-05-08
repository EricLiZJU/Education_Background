import pandas as pd
import json
import os
current_dir = os.path.dirname(__file__)
json_path = os.path.join(current_dir, 'province_city_data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

def city2province(city):
    for key, value in data.items():
        if city in value:
            return key
        else:
            continue

