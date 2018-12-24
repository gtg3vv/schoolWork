/*
 * Gabriel  Groover (gtg3vv)
 * HW3 - Synchronization
 * Due: 3/1/2018
 * max.h
 */
#ifndef MAX_H
#define MAX_H

#include <vector>
#include "barrier.h"

//Data  Structures
typedef struct argStruct {
    int tid;
} argStruct;


//Global Variables
std::vector<int> numList;
int numRounds;
Barrier *b; //Global barrier  instance

//Methods
int log2(int n); //Computes log base 2 of n
void* getMax(void* a); //Helper function for each thread

#endif