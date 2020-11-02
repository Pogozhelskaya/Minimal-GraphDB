from itertools import product, chain

from src.cnf import WeakCNF
import pytest
from pyformlang.cfg import *
from src.cfg_algorithms import hellings, mxm_cfpq, tensor_cfg_cfpq, tensor_rsa_cfpq

grammars = [
    '\n'.join(['S -> a S', 'S -> '])
    , '\n'.join(['S -> a S a', 'S -> b S b', 'S -> c'])
    , '\n'.join(['S -> b S b b', 'S -> A', 'A -> a A', 'A -> '])
    , '\n'.join(['S -> A B', 'A -> A A', 'B -> B B', 'A -> a', 'B -> b'])
    , '\n'.join(['S -> S S', 'S -> a'])
    , '\n'.join(['S -> a S b S', 'S -> '])
]


@pytest.fixture(scope='session', params=list(chain(
    [(grammars[0], 'aaaa', True)]
    , [(grammars[0], '', True)]
    , [(grammars[1], 'abbcbba', True)]
    , [(grammars[2], 'bbabbbb', True)]
    , [(grammars[2], '', True)]
    , [(grammars[0], 'aaab', False)]
    , [(grammars[1], 'aabbaa', False)]
    , [(grammars[2], 'baabbb', False)]
)))
def manual_suite(request):
    cnf, word, expected = request.param
    return {
        'cnf': WeakCNF.from_text(cnf)
        , 'word': [Terminal(x) for x in word]
        , 'expected': expected
    }


@pytest.fixture(scope='session', params=[
    {
        'cnf': WeakCNF.from_text(gr)
        , 'word': word
    } for gr in grammars for word in CFG.from_text(gr).get_words(10)
])
def auto_true_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'cnf': WeakCNF.from_text(gr)
        , 'word': word + [Terminal('d')]
    } for gr in grammars for word in CFG.from_text(gr).get_words(10)
])
def auto_false_suite(request):
    return request.param


@pytest.fixture(scope='session', params=[
    {
        'edges': ['0 a 1', '1 a 2', '2 a 0']
        , 'cnf': grammars[4]
        , 'expected': set(product({0, 1, 2}, {0, 1, 2}))
    }
    , {
        'edges': ['0 a 1', '1 a 2', '2 a 0', '2 b 3', '3 b 2']
        , 'cnf': grammars[5]
        , 'expected': {(1, 3), (0, 2), (2, 3), (1, 2), (0, 3)} | {(i, i) for i in range(4)}
    }
    , {
        'edges': ['0 a 0', '0 b 0']
        , 'cnf': grammars[5]
        , 'expected': {(0, 0)}
    }
    , {
        'edges': ['0 b 1', '1 b 1', '1 a 2', '2 a 3', '2 b 3', '3 b 4', '4 b 3']
        , 'cnf': grammars[2]
        , 'expected': {(0, 1), (2, 4), (1, 2), (0, 4), (3, 4), (4, 3), (0, 3), (1, 4), (2, 3), (1, 3)} \
                      | {(i, i) for i in range(5)}
    }
])
def manual_suite_cfpq(request):
    return request.param


@pytest.fixture(scope='session', params=[hellings, mxm_cfpq, tensor_cfg_cfpq, tensor_rsa_cfpq])
def cfpq_algo(request):
    return request.param
