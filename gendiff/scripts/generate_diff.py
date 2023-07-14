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
        return {"removed": tree1[key], "added": tree2[key]}
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


def pretty_output(output):
    patterns = {
        '"': '',
        ',': '',
        '  + ': '+ ',
        '  - ': '- '
    }
    for old, new in patterns.items():
        output = output.replace(old, new)
    return output


def stylish(diff):
    def inner(diff):
        result = {}
        for key, value in diff.items():
            if all([("removed" in value), ("added" in value)]):
                result[f"- {key}"] = value["removed"]
                result[f"+ {key}"] = value["added"]
            elif "added" in value:
                result[f"+ {key}"] = value["added"]
            elif "removed" in value:
                result[f"- {key}"] = value["removed"]
            elif "unchanged" in value:
                result[key] = value["unchanged"]
            else:
                result[key] = inner(value["children"])
        return result
    result = json.dumps(inner(diff), indent=4)
    return pretty_output(result)


def generate_diff(file1, file2, format):
    formatters_list = {
        "stylish": stylish,
    }
    formatter = formatters_list.get(format)
    if not formatter:
        raise KeyError(f"Unknown formatter: {format}")
    tree1 = read_file(file1)
    tree2 = read_file(file2)
    return formatter(create_diff_ast(tree1, tree2))
