import argparse

from src.LabeledGraph import LabeledGraph
from src.rpq import rpq

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='command line interface for simple graph database')
    parser.add_argument(
        '--graph'
        , required=True
        , type=str
        , help='path to graph.txt file'
    )
    parser.add_argument(
        '--regex'
        , required=True
        , type=str
        , help='path to regex.txt file'
    )
    parser.add_argument(
        '--sources'
        , required=False
        , type=str
        , help='path to sources.txt file'
    )
    parser.add_argument(
        '--destinations'
        , required=False
        , type=str
        , help='path to destinations.txt file'
    )
    args = parser.parse_args()

    g = LabeledGraph.from_txt(args.graph)
    r = LabeledGraph.from_regex(args.regex)

    res = rpq(g, r)

    srcs = None
    if args.sources is not None:
        with open(args.sources, 'r') as f:
            srcs = list(map(int, f.readline().split()))

    dsts = None
    if args.destinations is not None:
        with open(args.destinations, 'r') as f:
            dsts = list(map(int, f.readline().split()))

    for i, j, _ in zip(*res.to_lists()):
        if (srcs is None) or (i in srcs):
            if (dsts is None) or (j in dsts):
                print(f'There is path from {i} to {j} in graph')
