//Gabriel Groover (gtg3vv)
// February, 4th 2016 Stack.cpp

#include <iostream>
#include "Stack.h"


Stack::Stack( ) {
  count = 0;
  head = new StackNode();
  tail = new StackNode();
  head->next = tail;
}

int Stack::top( ) {
  return head->next->value;
	
}

void Stack::push(int s) {
  StackNode *node = new StackNode();
  node->value = s;
  node->next = head->next;
  head->next = node;
  count++;

}

void Stack::pop() {
  if(head->next != tail){
   head->next = head->next->next;
   count--;
  }
  else
    cout << "The list is already empty" << endl;

  
}

