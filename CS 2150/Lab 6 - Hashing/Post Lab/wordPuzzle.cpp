//Gabriel Groover (gtg3vv)
//CS2150 lab 6
//wordPuzzle.cpp

//big theta time = rows*colums*number of words in dict

#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include "hashTable.h"
#include <stdlib.h>
#include <sstream>
#include <set>
#include "timer.h"
// We create a 2-D array of some big size, and assume that the table
// read in will be less than this size (a valid assumption for lab 6)
#define MAXROWS 500
#define MAXCOLS 500
char table[MAXROWS][MAXCOLS];

// Forward declarations
bool readInTable (string filename, int &rows, int &cols);
char* getWordInTable (int startRow, int startCol, int dir, int len,
                      int numRows, int numCols);

using namespace std;
bool checkprime(unsigned int p);
int getNextPrime (unsigned int n);
int hash(string s,int size);


int main(int argc , char **argv){
  
  ifstream words(argv[1]);
  ifstream count(argv[1]);
  HashTable myhash;
  int numwords = 0,maxlength = 0;
  string line;
  timer t;
  vector<string> wordsfound;
  
  if (words.is_open())
  {
    while ( getline (words,line) )
      numwords++;
  }
  words.close();
  int hsize = checkprime(numwords / .5) ? (numwords / .5) : getNextPrime(numwords / .5);
  myhash = HashTable(hsize);
  
  while ( getline (count,line) )
  {
    if(line.size() > maxlength)
      maxlength = line.size();
      HashNode *temp = new HashNode(line,hash(line,hsize));
      myhash.insert(temp);
      //cout << line << '\n';
   }
   count.close();
  
   int rows,cols,numfound = 0;
   set<string> found;
   t.start();
   readInTable (argv[2], rows, cols);
   for (int i = 0; i < rows; i++)
     for (int j = 0; j < cols; j++)
       for (int k = 0; k < 8; k++)
       {
	 found.clear();
	 for (int l = 3; l <= maxlength; l++)
	 {
	   string str = string(getWordInTable (i, j, k, l,
                      rows, cols));
	   string lines = "";
	   if(str.size() >= 3)
	   {
	   
	   if(found.count(str) == 0 && myhash.find(hash(str,hsize),str))
	     
	   {
	     found.insert(str);
	     numfound++;
	     //cout << i << " " << j << " " << k << " " << l << endl;
	     switch (k) { // assumes table[0][0] is in the upper-left
            case 0:
                lines += "N (";
                break; // north
            case 1:
                lines += "NE (";
                break; // north-east
            case 2:
                lines += "E (";
                break; // east
            case 3:
                lines += "SE (";
                break; // south-east
            case 4:
                lines += "S (";
                break; // south
            case 5:
                lines += "SW (";
                break; // south-west
            case 6:
                lines += "W (";
                break; // west
            case 7:
                lines += "NW (";
                break; // north-west
	      }
	      //cout << i << ", " << j << "):	" <<  str << endl;
	      ostringstream ss;
	      ss << i;
	      lines += ss.str();
	      ss.str("");
	      lines += ", ";
	      ss << j;
	      lines += ss.str();
	      lines += "):  ";
	      lines += str;
	      wordsfound.push_back(lines);
	   }
	     
	  }
	     
	 }
       }
	  
   t.stop();
   for(int i = 0; i < wordsfound.size(); i ++)
     cout << wordsfound[i] << endl;
   
   cout << numfound << " words found" << endl;
  //cout << "Found all words in " << t.getTime() << " seconds." << endl;
  cout << (int) (t.getTime() * 1000) << endl;
  
  return 0;
}
bool readInTable (string filename, int &rows, int &cols) {
    // a C++ string to hold the line of data that is read in
    string line;
    // set up the file stream to read in the file (takes in a C-style
    // char* string, not a C++ string object)
    ifstream file(filename.c_str());
    // upon an error, return false
    if ( !file.is_open() )
        return false;
    // the first line is the number of rows: read it in
    file >> rows;
    //cout << "There are " << rows << " rows." << endl;
    getline (file,line); // eats up the return at the end of the line
    // the second line is the number of cols: read it in and parse it
    file >> cols;
    //cout << "There are " << cols << " cols." << endl;
    getline (file,line); // eats up the return at the end of the line
    // the third and last line is the data: read it in
    getline (file,line);
    // close the file
    file.close();
    // convert the string read in to the 2-D grid format into the
    // table[][] array.  In the process, we'll print the table to the
    // screen as well.
    int pos = 0; // the current position in the input data
    for ( int r = 0; r < rows; r++ ) {
        for ( int c = 0; c < cols; c++ ) {
            table[r][c] = line[pos++];
            //cout << table[r][c];
        }
        //cout << endl;
    }
    // return success!
    return true;
}
char* getWordInTable (int startRow, int startCol, int dir, int len,
                      int numRows, int numCols) {
    // the static-ness of this variable prevents it from being
    // re-declared upon each function invocataion.  It also prevents it
    // from being deallocated between invocations.  It's probably not
    // good programming practice, but it's an efficient means to return
    // a value.
    static char output[256];
    // make sure the length is not greater than the array size.
    if ( len >= 255 )
        len = 255;
    // the position in the output array, the current row, and the
    // current column
    int pos = 0, r = startRow, c = startCol;
    // iterate once for each character in the output
    for ( int i = 0; i < len; i++ ) {
        // if the current row or column is out of bounds, then break
        if ( (c >= numCols) || (r >= numRows) || (r < 0) || (c < 0) )
            break;
        // set the next character in the output array to the next letter
        // in the table
        output[pos++] = table[r][c];
        // move in the direction specified by the parameter
        switch (dir) { // assumes table[0][0] is in the upper-left
            case 0:
                r--;
                break; // north
            case 1:
                r--;
                c++;
                break; // north-east
            case 2:
                c++;
                break; // east
            case 3:
                r++;
                c++;
                break; // south-east
            case 4:
                r++;
                break; // south
            case 5:
                r++;
                c--;
                break; // south-west
            case 6:
                c--;
                break; // west
            case 7:
                r--;
                c--;
                break; // north-west
        }
    }
    // set the next character to zero (end-of-string)
    output[pos] = 0;
    // return the string (a C-style char* string, not a C++ string
    // object)
    return output;
}

int hash(string s,int size){
  //return (int(s[0]) * int(s[1]) * int(s[2]) * s.size()) % size;
  const char *m = s.c_str();
  unsigned int hash = 0;
  while (*m)
    hash = 37*hash + (*m++);
  return hash%size;
  
}

bool checkprime(unsigned int p) {
    if ( p <= 1 ) // 0 and 1 are not primes; the are both special cases
        return false;
    if ( p == 2 ) // 2 is prime
        return true; 
    if ( p % 2 == 0 ) // even numbers other than 2 are not prime
        return false;
    for ( int i = 3; i*i <= p; i += 2 ) // only go up to the sqrt of p
        if ( p % i == 0 )
            return false;
    return true;
}

int getNextPrime (unsigned int n) {
    while ( !checkprime(++n) );
    return n; // all your primes are belong to us
}