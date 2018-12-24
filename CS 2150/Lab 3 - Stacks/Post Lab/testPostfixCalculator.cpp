//Gabriel Groover (gtg3vv)
// February, 02 2016 testPostfixCalculator.cpp

#include <stack>
#include "postfixCalculator.h"
#include <iostream>
#include <cstdlib>
//#include <string>
//#include <cstring>
using namespace std;

int main(){

postfixCalculator p = postfixCalculator();

while(cin.good()) {
        string s;
        cin >> s;
        if(s == "") {
            break;
        }
        if(s == "+")
	  p.add();
	else if(s == "-")
	  p.subtract();
	else if(s == "/")
	  p.divide();
	else if(s == "~")
	  p.negate();
	else if(s == "*")
	  p.multiply();
        
	else p.pushNum(atoi(s.c_str()));
        //cout << s << endl;
    }

cout << "Result is: " << p.popNum() << endl;
return 0;

}
