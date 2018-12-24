//Gabriel Groover (gtg3vv)
// 2/16/16 inlab4.cpp


#include <iostream>
#include <climits>
#include <cfloat> 
using namespace std;

int main(){
  cout << sizeof(double*) << endl;
  cout << "int " << INT_MAX << endl;
  cout << "unsigned int" << UINT_MAX << endl;
  cout << " float " << FLT_MAX << endl;
  cout << "double " << DBL_MAX << endl;
  cout << "char " << CHAR_MAX << endl;
  int a = 1.0;
  unsigned int b = 17.0;
  float c = 1.0;
  double d = 1.0;
  char e = '1';
  bool f = true;
  int* g = NULL;
  char* h = NULL;
  double* i = NULL;
  
  cout << a << endl;
  cout << b << endl;
  cout << c << endl;
  cout << d << endl;
  cout << e << endl;
  cout << f << endl;
  cout << g << endl;
  cout << h << endl;
  cout << i << endl;

  cout << endl;
//primitive arrays
  
  int IntArray[10];
char CharArray[10];
for (int i = 0; i < 10; i++)
{
    IntArray[i] = 1;
    CharArray[i] = 1;
    
}
  int IntArray2D[6][5];
char CharArray2D[6][5];
for (int i = 0; i < 10; i++)
{
  for(int j = 0; j < 10; j++)
  {
    IntArray2D[i][j] = 1;
    CharArray2D[i][j] = 1;
    
  }}

cout <<endl;
}
