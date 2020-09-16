from pyformlang import *
from pygraphblas import *


class LabelGraph:
    def __init__(self, size):
        self.size = size
        self.vertices = set()
        self.labels = set()
        self.matrices = dict()
        self.start_states = set()
        self.final_states = set()

    def __getitem__(self, item):
        if item not in self.labels:
            self.labels.add(item)
            self.matrices[item] = Matrix.sparse(BOOL, self.size, self.size)
        return self.matrices[item]

    def __setitem__(self, key, value):
        self.matrices[key] = value

    def accepts(self, word):
        nfa = finite_automaton.EpsilonNFA(
            states=self.vertices,
            input_symbols=self.labels,
            start_state=self.start_states,
            final_states=self.final_states
        )

        for label in self.labels:
            for i, j, _ in zip(*self[label].select(lib.GxB_NONZERO).to_lists()):
                nfa.add_transition(i, label, j)

        return nfa.accepts(word)

    @classmethod
    def from_txt(cls, path):
        vertices = set()
        edges = set()
        with open(path, 'r') as f:
            for line in f:
                v, label, to = line.split()
                v, to = int(v), int(to)
                vertices |= {v, to}
                edges.add((v, label, to))

        g = LabelGraph(max(vertices) + 1)
        for v, label, to in edges:
            g[label][v, to] = True
        g.vertices = g.start_states = g.final_states = vertices

        return g

    @classmethod
    def from_regex(cls, path):
        with open(path, 'r') as f:
            regex = f.readline().replace('\n', '')

        r = regular_expression.Regex(regex).to_epsilon_nfa()\
            .to_deterministic().minimize()

        num = dict()
        for s in r.states:
            if s not in num:
                num[s] = len(num)

        edges = sorted(
            [
                (num[v], str(label), num[to])
                for v, label, to in r._transition_function.get_edges()
            ], key=lambda t: (t[1], t[0], t[2])
        )

        g = LabelGraph(len(r.states))
        for v, label, to in edges:
            g[label][v, to] = True
        g.vertices = set(num.values())
        g.start_states = set(map(num.get, r.start_states))
        g.final_states = set(map(num.get, r.final_states))

        return g
