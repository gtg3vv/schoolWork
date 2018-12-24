/*
 * Gabriel  Groover (gtg3vv)
 * HW3 - Synchronization
 * Due: 3/1/2018
 * barrier.cpp
 */

#include "barrier.h"

//Barrier Constructor
Barrier::Barrier(int val, int i)
{
    init = i;
    value = val;
    sem_init(&mutex,0,1);
    sem_init(&waitQueue,0,0);
    sem_init(&throttle,0,0);
}

//Barier Wait
void Barrier::wait() {
    sem_wait(&mutex);
    value--;
    
    //If not all threads are waiting
    if (value != 0) {
        sem_post(&mutex);
        sem_wait(&waitQueue);
        sem_post(&throttle);
    } 
    //Signal all threads to proceed
    else {
        for (int i = 0; i < init - 1; i++)
        {
            sem_post(&waitQueue);
            sem_wait(&throttle);
        }
        value = init;
        sem_post(&mutex);
    }
}

