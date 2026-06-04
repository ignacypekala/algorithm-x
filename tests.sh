#!/bin/bash
valgrind=${1:-false}
test_limit=${2:-5000}

make algorithm_x > /dev/null

for pack in tests/*; do
    pack_name=${pack#tests/}
    echo "Pack $pack_name: "
    ./test.sh $pack_name $valgrind $test_limit
    echo
done
