import re
import os
from typing import Dict, List, Optional, Tuple

from .errors import DistriError


def load(path: str) -> Dict[str, Optional[str]]:
    data: Dict[str, Optional[str]] = {}

    for line in read_lines(path):
        key, value = parse_line(line)
        if key:
            data[key] = value

    return data


def read_lines(path: str) -> List[str]:
    if not os.path.exists(path):
        raise DistriError(f'path not found: {path}')

    with open(path, 'r') as f:
        lines = f.readlines()

    return [l.replace('\n', '') for l in lines]


def parse_line(line: str) -> Tuple[str, Optional[str]]:
    p = '^([A-Z_]+)=\"?([a-zA-Z0-9\s\(\)\:\;\-\/\.\,]+)?\"?$'
    s = re.search(p, line)
    if s:
        name = s.group(1).lower()
        value = s.group(2)
        if value is not None:
            value = value.replace('\n', '')

        return (name, value)

    return ('', '')