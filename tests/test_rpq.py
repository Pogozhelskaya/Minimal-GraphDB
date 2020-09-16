import random
from itertools import product

import networkx
import pytest
from pygraphblas import *

from src.label_graph import LabelGraph
from src.rpq import rpq


def test_1(tmp_path):
    edges = ['0 a 1', '1 a 2', '2 a 3']

    graph = tmp_path / 'graph.txt'
    graph.write_text('\n'.join(edges))

    regex = tmp_path / 'regex.txt'
    regex.write_text('(a)(a)')

    g = LabelGraph.from_txt(graph)
    r = LabelGraph.from_regex(regex)

    actual = rpq(g, r)

    expected = Matrix.sparse(BOOL, 4, 4)
    expected[0, 2] = True
    expected[1, 3] = True

    assert expected.iseq(actual)


@pytest.fixture(scope='function', params=[
    {'n': n, 'm': m, 'r': r}
    for n in range(10, 20)
    for m in [n * (n - 1) // 2 * p // 100 for p in [10]]
    for r in ['(a)(a)', '(a|b)*', '(a)(a|b)(c)']
])
def automatic_suite(request):
    n, m, r = request.param.values()

    random_graph = networkx.gnm_random_graph(n, m, seed=29, directed=True)

    return {
        'edges': [
            f'{i} {chr(ord("a") + random.randint(0, 2))} {j}'
            for i, j in random_graph.edges
        ], 'regex': r
    }


def test_auto(automatic_suite, tmp_path):
    graph = tmp_path / 'graph.txt'
    graph.write_text('\n'.join(automatic_suite['edges']))

    regex = tmp_path / 'regex.txt'
    regex.write_text(automatic_suite['regex'])

    g = LabelGraph.from_txt(graph)
    r = LabelGraph.from_regex(regex)

    actual = rpq(g, r)

    paths = dict()

    for label in g.labels:
        for i, j, _ in zip(*g[label].select(lib.GxB_NONZERO).to_lists()):
            if (i, j) not in paths:
                paths[i, j] = set()
            paths[i, j].add(label)

    for k in range(g.size):
        for i in range(g.size):
            for j in range(g.size):
                if ((i, k) in paths) and ((k, j) in paths):
                    if (i, j) not in paths:
                        paths[i, j] = set()
                    paths[i, j] |= set(map(
                        lambda s: s[0] + s[1],
                        product(paths[i, k], paths[k, j])
                    ))

    expected = Matrix.sparse(BOOL, g.size, g.size)
    for i in range(g.size):
        for j in range(g.size):
            if (i, j) in paths:
                for path in paths[i, j]:
                    if r.accepts(path):
                        expected[i, j] = True
                        break

    assert expected.iseq(actual)
