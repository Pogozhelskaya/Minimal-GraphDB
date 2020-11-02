from typing import List

from pyformlang.cfg import Terminal, CFG, Variable
from pygraphblas import Matrix, BOOL, lib

from src.cnf import WeakCNF
from src.label_graph import LabelGraph
from src.regex_cfg import RegexCFG
from src.utils import transitive_closure


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


def hellings(g: LabelGraph, gr: WeakCNF):
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

    return set(zip(*result.dict[gr.start_symbol].to_lists()[:2]))


def mxm_cfpq(g: LabelGraph, gr: WeakCNF):
    m = LabelGraph(g.size)

    complex_productions = set()

    for production in gr.productions:
        if len(production.body) == 1:
            m[production.head] += g[production.body[0].value]
        elif len(production.body) == 2:
            complex_productions.add(production)

    if gr.generate_epsilon():
        for i in range(g.size):
            m[gr.start_symbol][i, i] = True

    changed = True
    while changed:
        changed = False
        for production in complex_productions:
            old_nnz = m[production.head].nvals
            m[production.head] += m[production.body[0]] @ m[production.body[1]]
            new_nnz = m[production.head].nvals
            changed |= not old_nnz == new_nnz
    return set(zip(*m[gr.start_symbol].to_lists()[:2]))


def tensor_cfg_cfpq(g: LabelGraph, gr: CFG):
    m = g.dup()

    graph_size = 0
    for p in gr.productions:
        graph_size += len(p.body) + 1
    rsa = LabelGraph(graph_size)

    heads = dict()

    cur = 0
    for p in gr.productions:
        rsa.start_states.add(cur)
        heads[(cur, cur + len(p.body))] = p.head
        if len(p.body) == 0:
            for i in m.vertices:
                m[p.head][i, i] = True
        for unit in p.body:
            if isinstance(unit, Terminal):
                rsa[unit.value][cur, cur + 1] = True
            else:
                rsa[unit][cur, cur + 1] = True
            cur += 1
        rsa.final_states.add(cur)
        cur += 1

    tc = m.get_intersection(rsa).get_transitive_closure()

    while True:
        prev = tc.nvals
        for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
            i_m, i_rsa = i // rsa.size, i % rsa.size
            j_m, j_rsa = j // rsa.size, j % rsa.size
            if (i_m in m.start_states) and (i_rsa in rsa.start_states):
                if (j_m in m.final_states) and (j_rsa in rsa.final_states):
                    m[heads[(i_rsa, j_rsa)]][i_m, j_m] = True

        tmp = m.get_intersection(rsa)
        for label in tmp.labels:
            tc += tmp[label]
        tc = transitive_closure(tc)

        if prev == tc.nvals:
            break

    ans = set(zip(*m[gr.start_symbol].to_lists()[:2]))

    return ans


def tensor_rsa_cfpq(g: LabelGraph, gr: RegexCFG):
    m = g.dup()

    graph_size = 0
    for x in gr.boxes:
        for box in gr.boxes[x]:
            graph_size += len(box.states)
    rsa = LabelGraph(graph_size)

    heads = dict()

    cur = 0
    for x in gr.boxes:
        for box in gr.boxes[x]:
            name = dict()
            for s in box.states:
                if s not in name:
                    name[s] = cur
                    cur += 1
                if s in box.final_states:
                    rsa.final_states.add(name[s])
            rsa.start_states.add(name[box.start_state])
            if box.start_state in box.final_states:
                for i in m.vertices:
                    m[Variable(x)][i, i] = True
            for s in box.final_states:
                heads[(name[box.start_state], name[s])] = Variable(x)
            for v in box._transition_function._transitions:
                for label in box._transition_function._transitions[v]:
                    to = box._transition_function._transitions[v][label]

                    if label.value == label.value.lower():
                        rsa[label.value][name[v], name[to]] = True
                    else:
                        rsa[Variable(label.value)][name[v], name[to]] = True

    tc = m.get_intersection(rsa).get_transitive_closure()

    while True:
        prev = tc.nvals
        for i, j, _ in zip(*tc.select(lib.GxB_NONZERO).to_lists()):
            i_m, i_rsa = i // rsa.size, i % rsa.size
            j_m, j_rsa = j // rsa.size, j % rsa.size
            if (i_m in m.start_states) and (i_rsa in rsa.start_states):
                if (j_m in m.final_states) and (j_rsa in rsa.final_states):
                    m[heads[(i_rsa, j_rsa)]][i_m, j_m] = True

        tmp = m.get_intersection(rsa)
        for label in tmp.labels:
            tc += tmp[label]
        tc = transitive_closure(tc)

        if prev == tc.nvals:
            break

    ans = set(zip(*m[gr.start_symbol].to_lists()[:2]))

    return ans
