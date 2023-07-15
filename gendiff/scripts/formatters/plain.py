SUB_FORMATTERS_LIST = {
    "added": lambda p, v: (
        f"Property '{p}' was added with value: {process_value(v)}"
    ),
    "removed": lambda p, _: f"Property '{p}' was removed",
    "changed": lambda p, v: (
        f"Property '{p}' was updated. "
        f"From {process_value(v['removed'])} to {process_value(v['added'])}"
    ),
    "children": lambda p, v: format_diff(v, p)
}


def process_prop(key, path):
    if path:
        return f"{path}.{key}"
    return key


def process_value(value):
    if type(value) in [dict, set]:
        return '[complex value]'
    if type(value) == bool:
        return str(value).lower()
    if type(value) == int:
        return value
    return f"'{value}'"


def prettify_output(output):
    patterns = {
        '"': '',
        "'false'": 'false',
        "'true'": 'true',
        "'null'": 'null'
    }
    for old, new in patterns.items():
        output = output.replace(old, new)
    return output


def format_diff(diff, path=''):
    result = []
    for key, value in diff.items():
        marker, value = value
        if marker == "unchanged":
            continue
        sub_formatter = SUB_FORMATTERS_LIST[marker]
        result.append(sub_formatter(process_prop(key, path), value))
    return "\n".join(result)


def format_plain(diff):
    return prettify_output(format_diff(diff))
