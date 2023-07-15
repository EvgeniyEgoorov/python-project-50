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


def process_common_key(tree1, tree2, key):
    if all(
        [
            (isinstance(tree1[key], dict)),
            (isinstance(tree2[key], dict)),
        ]
    ):
        return {"children": create_diff_ast(tree1[key], tree2[key])}
    elif tree1[key] != tree2[key]:
        return {"changed": {"removed": tree1[key], "added": tree2[key]}}
    else:
        return {"unchanged": tree1[key]}


def create_diff_ast(tree1, tree2):
    result = {}
    for key in sorted(set(tree1) | set(tree2)):
        if all([(key in tree1), (key in tree2)]):
            result[key] = process_common_key(tree1, tree2, key)
        elif key in tree1:
            result[key] = {"removed": tree1[key]}
        else:
            result[key] = {"added": tree2[key]}
    return result


def prettify_output(output):
    output = json.dumps(output, indent=4)
    patterns = {
        '"': '',
        ',': '',
        '  + ': '+ ',
        '  - ': '- '
    }
    for old, new in patterns.items():
        output = output.replace(old, new)
    return output


def format_diff(diff):
    result = {}
    sub_formatters_list = {
        "changed": lambda k, v: {
            f"- {k}": v["removed"],
            f"+ {k}": v["added"]
        },
        "added": lambda k, v: {f"+ {k}": v},
        "removed": lambda k, v: {f"- {k}": v},
        "children": lambda k, v: {k: format_diff(v)},
        "unchanged": lambda k, v: {k: v}
    }
    for key, value in diff.items():
        sub_key, sub_value = list(value.items())[0]
        sub_formatter = sub_formatters_list[sub_key]
        result.update(sub_formatter(key, sub_value))
    return result


def format_stylish(diff):
    print(diff)
    return prettify_output(format_diff(diff))


def generate_diff(file1, file2, format):
    formatters_list = {
        "stylish": format_stylish,
    }
    formatter = formatters_list.get(format)
    if not formatter:
        raise KeyError(f"Unknown formatter: {format}")
    tree1 = read_file(file1)
    tree2 = read_file(file2)
    return formatter(create_diff_ast(tree1, tree2))
