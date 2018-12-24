#!/bin/bash
#Gabriel Groover (gtg3vv)
read -p "enter the exponent for counter.cpp: " e
TOTAL_TIME=0
RUNNING_TIME=0
if [[ "$e" = "quit" ]] ; then
  exit
fi

for i in {1..5} ; do	
  RUNNING_TIME=`./a.out "$e" | tail -1`
  TOTAL_TIME=$((RUNNING_TIME + TOTAL_TIME))
  echo "Running iteration $i..."
  echo "time taken: $RUNNING_TIME ms"
done

echo "5 iterations took $TOTAL_TIME ms"
echo "Average time was $((TOTAL_TIME / 5)) ms"