import argparse
import timeit
from statistics import fmean, variance

from src.label_graph import LabelGraph
from src.rpq import rpq, rpq_with_linear_tc

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='command line interface for simple graph database')
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

    g = LabelGraph.from_txt(args.graph)
    r = LabelGraph.from_regex(args.regex)

    print(str(args.graph) + " " + str(args.regex))

    time_sum_1 = 0
    time_sum_2 = 0

    for i in range(5):
        time_1 = timeit.default_timer()
        res_1 = rpq(g, r)
        time_sum_1 += timeit.default_timer() - time_1

        time_2 = timeit.default_timer()
        res_2 = rpq_with_linear_tc(g, r)
        time_sum_2 += timeit.default_timer() - time_2

        assert (res_1.nvals == res_2.nvals)
        print(str(res_1.nvals))

    print(str(time_sum_1 / 5))
    print(str(time_sum_2 / 5))

    res = rpq(g, r)
    srcs = None
    if args.sources is not None:
        with open(args.sources, 'r') as f:
            srcs = list(map(int, f.readline().split()))

    dsts = None
    if args.destinations is not None:
        with open(args.destinations, 'r') as f:
            dsts = list(map(int, f.readline().split()))
    f = open("output.txt", 'a')
    f.write(str(args.graph) + " " + str(args.regex) + "\n")
    start_time = timeit.default_timer()
    for i, j, _ in zip(*res.to_lists()):
        if (srcs is None) or (i in srcs):
            if (dsts is None) or (j in dsts):
                f.write(f'{i} to {j}')
    print(str(timeit.default_timer() - start_time))
    f.close()
