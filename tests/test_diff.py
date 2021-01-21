from src.diff_regex import accepts
from itertools import chain
import pytest


@pytest.fixture(scope='session', params=list(chain(
    [('a*', 'aaaa', True)]
    , [('(b | a)*.d', 'bababaaad', True)]
    , [('( a* ) | (a* b*)', 'abababab', False)]
    , [('(b | a)*.d', 'babab', False)]
    , [('a*', '', True)]
    , [('(a).(a|b)', 'aa', True)]
    , [('(a).(a|b)', 'ac', False)]
    , [('(a|b)*', 'abab', True)]
    , [('a.(b|(c.(d|(e.(f|f.f)))))', 'aceff', True)]
    , [('a', 'a', True)]
)))
def manual_suite_diff(request):
    regex, word, expected = request.param
    return {
        'regex': regex
        , 'word': word
        , 'expected': expected
    }


def test_manual_diff(manual_suite_diff):
    regex = manual_suite_diff['regex']
    word = manual_suite_diff['word']
    expected = manual_suite_diff['expected']

    actual = accepts(regex, word)

    assert actual == expected
