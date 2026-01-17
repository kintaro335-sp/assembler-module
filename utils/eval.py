from typing import Literal

def eval_value(value) -> Literal['NAME', 'NUMBER']:
  try:
    a = int(value)
    return 'NUMBER'
  except ValueError:
    return 'NAME'
