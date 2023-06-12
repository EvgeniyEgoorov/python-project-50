import json


def generate_diff(file_path1, file_path2):

    file_content1 = json.load(open(file_path1))
    file_content2 = json.load(open(file_path2))

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
