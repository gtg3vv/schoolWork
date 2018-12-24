/*
 * Gabriel  Groover (gtg3vv)
 * HW3 - Synchronization
 * Due: 3/1/2018
 * barrier.h
 */

#ifndef BARRIER_H
#define BARRIER_H

#include <semaphore.h>

//Barrier Class as outlined in lecture on 3/22
class Barrier {
    private:
        int value; //semaphore value
        sem_t mutex;
        sem_t waitQueue;
        sem_t throttle;
        int init; //number of threads initially
        
    public: 
        Barrier(int val, int i);
        void wait();
};

#endif