//Gabriel Groover (gtg3vv)
// 2/17/2016 prelab4.cpp

#include <iostream>

using namespace std;

void sizeOfTest(){
  cout << sizeof(int) << endl;
  cout << sizeof(unsigned int) << endl;
  cout << sizeof(float) << endl;
  cout << sizeof(double) << endl;
  cout << sizeof(char) << endl;
  cout << sizeof(bool) << endl;
  cout << sizeof(int*) << endl;
  cout << sizeof(double*) << endl;
  cout << sizeof(char*) << endl;
}
void outputBinary(unsigned int x){
  int j = 0;
  for(int i = 31; i >= 0; i--){
    if(j%4 != 0 || j == 0)
      cout << ((x >> i) & 1);
    else
      cout << " " << ((x >> i) & 1);
    j++;
  }
  cout << endl;
}
void overflow(){
 unsigned int x = -1;
 cout << (x + 1) << endl;
 cout << "The max value is all ones in binary, it adds a new bit and the rest become 0s. There isn't actually room for this new bit so the number becomes 0." << endl;
}
int main(){
  unsigned int x;
 cin >> x;
 sizeOfTest();
 outputBinary(x);
 overflow();
 return 0;
}
