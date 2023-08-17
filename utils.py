import re
import time
import openai

from math import isclose
from typing import List, Dict, Any, Union
from sympy import symbols, Eq, solve, S, simplify


API_VERSION = {
    "code-davinci-002": "2022-12-01",
    "35turbo": "2023-03-15-preview"
}
ENGINE_MAP = {
    "codex": "code-davinci-002",
    "gpt3.5": "35turbo"
}
ERROR_TYPES = {
    "continue_error": [
        "timed out",
        "Connection reset by peer",
        "Remote end closed connection without response",
        "occurred in violation of protocol",
        "Failed to resolve",
        "TLSV1_ALERT_INTERNAL_ERROR",
        "Error communicating"
    ],
    "sleep_error": [
        "call rate limit",
        "token rate limit"
    ],
    "ignore_error": [
        "content"
    ]
}

openai.api_type = "azure"
openai.api_base = "your_api_base"
openai.api_key = "your_api_key"


def inference(sentence: str, engine: str = "35turbo", temperature: float = 0.0, beam_size: int = 1) -> List[str]:
    openai.api_version = API_VERSION[engine]
    params = {
        "temperature": temperature,
        "max_tokens": 256,
        "top_p": 1,
        "n": beam_size,
        "request_timeout": 15
    }
    while True:
        try:
            if 'turbo' in engine:
                completion = openai.ChatCompletion.create(
                    engine=engine,
                    messages=[{"role": "user", "content": sentence}],
                    **params)
                return [x['message']['content'] for x in completion['choices']]
            elif 'code' in engine:
                response = openai.Completion.create(
                    engine=engine,
                    prompt=sentence,
                    stop=['\n\n'],
                    **params)
                return [x['text'] for x in response['choices']]
        except Exception as e:
            continue_flag = False
            sleep_flag = False
            ignore_flag = False
            for x in ERROR_TYPES['continue_error']:
                if x in str(e):
                    continue_flag = True
            for x in ERROR_TYPES['sleep_error']:
                if x in str(e):
                    sleep_flag = True
                    continue_flag = True
            for x in ERROR_TYPES['ignore_error']:
                if x in str(e):
                    ignore_flag = True
            if sleep_flag:
                time.sleep(5)
            if continue_flag:
                continue
            if not ignore_flag:
                print(e)
            return [""]


def clear_answer(answer: str) -> str:
    # get answer
    answer = answer.split('Answer: ')[-1]
    answer = answer.split()[0]

    # check negative
    negative_flag = False
    if answer.startswith('-'):
        negative_flag = True
        answer = answer[1:]

    # clear unused symbols
    for symbol in [' ', '\n', '$', '.', '%', 'km', 'm', 'cm', '°', 'pi', 'Rs', 'Rs.']:
        answer = answer.strip(symbol)
    answer = answer.strip()

    # clear comma
    answer = answer.replace(',', '')

    # calculate
    answer = simplify(S(answer))

    if negative_flag:
        answer = f"-{answer}"
    return answer


def solve_equations(equations: List[str]) -> Dict[str, float]:
    variables = set()
    for equation in equations:
        variables.update(re.findall(r'[a-zA-Z_][a-zA-Z_0-9]*', equation))

    sym_variables = symbols(' '.join(variables))

    sympy_equations = []
    for equation in equations:
        items = equation.split('=')
        left, right = items[0], items[1]
        sympy_equations.append(Eq(eval(left, {str(var): var for var in sym_variables}), eval(
            right, {str(var): var for var in sym_variables})))

    solutions = solve(sympy_equations)
    if isinstance(solutions, list):
        solutions = solutions[0]
    solutions = {str(var): float(value) for var, value in solutions.items()}

    return solutions


def answer_equal(prediction: Union[bool, float, str],
                 reference: Union[float, str],
                 include_percentage: bool = False,
                 is_close: float = False) -> bool:
    def get_precision(gt_ans: float) -> int:
        precision = 5
        if '.' in str(gt_ans):
            precision = len(str(gt_ans).split('.')[-1])
        return precision

    if prediction is None:
        return False
    elif type(prediction) == bool:
        # bool questions
        if prediction:
            return reference == 'yes'
        else:
            return reference == 'no'
    elif type(reference) == str or type(prediction) == str:
        # string questions
        return prediction == reference
    else:
        # number questions
        if include_percentage:
            gt_result = [reference / 100, reference, reference * 100]
        else:
            gt_result = [reference]
        for item in gt_result:
            try:
                if is_close:
                    if isclose(item, prediction, rel_tol=0.001):
                        return True
                precision = min(get_precision(prediction), get_precision(item))
                if round(prediction, precision) == round(item, precision):
                    return True
            except Exception:
                continue
        return False
