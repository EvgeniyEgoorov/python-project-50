import json
from typing import Dict, Optional
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


def process_common_key(tree1, tree2, key):
    if all(
        [
            (isinstance(tree1[key], dict)),
            (isinstance(tree2[key], dict)),
        ]
    ):
        return {"children": create_diff_ast(tree1[key], tree2[key])}
    elif tree1[key] != tree2[key]:
        return {"minus": tree1[key], "plus": tree2[key]}
    else:
        return {"equal": tree1[key]}


def process_tree1_key(tree1, key):
    return {"minus": tree1[key]}


def process_tree2_key(tree2, key):
    return {"plus": tree2[key]}


def create_diff_ast(tree1, tree2):
    result = {}
    for key in sorted(set(tree1) | set(tree2)):
        if all([(key in tree1), (key in tree2)]):
            result[key] = process_common_key(tree1, tree2, key)
        elif key in tree1:
            result[key] = process_tree1_key(tree1, key)
        else:
            result[key] = process_tree2_key(tree2, key)
    return result


from collections import defaultdict


def stylish(diff):
    return diff


def generate_diff(file1, file2):

    tree1 = read_file(file1)
    tree2 = read_file(file2)
    return stylish(create_diff_ast(tree1, tree2))
