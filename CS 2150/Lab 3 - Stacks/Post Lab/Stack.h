
//Gabriel Groover (gtg3vv)
// February, 4th 2016 Stack.h
#ifndef STACK_H
#define STACK_H

#include <iostream>
#include <string>
#include "StackNode.h"

using namespace std;

class Stack {
public:
    Stack( );				//Constructor
    bool isEmpty() const;		//Returns true if empty; else false
    int top();
    void push(int s);
    void pop();

private:
    StackNode *head, *tail;
    int count;
};

#endif

