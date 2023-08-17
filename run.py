import os
import sys
import json
import random
import argparse

from importlib import import_module
from typing import List, Dict, Any, Tuple
from tqdm.contrib.concurrent import process_map
from concurrent.futures import ProcessPoolExecutor

sys.path.append('.')
sys.path.append('./prompt/FoT_decompose')


if __name__ == '__main__':
    from utils import ENGINE_MAP

    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str)
    parser.add_argument('--parallel', action='store_true')
    parser.add_argument('--module_path', type=str)
    parser.add_argument('--prompt_path', type=str)
    parser.add_argument('--input_path', type=str)
    parser.add_argument('--output_path', type=str)
    parser.add_argument('--random_seed', type=int, default=42)
    parser.add_argument('--data_size', type=int, default=None)
    parser.add_argument('--beam_size', type=int, default=1)
    parser.add_argument('--prompt_examples', type=int, default=None)
    args = parser.parse_args()
    random.seed(args.random_seed)

    prompt_module = import_module(args.module_path)
    with open(args.prompt_path, 'r', encoding='utf-8') as f:
        prompt = '\n'.join([line.strip() for line in f.readlines()])
    if not (args.prompt_examples is None):
        prompt_examples = prompt.split('\n\n')
        examples = min(len(prompt_examples) - 1, args.prompt_examples)
        prompt = '\n\n'.join([prompt_examples[0]] +
                             random.sample(prompt_examples[1:], examples))

    with open(args.input_path, 'r', encoding='utf-8') as f:
        data: List[Dict[str, Any]] = json.load(f)
    if args.data_size:
        data = random.sample(data, args.data_size)
    packed_data: List[Tuple[Dict[str, Any], str]] = [
        (d, ENGINE_MAP[args.engine], prompt, args.beam_size) for d in data]

    if args.parallel:
        with ProcessPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
            result: List[Dict[str, Any]] = list(process_map(
                prompt_module.process_data, packed_data, max_workers=os.cpu_count(), chunksize=1))
    else:
        result: List[Dict[str, Any]] = [
            prompt_module.process_data(x) for x in packed_data]

    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    with open(args.output_path, "w", encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
