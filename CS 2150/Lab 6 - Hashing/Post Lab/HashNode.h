//Gabriel Groover (gtg3vv)
//CS2150 lab 6
//HashNode.h
#ifndef HASHNODE_H
#define HASHNODE_H

#include <iostream>
#include <string>


using namespace std;
class HashTable;
class HashNode {
public:
    HashNode();                 // Constructor
    HashNode(string value, int k);

private:
    int key;
    string word;
    HashNode *next;
    friend class HashTable;
    
};

#endif
