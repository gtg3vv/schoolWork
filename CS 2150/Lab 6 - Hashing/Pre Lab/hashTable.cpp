//Gabriel Groover (gtg3vv)
//CS2150 lab 6
//hashTable.cpp
#include <iostream>
#include <vector>
#include <string>
#include "hashTable.h"

using namespace std;

HashTable::HashTable(){
  nodes = vector<HashNode*> (500);
  
}
HashTable::HashTable(int size)
{
  nodes = vector<HashNode*> (size);
}
string HashTable::getValue(int key)
{
  if(nodes[key] != NULL)
    return nodes[key]->word;
  return "";
}
bool HashTable::find(int key, string s){
  if(nodes[key] == NULL)
    return false;
  else if (nodes[key]->word == s)
    return true;
  else
  {
    HashNode *temp = nodes[key];
    while (temp->next != NULL){
      temp = temp->next;
      if(temp->word == s)
	return true;
    }
    return false;
  }
}

void HashTable::insert(HashNode *node)
{
  if(nodes[node->key] != NULL)
  {
    node->next = nodes[node->key]->next;
    nodes[node->key]->next = node;
    //cout << "collide" << endl;
  }
  else
  {
    nodes[node->key] = node;
    //cout << "success" << endl;
  }
  
}