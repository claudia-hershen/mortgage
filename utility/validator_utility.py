"""Utility Functions."""


def is_number(test_value):
    """Check if test_value is a number.

    A number is considered to be an int or a float

    Params:
        test_value
    Return:
        True or False
    """
    return type(test_value) == int or type(test_value) == float


def number_bigger_than(test_value, value):
    """Check if test_value is bigger than value.

    Params:
        test_value
        value
    Return:
        True or False
    """
    if is_number(test_value) and is_number(value):
        return test_value > value
    return None


def number_smaller_than(test_value, value):
    """Check if test_value is smaller than value.

    Params:
        test_value
        value
    Return:
        True or False
    """
    if is_number(test_value) and is_number(value):
        return test_value < value
    return None


def is_negative_number(test_value):
    """Check if test_value is a negative number.

    Params:
        test_value
    Return:
        True or False
    """
    return is_number(test_value) and number_smaller_than(test_value, 0)
