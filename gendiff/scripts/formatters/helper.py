def prettify_output(output):
    # output = json.dumps(output, indent=4)
    patterns = {
        '"': '',
        ',': '',
        '  + ': '+ ',
        '  - ': '- ',
        "'false'": 'false',
        "'true'": 'true',
        "'null'": 'null'
    }
    for old, new in patterns.items():
        output = output.replace(old, new)
    return output
