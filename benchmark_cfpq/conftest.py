import os
import shutil
from glob import glob
from pathlib import Path

import pytest

from src.cfg_algorithms import hellings, mxm_cfpq, tensor_cfg_cfpq, tensor_rsa_cfpq

cwd = './benchmark_cfpq'
results_dir = cwd + '/results'
data_for_cfpq_dir = cwd + '/myDataForCFPQ'

if not os.path.exists(data_for_cfpq_dir):
    os.mkdir(data_for_cfpq_dir)

if not os.path.exists(results_dir):
    os.mkdir(results_dir)

if len(os.listdir(data_for_cfpq_dir)) == 0:
    shutil.unpack_archive(data_for_cfpq_dir + '.tar.xz', cwd)

suites = [
    {
        'id': f'algo={algo.__name__},graph={graph.split("/")[-3]},graph_file={Path(graph).stem},grammar={Path(grammar).stem}'
        , 'algo': algo
        , 'algo_name': algo.__name__
        , 'graph': graph
        , 'graph_name': graph.split("/")[-3]
        , 'graph_filename': Path(graph).stem
        , 'grammar': grammar
        , 'grammar_name': Path(grammar).stem
    }
    for algo in [
        hellings
        , mxm_cfpq
        , tensor_cfg_cfpq
        , tensor_rsa_cfpq
    ]
    for graph in glob(f'{data_for_cfpq_dir}/*/graphs/*')
    for grammar in glob(f'{data_for_cfpq_dir}/{graph.split("/")[-3]}/grammars/*')
]

params = [
    pytest.param(
        {'algo': x['algo'], 'name': x['algo_name']}
        , {'graph': x['graph'], 'name': x['graph_name'], 'filename': x['graph_filename']}
        , {'grammar': x['grammar'], 'name': x['grammar_name']}
        , marks=[
            getattr(pytest.mark, x['algo_name'])
            , getattr(pytest.mark, x['graph_name'])
            , getattr(pytest.mark, x['grammar_name'])
            , getattr(pytest.mark, x['graph_filename'])
        ]
        , id=x['id']
    )
    for x in suites
]


def pytest_configure(config):
    for param in params:
        for mark in param.marks:
            config.addinivalue_line('markers', f'{mark}: generated marker')
