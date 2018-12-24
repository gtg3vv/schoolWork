//Gabriel Groover (gtg3vv) heap.cpp

#include <iostream>
#include <string>
#include "heap.h"
#include "huffNode.h"
using namespace std;

// default constructor
heap::heap() : heap_size(0) {
   myheap.push_back(new HuffNode(0,';'));
}

// builds a heap from an unsorted vector
heap::heap(vector<HuffNode*> vec) : heap_size(vec.size()) {
    myheap = vec;
    myheap.push_back(myheap[0]);
    myheap[0] = 0;
    for ( int i = heap_size/2; i > 0; i-- )
        percolateDown(i);
}

// the destructor doesn't need to do much
heap::~heap() {
}

void heap::insert(HuffNode *h) {
    // a vector push_back will resize as necessary
    myheap.push_back(h);
    //cout << h->character << h->frequency;
    // move it up into the right position
    if (heap_size != 0)
    percolateUp(++heap_size);
    else
      heap_size++;
}

void heap::percolateUp(int hole) {
    // get the value just inserted
    HuffNode *x = myheap[hole];
    // while we haven't run off the top and while the
    // value is less than the parent...
    for ( ; (hole > 1) && (x->frequency < myheap[hole/2]->frequency); hole /= 2 )
        myheap[hole] = myheap[hole/2]; // move the parent down
    // correct position found!  insert at that spot
    myheap[hole] = x;
}

HuffNode* heap::deleteMin() {
    // make sure the heap is not empty
    if ( heap_size == 0 )
        throw "deleteMin() called on empty heap";
    // save the value to be returned
    HuffNode* ret = myheap[1];
    // move the last inserted position into the root
    myheap[1] = myheap[heap_size--];
    // make sure the vector knows that there is one less element
    myheap.pop_back();
    // percolate the root down to the proper position
    percolateDown(1);
    // return the old root node
    return ret;
}

void heap::percolateDown(int hole) {
    // get the value to percolate down
    HuffNode* x = myheap[hole];
    // while there is a left child...
    while ( hole*2 <= heap_size ) {
        int child = hole*2; // the left child
        // is there a right child?  if so, is it lesser?
        if ( (child+1 <= heap_size) && (myheap[child+1]->frequency < myheap[child]->frequency) )
            child++;
        // if the child is greater than the node...
        if ( x->frequency > myheap[child]->frequency ) {
            myheap[hole] = myheap[child]; // move child up
            hole = child;             // move hole down
        } else
            break;
    }
    // correct position found!  insert at that spot
    myheap[hole] = x;
}

HuffNode* heap::findMin() {
    if ( heap_size == 0 )
        throw "findMin() called on empty heap";
    return myheap[1];
}

unsigned int heap::size() {
    return heap_size;
}

void heap::makeEmpty() {
    heap_size = 0;
}

bool heap::isEmpty() {
    return !heap_size;
}

void heap::huffTree()
{
  while(heap_size >=2)
  {
    HuffNode *newNode = new HuffNode(1,'0');
    newNode->left=findMin();
    deleteMin();
    newNode->right=findMin();
    deleteMin();
    newNode->frequency=newNode->left->frequency + newNode->right->frequency;
    insert(newNode);
  }
}

void heap::prefixs(HuffNode *node, string prefix)
{
  if (!(node->left || node->right))
  {
    if (node->character == ' ')
    {
      cout << "space" << " " << prefix << endl;
      prefixlist[' '] = prefix;
    }
 
    else
    {
      cout << node->character << " " << prefix << endl;
      prefixlist[node->character] = prefix;
    }
  }
  if (node->left)
    prefixs(node->left,prefix+"0");
  if (node->right)
    prefixs(node->right,prefix+"1");
}
