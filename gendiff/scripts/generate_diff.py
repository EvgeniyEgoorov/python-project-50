import json
from typing import Dict
import yaml
from yaml.loader import BaseLoader
from pathlib import Path


def read_file(file_path) -> Dict:
    extension = Path(file_path).suffix
    if extension == ".json":
        return json.load(open(file_path))
    elif extension in [".yaml", ".yml"]:
        with open(file_path, 'r') as file:
            return yaml.load(file, Loader=BaseLoader)
    else:
        raise TypeError(f"Unsupported file format: '{extension}'")


def generate_diff(file_path1, file_path2) -> str:

    file_content1 = read_file(file_path1)
    print(file_content1)
    file_content2 = read_file(file_path2)

    union_keys = sorted({**file_content1, **file_content2}.keys())

    result = "{"

    for key in union_keys:
        if key not in file_content2:
            result += f"\n    - {key}: {file_content1[key]}"
        elif key not in file_content1:
            result += f"\n    + {key}: {file_content2[key]}"
        elif file_content1[key] != file_content2[key]:
            result += f"\n    - {key}: {file_content1[key]}"
            result += f"\n    + {key}: {file_content2[key]}"
        else:
            result += f"\n      {key}: {file_content2[key]}"

    result += "\n}"

    return result
