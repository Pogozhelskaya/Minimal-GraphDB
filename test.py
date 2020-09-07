from pygraphblas import Matrix
from pyformlang.finite_automaton import State, EpsilonNFA, Symbol

import pytest


def test_mxm():
    m = Matrix.from_lists([0, 1, 2], [0, 1, 2], [1, 2, 3])
    n = Matrix.from_lists([0, 1, 2], [0, 1, 2], [1, 2, 3])

    actual_res = m @ n

    expected_res = Matrix.from_lists([0, 1, 2], [0, 1, 2], [1, 4, 9])

    assert actual_res.iseq(expected_res), "Not equal"


def test_intersection():
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)

    symbol_a = Symbol("a")
    symbol_b = Symbol("b")
    symbol_c = Symbol("c")

    dfa0 = EpsilonNFA()
    dfa0.add_start_state(state0)
    dfa0.add_final_state(state2)
    dfa0.add_transition(state0, symbol_a, state1)
    dfa0.add_transition(state1, symbol_b, state1)
    dfa0.add_transition(state1, symbol_c, state2)

    dfa1 = EpsilonNFA()
    dfa1.add_start_state(state0)
    dfa1.add_final_state(state2)
    dfa1.add_transition(state0, symbol_a, state1)
    dfa1.add_transition(state1, symbol_b, state2)
    dfa1.add_transition(state1, symbol_c, state2)

    res = dfa0 & dfa1
    check_correctness(res)


def check_correctness(res: EpsilonNFA):
    assert res.accepts("ac")
    assert not res.accepts("ab")
    assert not res.accepts("abc")
