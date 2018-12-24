//Gabriel Groover (gtg3vv)
// February, 02 2016 postfixCalculator.cpp
#include "postfixCalculator.h"
#include <stack>

postfixCalculator::postfixCalculator(){
calculator = Stack();
}

postfixCalculator::~postfixCalculator(){
}

void postfixCalculator::pushNum(int num){
calculator.push(num);
}

int postfixCalculator::popNum(){
return calculator.top();
}

void postfixCalculator::negate(){
  int temp = calculator.top();
  temp = -temp;
  calculator.pop();
  calculator.push(temp);
}

void postfixCalculator::add(){
int temp = calculator.top();
calculator.pop();
temp = temp + calculator.top();
calculator.pop();
calculator.push(temp);
}

void postfixCalculator::multiply(){
int temp = calculator.top();
calculator.pop();
temp = temp * calculator.top();
calculator.pop();
calculator.push(temp);
}

void postfixCalculator::subtract(){
int temp = calculator.top();
calculator.pop();
temp = calculator.top() - temp;
calculator.pop();
calculator.push(temp);
}

void postfixCalculator::divide(){
int temp = calculator.top();
calculator.pop();
temp = calculator.top() / temp;
calculator.pop();
calculator.push(temp);
}
