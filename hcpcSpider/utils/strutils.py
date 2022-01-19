def remove_empty_char(s: str):
    empty_chars = [
        '\n',
        '\t'
    ]
    for char in empty_chars:
        s.replace(char, '')

    return s
