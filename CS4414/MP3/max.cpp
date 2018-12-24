/*
 * Gabriel  Groover (gtg3vv)
 * HW3 - Synchronization
 * Due: 3/1/2018
 * max.cpp
 */


#include <iostream>
#include <pthread.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "max.h"

using namespace std;

//Log base 2 function using  bitshifts
int log2(int n)
{
    int val = 0;
    while (n >>= 1)
        val++;
    return val;
    
}

//Helper function for single thread
void* getMax(void* a){  
    argStruct* args = (argStruct*) a;
    int currentRound = 1;
    bool done = false;
    
    //Loop until thread exits
    while (true)
    {
      if (!done)
      {
	  //Locate indexes based on thread id and round
	  int idx1 = args->tid * pow(2, currentRound);
	  int idx2 = idx1 + pow(2, currentRound-1);
	  
	  //cout << "round " << currentRound << " " << idx1 << " " <<idx2 << endl;
	  //Exit thread if work is done
	  if (currentRound > numRounds)
	      pthread_exit(0);
	  
	  //If thread should still be doing comparisons, store max in array
	  if (idx1 < numList.size() && idx2 < numList.size())
	  {
	    numList[idx1] = max(numList[idx1], numList[idx2]);
	    //cout << "adding indexes " << idx1 << " " << idx2 << endl;
	  } else done = true;
      }
           
         //Wait for all threads to complete
         b->wait();
         currentRound++;
    }   
}

//Main function to set parameters and  spool up threads
int main(){
    
    //Read user input until empty line
    string num;
    while (getline(cin, num))
    {
      if (num.empty())
	break;
      numList.push_back(atoi(num.c_str()));
    }
    
    //Set round and thread counts
    numRounds = log2(int(numList.size()));
    int numThreads = int(numList.size()) / 2;
    //cout << numRounds << " rounds" << endl;
    //cout << numThreads << " threads" << endl;
    
    //Initialize thread parameters
    argStruct args[numThreads];
    pthread_t tids[numThreads];
    pthread_attr_t attr;
    pthread_attr_init(&attr);
    b = new Barrier(numThreads, numThreads);
	
    //Start the threads and pass in thread number
    for (int i = 0; i < numThreads; i++)
    {
        args[i].tid = i;
        pthread_create(&tids[i],&attr,getMax,&args[i]);
    }
    
    //Join first thread and retrieve max from index 0
    pthread_join(tids[0],NULL);
    cout << numList[0] << endl;
    
}



