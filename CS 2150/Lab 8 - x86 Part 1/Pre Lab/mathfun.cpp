 
// main.cpp
//Gabriel Groover gtg3vv
//3/28/16

#include <iostream>
#include <time.h>
#include <cstdlib>

using namespace std;

extern "C" int product (int, int);
extern "C" int power (int, int);

int  main () {
    int  n1,n2,p;
    cout << "Please enter n1:  ";
    cin >> n1;
    cout << "Please enter n2:  ";
    cin >> n2;


    // find the product
    p = product(n1, n2);
    cout << "The product is " << p << endl;

    // find the product
    p = power(n1, n2);
    cout << "The power is " << p << endl;
    
    
    return 0;
}
