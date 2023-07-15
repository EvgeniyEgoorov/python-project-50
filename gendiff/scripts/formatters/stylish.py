import json


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
        marker, value = value
        sub_formatter = sub_formatters_list[marker]
        result.update(sub_formatter(key, value))
    return result


def format_stylish(diff):
    return prettify_output(format_diff(diff))
