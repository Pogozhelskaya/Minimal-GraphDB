import pytest

from src.cfg_algorithms import hellings
from src.label_graph import LabelGraph
from src.cnf import WeakCNF
from src.cfg_algorithms import cyk


def test_manual_cyk(manual_suite):
    cfg = manual_suite['cnf']
    word = manual_suite['word']
    expected = manual_suite['expected']
    assert cyk(word, cfg) == expected


def test_auto_true_cyk(auto_true_suite):
    cnf = auto_true_suite['cnf']
    accepted = auto_true_suite['word']

    assert cyk(accepted, cnf) is True


def test_false_true_cyk(auto_false_suite):
    cnf = auto_false_suite['cnf']
    accepted = auto_false_suite['word']

    assert cyk(accepted, cnf) is False


def test_manual_hellings(manual_suite_hellings, tmp_path):
    graph_file = tmp_path / 'graph.txt'
    graph_file.write_text('\n'.join(manual_suite_hellings['edges']))

    g = LabelGraph.from_txt(graph_file)
    gr = WeakCNF.from_text(manual_suite_hellings['cnf'])
    actual = set(zip(*hellings(g, gr).to_lists()[:2]))
    expected = manual_suite_hellings['expected']

    assert actual == expected
