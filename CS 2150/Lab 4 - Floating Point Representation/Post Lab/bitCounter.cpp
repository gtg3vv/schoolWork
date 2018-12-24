//Gabriel Groover (gtg3vv)
// 2/18/2016 bitCounter.cpp
#include <iostream>
#include <stdlib.h>

using namespace std;

unsigned int bit(unsigned int num){
  if (num == 1)
    return 1;
  return bit(num >> 1) + (num % 2);
}

int main(int argc , char **argv){
  cout << bit(atoi(argv[1])) << endl;
  return 0;
}
