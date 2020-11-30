if [ ! -f ./benchmark_cfpq/myDataForCFPQ.tar.xz ]; then
  cd ./benchmark_cfpq/
  gdown https://drive.google.com/uc?id=1UDw3OTJG25GM8z_R84D8WiiTkuLxCfLM
  cd ../
fi

echo "Started benchmark MemoryAliases"
python3 -m pytest -vv -s benchmark_cfpq/test_benchmark_cfpq.py -m "MemoryAliases"
echo "Ended benchmark MemoryAliases"

echo "Started benchmark FullGraph"
python3 -m pytest -v -s benchmark_cfpq/test_benchmark_cfpq.py -m "(FullGraph) and (not hellings)"
echo "Ended benchmark FullGraph"

echo "Started benchmark WorstCase"
python3 -m pytest -v -s benchmark_cfpq/test_benchmark_cfpq.py -m "(WorstCase) and (not hellings)"
echo "Ended benchmark WorstCase"
