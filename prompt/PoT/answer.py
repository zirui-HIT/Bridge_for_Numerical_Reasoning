from utils import inference
from prompt.PoT.utils import floatify_ans, safe_execute
from typing import Tuple, Dict, Any


def process_data(packed_data: Tuple[Dict[str, Any], str, str]) -> Dict[str, Any]:
    d, engine, prompt, beam_size = packed_data
    sentence = f"{prompt}\n\nQuestion: {d['question']}\n# Python code, return ans\n"
    pred = inference(sentence, engine)[0].strip()
    ans = safe_execute(pred)
    ans = floatify_ans(ans)

    d['program'] = pred.split('\n')
    d['pred'] = ans
    return d
