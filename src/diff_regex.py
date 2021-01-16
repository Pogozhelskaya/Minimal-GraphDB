import copy

from pyformlang.regular_expression import Regex
from pyformlang.regular_expression.regex_objects import *


def is_nullable(regex):
    if type(regex.head) in {Epsilon, KleeneStar}:
        return True

    if type(regex.head) == Union:
        return is_nullable(regex.sons[0]) or is_nullable(regex.sons[1])

    if type(regex.head) == Concatenation:
        return is_nullable(regex.sons[0]) and is_nullable(regex.sons[1])

    return False


def differ(regex, symbol):
    if type(regex.head) == Union:
        regex.sons[0] = differ(regex.sons[0], symbol)
        regex.sons[1] = differ(regex.sons[1], symbol)
    elif type(regex.head) == Concatenation:
        if is_nullable(regex.sons[0]):
            regex1 = copy.deepcopy(regex.sons[0])
            regex2 = copy.deepcopy(regex.sons[1])
            regex1 = differ(regex1, symbol).concatenate(regex2)
            regex.head = Union()
            regex.sons[0] = regex1
            regex.sons[1] = differ(regex.sons[1], symbol)
        else:
            regex.sons[0] = differ(regex.sons[0], symbol)
    elif type(regex.head) == KleeneStar:
        regex1 = copy.deepcopy(regex.sons[0])
        regex = differ(regex1, symbol).concatenate(regex)
    else:
        if regex.head.value == symbol:
            regex.head = Epsilon()
        else:
            regex.head = Empty()
    return regex


def accepts(regex, word):
    regex = Regex(regex)
    for symbol in word:
        regex = differ(regex, symbol)
    return is_nullable(regex)
