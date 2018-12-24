//Gabriel Groover (gtg3vv)
// February, 02 2016 testPostfixCalculator.cpp

#include <stack>
#include "postfixCalculator.h"
#include <iostream>
using namespace std;

int main(){

postfixCalculator p = postfixCalculator();
p.pushNum(3);
p.pushNum(4);
p.add();
cout << p.popNum() << endl;
p.pushNum(10);
p.subtract();
cout << p.popNum() << endl;
p.pushNum(-1);
p.divide();
p.pushNum(4);
p.multiply();
cout << p.popNum() << endl;


}
