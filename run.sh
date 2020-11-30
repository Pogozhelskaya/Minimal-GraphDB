#!/bin/sh

REGEX=refinedDataForRPQ/LUBM300/regexes/'q*0'
# shellcheck disable=SC2039
GRAPHS=("refinedDataForRPQ/LUBM300/LUBM300.txt" "refinedDataForRPQ/LUBM500/LUBM500.txt" "refinedDataForRPQ/LUBM1M/LUBM1M.txt" "refinedDataForRPQ/LUBM1.5M/LUBM1.5M.txt" "refinedDataForRPQ/LUBM1.9M/LUBM1.9M.txt")

# shellcheck disable=SC2039
for (( i=0; i < 5; i++ ))
do
    for r in $REGEX
    do
        python3 main.py --graph "${GRAPHS[i]}" --regex "$r"
    done
done