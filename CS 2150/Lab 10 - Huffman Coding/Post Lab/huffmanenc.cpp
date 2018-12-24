//Gabriel Groover (gtg3vv) huffmanenc.cpp
// included so we can use cout
#include <iostream>
// stdlib.h is where exit() lives
#include <stdlib.h>
#include <string>

using namespace std;

// include the standard I/O library
#include <stdio.h>
#include <map>
#include "heap.h"
#include "huffNode.h"

// we want to use parameters
int main (int argc, char **argv) {
    // verify the correct number of parameters
    if ( argc != 2 ) {
        cout << "Must supply the input file name as the one and only parameter" << endl;
        exit(1);
    }
    map<char, int> characters;
    heap myheap;
    int symbols=0,unique=0,compressed=0;
    //float cost = 0.0;
    
    // attempt to open the supplied file.  FILE is a type desgined to
    // hold file pointers.  The first parameter to fopen() is the
    // filename.  The second parameter is the mode -- "r" means it
    // will read from the file.
    FILE *fp = fopen(argv[1], "r");
    // if the file wasn't found, output and error message and exit
    if ( fp == NULL ) {
        cout << "File '" << argv[1] << "' does not exist!" << endl;
        exit(2);
    }
    // read in each character, one by one.  Note that the fgetc() will
    // read in a single character from a file, and returns EOF when it
    // reaches the end of a file.
    char g;
    while ( (g = fgetc(fp)) != EOF )
    {
        //cout << g;
	if(g != '\t' && g != '\n')
	{
	if (characters.count(g) > 0)
	{
	  characters[g]++;
	  symbols++;
	}
	else
	{
	  characters[g]=1;
	  symbols++;
	  unique++;
	}
	//cout << " " << characters[g] << endl;
	}
    }	
    for (map<char,int>::iterator it=characters.begin(); it!=characters.end(); it++)
    {
      myheap.insert(new HuffNode(it->second,it->first));
    }
   

    // rewinds the file pointer, so that it starts reading the file
    // again from the begnning
    rewind(fp);
    // read the file again, and print to the screen
    //heap.print();
    myheap.huffTree();
    myheap.prefixs(myheap.findMin(),"");
   // a nice pretty separator
    cout << "----------------------------------------" << endl;
    while ( (g = fgetc(fp)) != EOF )
    {
      cout << myheap.prefixlist[g] << " ";
      compressed += myheap.prefixlist[g].length();
      //cost += (float) characters[g]/(float) symbols * heap.prefixlist[g].length();
      
    }
    cout << endl << "----------------------------------------" << endl; 
    cout << "There are a total of " << symbols << " symbols that are encoded." << endl;
    cout << "There are " << unique << " distinct symbols used. " << endl;
    cout << "There were " << symbols*8 << " bits in the original file." << endl;
    cout << "There were " << compressed << " bits in the compressed file." << endl;
    cout << "This gives a compression ratio of " <<  symbols*8.0/compressed << "." << endl;
    cout << "The cost of the Huffman tree is " << (float) compressed/symbols << " bits per character." << endl;
    //heap.print();
    // close the file
    fclose(fp);
}

