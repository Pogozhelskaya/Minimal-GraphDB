from pyformlang.cfg import *


class WeakCNF(CFG):
    def to_weak_normal_form(self):
        gen_eps = self.generate_epsilon()
        cfg = self.to_normal_form()
        if gen_eps is True:
            cfg._productions |= {Production(cfg._start_symbol, [])}
        return WeakCNF(
            cfg.variables,
            cfg.terminals,
            cfg.start_symbol,
            cfg.productions
        )

    @classmethod
    def from_text(cls, text, start_symbol=Variable("S")):
        cnf = CFG.from_text(text, start_symbol=start_symbol)
        wcnf = WeakCNF(
            cnf.variables,
            cnf.terminals,
            cnf.start_symbol,
            cnf.productions
        )
        return wcnf.to_weak_normal_form()

    @classmethod
    def from_txt(cls, path):
        productions = []
        with open(path, 'r') as f:
            for line in f:
                production = line.split()
                productions.append(production[0] + ' -> ' + ' '.join(production[1:]))
        grammar = WeakCNF.from_text('\n'.join(productions))
        return grammar
