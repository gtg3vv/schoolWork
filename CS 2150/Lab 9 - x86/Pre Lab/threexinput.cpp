 
// threexinput.cpp
//Gabriel Groover gtg3vv
//4/11/16

#include <iostream>
#include "timer.h"
#include <cstdlib>

using namespace std;

extern "C" int threexplusone (int);

int  main () {
    int  x,n;
    timer t;
    
    cout << "Please enter the number x:  ";
    cin >> x;
    cout << "Please enter the number of iterations:  ";
    cin >> n;
    t.start();
    for(int i=0; i<n; i++) threexplusone(x);
    t.stop();
    
    cout << "The number of ops is " << threexplusone(x) << endl;
    cout << "The average runtime is " << t.getTime()/n << endl;
    
    
    return 0;
}
