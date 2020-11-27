import argparse

from pyformlang.cfg import *

from src.cfg_algorithms import cyk
from src.regex_cfg import RegexCFG


def check(script):
    script = [Terminal(x) for x in script.replace(' ', '@')]
    return cyk(script, RegexCFG.from_txt('grammar.txt').to_cnf())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='script analyzer using CYK')
    parser.add_argument(
        '--script'
        , required=False
        , type=str
        , help='path to script.txt'
        , default=None
    )
    args = parser.parse_args()

    script = ''
    with open(args.script, 'r') as f:
        for line in f:
            script += line.replace('\n', '')

    accepts = check(script)

    print(f'Script is {"accepted" if accepts else "not accepted"}')