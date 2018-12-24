#include <iostream>
#include <vector>
#include <queue>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <string>

using namespace std;
/** @brief Class to contain each vertex and adjacency list
 * @author Gabriel Groover (gtg3vv)
 * @date 4.25.2016
 * 
 * @public
 */

class vertex {
  public:
    vertex(string num);
    vector<vertex*> nodes;
    int indegree;
    string coursenum;    
};

vertex::vertex(string num){
  coursenum = num;
  indegree = 0;
}

/** @brief main method to carry out sort
 * @param argc number of arguments
 * @param **argv character array of file namespace
 * 
 * First reads in each line of the file
 * Constructs graph from vertices and adjacency lists
 * Sorts using queue and vertices of indegree 0
 * Prints out sorted classes.
 * @return 0 to exit normally
 * 
 */

int main (int argc, char **argv) {
    if ( argc != 2 ) {
        cout << "Must supply the input file name as the only parameter" << endl;
        exit(1);
    }
    ifstream file(argv[1], ifstream::binary);
  
    if ( !file.is_open() ) {
        cout << "Unable to open file '" << argv[1] << "'." << endl;
        exit(2);
    }
    
    vector<vertex*> myGraph;
    myGraph.clear();
    
    
    while(true){
      string v1, v2;
        file >> v1;
	file >> v2;
	bool newvert = true, newadj = true;
	if (v2 == "0" && v2 == "0")
	  break;
	
	for (int i=0; i< myGraph.size(); i++)
	{
	  if (myGraph[i]->coursenum == v1)
	    newvert = false;
	  if (myGraph[i]->coursenum == v2)
	    newadj = false;
	  
	  for (int j = 0; j < myGraph[i]->nodes.size(); j++)
	  {
	      if (myGraph[j]->coursenum == v2)
		newadj = false;
	      if (myGraph[j]->coursenum == v1)
		newvert = false;
	  }
	  
	}
	
	if (newvert)
	  myGraph.push_back(new vertex(v1));
	if (newadj)
	  myGraph.push_back(new vertex(v2));
	
	for (int i=0; i< myGraph.size(); i++)
	{
	  if(myGraph[i]->coursenum == v1)
	  {
	     for (int j = 0; j < myGraph.size(); j++)
	      {
		if (myGraph[j]->coursenum == v2)
		{
		   myGraph[i]->nodes.push_back(myGraph[j]);
		   myGraph[j]->indegree++;
		}
	      }
	  }
	}
    }
    queue<vertex*> topo;
    vertex *v;
    for (int i=0; i< myGraph.size(); i++)
    {
      if(myGraph[i]->indegree == 0)
	topo.push(myGraph[i]);
    }
    while (topo.size() != 0)
   {
      v = topo.front();
      topo.pop();
      cout << v->coursenum << " ";
      for (int i = 0; i < v->nodes.size(); i++)
      {
	v->nodes[i]->indegree--;
	if(v->nodes[i]->indegree == 0)
	  topo.push(v->nodes[i]);
      }
    }
    cout << endl;
    return 0;
}
     
     
    