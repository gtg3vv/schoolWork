#include <iostream>
using namespace std;

int xton(int x,int n){
  if (n == 0)
    return 1;
  else
    return x*xton(x,n-1);
}
int main( ){
  int x,y,z;
  cin >> x;
  cin >> y;
  z = xton(x,y);
  cout << x << " ^ " << y << " = " << z << endl;
  return 0;
}
