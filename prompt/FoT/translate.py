from typing import Tuple, Dict, Any
from utils import inference, solve_equations


def process_data(packed_data: Tuple[Dict[str, Any], str, str, int]) -> Dict[str, Any]:
    d, engine, prompt, beam_size = packed_data
    temperature = 0.0 if beam_size == 1 else 0.4

    decomposed = '\n'.join(d['decomposed'])
    sentence = f"{prompt}\n\nParagraph:\n{d['erased']}\nDecomposed:\n{decomposed}\nEquations:\n"
    pred_list = inference(sentence, engine, temperature, beam_size)
    d['equations'] = []
    d['solutions'] = []
    for pred in pred_list:
        try:
            equations = [x.strip() for x in pred.split('\n')]
            solutions = solve_equations(equations)
            d["equations"].append(equations)
            d["solutions"].append(solutions)
        except Exception:
            d["equations"].append([])
            d["solutions"].append({})
    return d
