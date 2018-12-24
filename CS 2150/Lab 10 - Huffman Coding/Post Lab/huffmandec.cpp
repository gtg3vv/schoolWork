 //Gabriel Groover (gtg3vv)
 //inlab

#include <iostream>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include "huffNode.h"
using namespace std;

// main(): we want to use parameters
int main (int argc, char **argv) {
    // verify the correct number of parameters
    if ( argc != 2 ) {
        cout << "Must supply the input file name as the only parameter" << endl;
        exit(1);
    }
    // attempt to open the supplied file; must be opened in binary
    // mode, as otherwise whitespace is discarded
    ifstream file(argv[1], ifstream::binary);
    // report any problems opening the file and then exit
    if ( !file.is_open() ) {
        cout << "Unable to open file '" << argv[1] << "'." << endl;
        exit(2);
    }
    HuffNode *root = new HuffNode(1,'3');
    HuffNode *temp = new HuffNode(1,'3');
    root->right=temp;
    // read in the first section of the file: the prefix codes
    while ( true ) {
        string character, prefix;
        // read in the first token on the line
        file >> character;
        // did we hit the separator?
        if ( (character[0] == '-') && (character.length() > 1) )
            break;
        // check for space
        if ( character == "space" )
            character = " ";
        // read in the prefix code
        file >> prefix;
        // do something with the prefix code]
	//char c;
	temp = root->right;
	for (int i = 0; i < prefix.length(); i++)
	{
	  
	  if(prefix[i] == '1')
	  {
	    if(temp->right == NULL)
	    {
	      temp->right=new HuffNode(1,character[0]);
	      temp = temp->right;
	    }
	    else
	      temp = temp->right;
	  }
	  if(prefix[i] == '0')
	  {
	    if(temp->left == NULL)
	    {
	      temp->left=new HuffNode(1,character[0]);
	      temp = temp->left;
	    }
	    else
	      temp = temp->left;
	  }
	}
        cout << character << " "
             << prefix << endl;
    }
    // read in the second section of the file: the encoded message
    stringstream sstm;
    while ( true ) {
        string bits;
        // read in the next set of 1's and 0's
        file >> bits;
        // check for the separator
        if ( bits[0] == '-' )
            break;
        // add it to the stringstream
        sstm << bits;
    }
    string allbits = sstm.str();
    // at this point, all the bits are in the 'allbits' string
    cout << "----------------------------------------" << endl;
    temp=root->right;
    for (int i = 0; i < allbits.length(); i++)
	{
	  if(allbits[i] == '1' && temp->right != NULL)
	  {
	    temp = temp->right;
	  }
	  else if (allbits[i] == '1' && temp->right == NULL)
	  {
	    cout << temp->character;
	    temp = root->right->right;
	  }
	  else if(allbits[i] == '0' && temp->left != NULL)
	  {
	    temp = temp->left;
	  }
	  else if (allbits[i] == '0' && temp->left == NULL)
	  {
	    cout << temp->character;
	    temp = root->right->left;
	  }
	  
	}
	cout << temp->character << endl;
    //cout << endl << "All the bits: " << allbits << endl;
    // close the file before exiting
    file.close();
}