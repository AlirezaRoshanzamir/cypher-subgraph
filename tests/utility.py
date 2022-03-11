import string


def remove_whitespace(input_string: str) -> str:
    return input_string.translate(str.maketrans("", "", string.whitespace))
