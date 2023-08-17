from collections import Counter
from typing import Tuple, Dict, Any, List
from utils import inference, solve_equations


def constrain(equations_list: List[List[str]]) -> List[str]:
    counter = Counter()
    counter_with_index = dict()

    for i, x in enumerate(equations_list):
        equations = x
        try:
            solutions = solve_equations(equations)
            solution_str = str(solutions['ans'])
            counter.update([solution_str])
            if solution_str not in counter_with_index:
                counter_with_index[solution_str] = i
        except Exception:
            continue

    if not counter:
        return equations_list[0]
    max_count_solution_str = counter.most_common(1)[0][0]
    return equations_list[counter_with_index[max_count_solution_str]]


def process_data(packed_data: Tuple[Dict[str, Any], str, str, int]) -> Dict[str, Any]:
    try_times = 5
    d, engine, prompt, beam_size = packed_data
    init_temperature = 0 if beam_size == 1 else 0.8

    for i, (e, s) in enumerate(zip(d['equations'][:beam_size], d['solutions'][:beam_size])):
        for j in range(try_times):
            equations_temp = []
            if e:
                equations = '\n'.join(e)
                sentence = f"{prompt}\n\nQuestion:\n{d['question']}\nEquations:\n{equations}\n"
                pred_list = inference(sentence, engine, init_temperature)
                equations_temp = e + pred_list[0].split('\n')
            else:
                sentence = f"{prompt}\n\nQuestion:\n{d['question']}\nEquations:\n"
                pred_list = inference(
                    sentence, engine, init_temperature + j * 0.1)
                equations_temp = pred_list[0].split('\n')
            try:
                d['solutions'][i] = solve_equations(equations_temp)
            except Exception:
                d['solutions'][i] = {}
            if len(d['solutions'][i]) > 0:
                d['equations'][i] = equations_temp
                break
    d['pred_equation'] = constrain(d['equations'])
    try:
        d['pred_solution'] = solve_equations(d['pred_equation'])
        d['pred'] = d['pred_solution']['ans']
    except Exception as e:
        d['pred_solution'] = {}
        d['pred'] = 2
    return d
