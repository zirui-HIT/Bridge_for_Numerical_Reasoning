from utils import inference, clear_answer
from typing import Tuple, Dict, Any


def process_data(packed_data: Tuple[Dict[str, Any], str, str]) -> Dict[str, Any]:
    d, engine, prompt = packed_data
    sentence = f"{prompt}\n\nQuestion:\n{d['question']}\nAnswer:\n"
    pred = inference(sentence, engine)
    try:
        value = pred.split('The answer is')[-1].strip()
        value = clear_answer(value)
        d['pred'] = float(value)
    except Exception:
        d['pred'] = pred
    return d
