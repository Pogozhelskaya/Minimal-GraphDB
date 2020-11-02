from src.cfg_algorithms import cyk
from src.label_graph import LabelGraph
from src.regex_cfg import RegexCFG


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


def test_manual_cfpq(manual_suite_cfpq, cfpq_algo, tmp_path):
    graph_file = tmp_path / 'graph.txt'
    graph_file.write_text('\n'.join(manual_suite_cfpq['edges']))

    g = LabelGraph.from_txt(graph_file)

    if cfpq_algo.__name__ == 'tensor_rsa_cfpq':
        gr = RegexCFG.from_text(manual_suite_cfpq['cnf'])
    else:
        gr = RegexCFG.from_text(manual_suite_cfpq['cnf']).to_cnf()

    actual = cfpq_algo(g, gr)
    expected = manual_suite_cfpq['expected']

    assert actual == expected
