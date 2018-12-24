//Gabriel Groover (gtg3vv) huffNode.h
#ifndef HUFFNODE_H
#define HUFFNODE_H

#include <vector>
#include <string>
using namespace std;

class HuffNode {
public:
    HuffNode(int f,char c);
    unsigned int frequency;
    char character;
    HuffNode *left,*right;
    
};

#endif
 
