//Gabriel Groover (gtg3vv) heap.h

#ifndef heap_H
#define heap_H

#include <vector>
#include <string>
#include <map>
#include "huffNode.h"
using namespace std;

class heap {
public:
    heap();
    heap(vector<HuffNode*> vec);
    ~heap();

    void insert(HuffNode* x);
    HuffNode* findMin();
    HuffNode* deleteMin();
    unsigned int size();
    void makeEmpty();
    bool isEmpty();
    void print();
    void huffTree();
    void prefixs(HuffNode *node, string prefix);
    map<char, string> prefixlist;

private:
    vector<HuffNode*> myheap;
    unsigned int heap_size;

    void percolateUp(int hole);
    void percolateDown(int hole);
};

#endif
