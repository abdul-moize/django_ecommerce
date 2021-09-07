"""
Contains functions that verify the values of variable
"""
import re
from contants import email_regex


def validate_email(email):
    """

    Args:
        email(str): Value containing email e.g 'abc@gmail.com'
    :return:
    """
    return isinstance(email, str) and re.match(email_regex, email, re.VERBOSE)