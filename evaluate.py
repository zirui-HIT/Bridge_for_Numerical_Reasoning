import sys
import json
import argparse

from tqdm import tqdm
from sympy import sympify
from typing import List, Dict, Any

sys.path.append('.')


if __name__ == '__main__':
    from utils import clear_answer, answer_equal

    parser = argparse.ArgumentParser()
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    args = parser.parse_args()

    with open(args.input_path, 'r', encoding='utf-8') as f:
        data: List[Dict[str, Any]] = json.load(f)

    count = 0
    for d in tqdm(data):
        prediction: float = d['pred']
        gt_ans: float = d['answer']
        if answer_equal(prediction, gt_ans):
            count += 1
            d['match'] = True
        else:
            d['match'] = False

        d['question'] = d['question'].split('. ')
        if 'thought' in d:
            d['thought'] = d['thought'].split('\n')
        d['error_type'] = ""

    print(f"em: {count / len(data)}")
    data = [d for d in data if not d['match']]
    with open(args.output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
