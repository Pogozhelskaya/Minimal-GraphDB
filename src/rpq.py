from pygraphblas import *

from src.label_graph import LabelGraph





def rpq(g: LabelGraph, r: LabelGraph) -> Matrix:
    kron = LabelGraph(g.size * r.size)
    tmp = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in g.labels:
        g[label].kronecker(r[label], out=tmp)
        kron[label] += tmp

    transitive_closure = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in kron.labels:
        transitive_closure += kron[label]

    while True:
        prev = transitive_closure.nvals
        transitive_closure += transitive_closure @ transitive_closure
        if prev == transitive_closure.nvals:
            break

    ans = Matrix.sparse(BOOL, g.size, g.size)
    for i, j, _ in zip(*transitive_closure.select(lib.GxB_NONZERO).to_lists()):
        i_g, i_r = i // r.size, i % r.size
        j_g, j_r = j // r.size, j % r.size
        if (i_g in g.start_states) and (i_r in r.start_states):
            if (j_g in g.final_states) and (j_r in r.final_states):
                ans[i_g, j_g] = True

    return ans


def rpq_with_linear_tc(g: LabelGraph, r: LabelGraph) -> Matrix:
    kron = LabelGraph(g.size * r.size)
    tmp = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in g.labels:
        g[label].kronecker(r[label], out=tmp)
        kron[label] += tmp

    transitive_closure = Matrix.sparse(BOOL, kron.size, kron.size)
    for label in kron.labels:
        transitive_closure += kron[label]
    tmp = transitive_closure.dup()
    while True:
        prev = transitive_closure.nvals
        transitive_closure += transitive_closure @ tmp
        if prev == transitive_closure.nvals:
            break

    ans = Matrix.sparse(BOOL, g.size, g.size)
    for i, j, _ in zip(*transitive_closure.select(lib.GxB_NONZERO).to_lists()):
        i_g, i_r = i // r.size, i % r.size
        j_g, j_r = j // r.size, j % r.size
        if (i_g in g.start_states) and (i_r in r.start_states):
            if (j_g in g.final_states) and (j_r in r.final_states):
                ans[i_g, j_g] = True

    return ans