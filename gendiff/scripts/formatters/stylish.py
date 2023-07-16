import json

from gendiff.scripts.formatters.helper import prettify_output


SUB_FORMATTERS_LIST = {
    "changed": lambda k, v: {
        f"- {k}": v["removed"],
        f"+ {k}": v["added"]
    },
    "added": lambda k, v: {f"+ {k}": v},
    "removed": lambda k, v: {f"- {k}": v},
    "children": lambda k, v: {k: format_diff(v)},
    "unchanged": lambda k, v: {k: v}
}


def format_diff(diff):
    result = {}
    for key, value in diff.items():
        marker, value = value
        sub_formatter = SUB_FORMATTERS_LIST[marker]
        result.update(sub_formatter(key, value))
    return result


def format_stylish(diff):
    result = json.dumps(format_diff(diff), indent=4)
    return prettify_output(result)
