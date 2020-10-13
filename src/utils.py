from pygraphblas import *


def transitive_closure(m: Matrix) -> Matrix:
    tc = m.dup()

    while True:
        prev = tc.nvals
        tc += tc @ tc
        if prev == tc.nvals:
            break

    return tc
