//Gabriel Groover (gtg3vv) huffNode.cpp
#include "huffNode.h"

HuffNode::HuffNode(int f, char c)
{
  frequency = f;
  character = c;
  left = 0;
  right = 0;
}