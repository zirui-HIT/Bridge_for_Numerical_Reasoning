import sys
import json

sys.path.append('.')


if __name__ == '__main__':
    from utils import clear_answer

    with open('./dataset/GSM8K/input/test.origin.jsonl', 'r', encoding='utf-8') as f:
        data = [json.loads(x) for x in f]

    result = []
    for i, d in enumerate(data):
        result.append({
            "question": d['question'],
            "thought": d['answer'],
            "answer": float(clear_answer(d['answer'].split("####")[-1].strip())),
            "idx": i
        })

    with open('./dataset/GSM8K/input/test.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
