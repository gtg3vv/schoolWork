#!/bin/bash
#Gabriel Groover
#lab 101

#store the two file name parameters
dict="$1"
square="$2"

#Take running time from each run of the program and add to previous value
RUNNING_TIME=`./a.out $dict $square | tail -1`
RUNNING_TIME=$((`./a.out $dict $square | tail -1` + RUNNING_TIME))
RUNNING_TIME=$((`./a.out $dict $square | tail -1` + RUNNING_TIME))
RUNNING_TIME=$((`./a.out $dict $square | tail -1` + RUNNING_TIME))
RUNNING_TIME=$((`./a.out $dict $square | tail -1` + RUNNING_TIME))

#output the average runtime as calculated by totaltime/numtrials
echo $((RUNNING_TIME / 5))
 
 