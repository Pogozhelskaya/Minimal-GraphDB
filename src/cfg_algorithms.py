from typing import List

from pyformlang.cfg import Terminal
from pygraphblas import Matrix, BOOL, lib

from src.label_graph import LabelGraph
from src.cnf import WeakCNF


def cyk(w: List[Terminal], cnf: WeakCNF):
    n = len(w)

    if n == 0:
        return cnf.generate_epsilon()

    dp = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for p in cnf.productions:
            if len(p.body) == 1 and p.body[0] == w[i]:
                dp[0][i].add(p.head)

    for d in range(1, n):
        for i in range(n - d):
            for s in range(d):
                l, r = dp[s][i], dp[d - s - 1][i + s + 1]
                for p in cnf.productions:
                    if len(p.body) == 2 and p.body[0] in l and p.body[1] in r:
                        dp[d][i].add(p.head)

    return cnf.start_symbol in dp[n - 1][0]


def hellings(g: LabelGraph, gr: WeakCNF) -> Matrix:
    result = LabelGraph(g.size)

    for variable in gr.variables:
        result.dict[variable] = Matrix.sparse(BOOL, g.size, g.size)

    for label in g.labels:
        result[Terminal(label)] = g[label].dup()
        for i, j, _ in zip(*result[Terminal(label)].select(lib.GxB_NONZERO).to_lists()):
            for production in gr.productions:
                if len(production.body) == 1 and production.body[0] == Terminal(label):
                    head = production.head
                    result.dict[head][i, j] = True

    if gr.generate_epsilon():
        for i in range(g.size):
            result.dict[gr.start_symbol][i, i] = True

    changing = True
    while changing:
        changing = False
        for p in gr.productions:
            if len(p.body) == 2:
                for i, k in zip(*result.dict[p.body[0]].select(lib.GxB_NONZERO).to_lists()[:2]):
                    for l, j in zip(*result.dict[p.body[1]].select(lib.GxB_NONZERO).to_lists()[:2]):
                        if k == l:
                            if (i, j) not in zip(*result.dict[p.head].select(lib.GxB_NONZERO).to_lists()[:2]):
                                changing = True
                                result.dict[p.head][i, j] = True

    return result.dict[gr.start_symbol]
