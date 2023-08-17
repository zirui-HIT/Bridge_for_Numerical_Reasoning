import json


if __name__ == '__main__':
    with open('./dataset/SVAMP/input/test.origin.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    result = []
    for i, d in enumerate(data):
        result.append({
            "question": f"{d['Body'].strip('.')}. {d['Question']}",
            "thought": d['Equation'],
            "answer": d['Answer'],
            "idx": i
        })

    with open('./dataset/SVAMP/input/test.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
