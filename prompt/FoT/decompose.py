from utils import inference
from typing import Tuple, Dict, Any


def process_data(packed_data: Tuple[Dict[str, Any], str, str, int]) -> Dict[str, Any]:
    d, engine, prompt, beam_size = packed_data
    sentence = f"{prompt}\n\nParagraph:\n{d['erased']}\nDecomposed:\n"
    pred = inference(sentence, engine)[0].strip()
    d['decomposed'] = pred.split('\n')
    return d
