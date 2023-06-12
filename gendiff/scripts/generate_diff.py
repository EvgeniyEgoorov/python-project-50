import json


def generate_diff(
        file_path1 = 'demo_files/file1.json',
        file_path2 = 'demo_files/file2.json'
):
    file_content1 = json.load(open(file_path1))
    file_content2 = json.load(open(file_path2))
    
    union_keys = sorted(file_content1 | file_content2)

    result = {}

    for key in union_keys:
        if key not in file_content2:
            result[("- " + key)] = file_content1[key]
        elif key not in file_content1:
            result[("+ " + key)] = file_content2[key]
        elif file_content1[key] != file_content2[key]:
            result[("- " + key)] = file_content1[key]
            result[("+ " + key)] = file_content2[key]
        else:
            result[("  " + key)] = file_content2[key]

    body =  "\n".join(f"    {k}: {v}" for k, v in result.items())
    return "\n".join(["{", body, "}"])


if __name__ == "__main__":
    print(generate_diff())