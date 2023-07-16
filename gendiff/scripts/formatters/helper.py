def prettify_output(output):
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
