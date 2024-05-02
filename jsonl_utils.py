import os
import json


def load_jsonl(file_path):
    if not os.path.exists(file_path):
        return []
    data = []
    with open(file_path, mode='r+', encoding='utf-8') as f:
        for line in f.readlines():
            data.append(json.loads(line.strip()))
    return data


def append_to_jsonl(file_path, data):
    with open(file_path, mode='a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=True)
        f.write('\n')

