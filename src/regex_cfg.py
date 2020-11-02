from pyformlang.cfg import *
from pyformlang.regular_expression import Regex

from src.cnf import WeakCNF


class RegexCFG:
    def __init__(self):
        self.start_symbol = None
        self.boxes = dict()

    def to_cfg(self):
        variables = set()
        terminals = set()
        start_symbol = self.start_symbol
        productions = set()

        cnt = 1
        for x in self.boxes:
            head = Variable(x)
            variables.add(head)
            for box in self.boxes[x]:
                name = {box.start_state: head}
                for s in box.states:
                    if s not in name:
                        name[s] = Variable(f'S{cnt}')
                        cnt += 1
                        variables.add(name[s])
                    if s in box.final_states:
                        productions.add(Production(name[s], []))
                for v in box._transition_function._transitions:
                    for label in box._transition_function._transitions[v]:
                        to = box._transition_function._transitions[v][label]

                        if label.value == label.value.lower():
                            terminals.add(Terminal(label.value))
                            productions.add(Production(name[v], [Terminal(label.value), name[to]]))
                        else:
                            productions.add(Production(name[v], [Variable(label.value), name[to]]))

        return CFG(
            variables=variables,
            terminals=terminals,
            start_symbol=start_symbol,
            productions=productions
        )

    def to_cnf(self):
        cnf = self.to_cfg()

        wcnf = WeakCNF(
            variables=cnf.variables,
            terminals=cnf.terminals,
            start_symbol=cnf.start_symbol,
            productions=cnf.productions
        )

        return wcnf.to_weak_normal_form()

    @classmethod
    def from_text(cls, text, start_symbol='S'):
        rsm = RegexCFG()

        rsm.start_symbol = start_symbol

        productions = text.split('\n')

        for p in productions:
            head, body = p.split(' -> ')
            body = body.replace('epsilon', '$').replace('eps', '$')
            if body == '':
                body = '$'
            rsm.boxes[head] = rsm.boxes.get(head, list()) + [
                Regex(body).to_epsilon_nfa().to_deterministic().minimize()
            ]

        return rsm

    @classmethod
    def from_txt(cls, path):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))

        text = '\n'.join(productions)

        return RegexCFG.from_text(text)
