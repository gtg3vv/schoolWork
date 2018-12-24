//Gabriel Groover (gtg3vv)
//CS2150 lab 6
//HashNode.cpp
#include "HashNode.h"
#include <iostream>


using namespace std;

HashNode::HashNode( ) {
  next = NULL;
  word = "";
  key = NULL;
}

HashNode::HashNode(string value, int k){
  next = NULL;
  word = value;
  key = k;
}
