#!/bin/bash
# A script to test the program located at the path defined in the $program variable.
#
# Usage:
#  test.sh [suite] [memcheck] [test_limit]
# Where:
#  [suite]      - the name of the test folder located inside the "tests" directory
#  [memcheck]   - true/false indicating whether to run the tests with valgrind
#  [test_limit] - the maximum number of tests to run
#
# A test is considered passed if valgrind does not report any errors and the output
# perfectly matches the expected result.

program=./algorithm_x
subdir=$1
memcheck=$2
limit=$3
total=0
passed=0

for t in tests/$subdir/*.in
do
    total=$((total + 1))

    if ( [ "$memcheck" = "false" ] && $program < $t > result.out ) || \
        ( [ "$memcheck" != "false" ] && valgrind --leak-check=full -q --error-exitcode=1 $program < $t > result.out )
then
    sort result.out > result.out.sorted
    sort "${t%in}out.sorted" -o "${t%in}out.sorted"

    if diff -q "${t%in}out.sorted" result.out.sorted
    then
        passed=$((passed + 1))
    else
        diff "${t%in}out.sorted" result.out.sorted -y
        cat "${t%in}out.sorted"
    fi
else
    echo "Valgrind reports an error in test ${t%.in}"
    fi

    if (( limit <= total )); then
        break
    fi

done

echo "Passed ${passed} out of ${total} tests"

rm result.out 2>/dev/null
rm result.out.sorted 2>/dev/null
