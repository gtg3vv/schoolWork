//Gabriel Groover (gtg3vv)
//CS2150 lab 6
//hastTable.h
#ifndef HASHTABLE_H
#define HASHTABLE_H

#include <iostream>
#include <vector>
#include "HashNode.h"
using namespace std;



class HashTable {
public:
    HashTable();				//Constructor
    HashTable(int size);
    //~HashTable();//Destructor
    void insert(HashNode *node);
    string getValue(int key);
    bool find(int key,string s);

private:
    vector<HashNode*> nodes;
};

#endif
