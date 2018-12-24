//Gabriel Groover (gtg3vv)
// February, 02 2016 postfixCalculator.h
#include "Stack.h"
using namespace std;

class postfixCalculator {
public:
  postfixCalculator(); //default constructor
  ~postfixCalculator(); //destructor
 
  void divide();	//perform operation and return to stack
  void multiply();
  void add();
  void subtract();
  void negate();
  void pushNum(int num); //add new number to top of stack
  int popNum(); //return top element
private:
  Stack calculator;
};
  
