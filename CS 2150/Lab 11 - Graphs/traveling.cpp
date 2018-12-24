#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <algorithm>

using namespace std;

#include "middleearth.h"

float computeDistance (MiddleEarth &me, string start, vector<string> dests);
void printRoute (string start, vector<string> dests);
/** @brief Computes the minimum path between a random set of cities
 * Randomly generates middle MiddleEarth
 * Creates Itinerary of cities to visit
 * Brute force calculates shortest path
 * 
 * 
 */
int main (int argc, char **argv) {
    // check the number of parameters
    if ( argc != 6 ) {
        cout << "Usage: " << argv[0] << " <world_height> <world_width> "
             << "<num_cities> <random_seed> <cities_to_visit>" << endl;
        exit(0);
    }
    // we'll assume the parameters are all well-formed
    int width, height, num_cities, rand_seed, cities_to_visit;
    sscanf (argv[1], "%d", &width);
    sscanf (argv[2], "%d", &height);
    sscanf (argv[3], "%d", &num_cities);
    sscanf (argv[4], "%d", &rand_seed);
    sscanf (argv[5], "%d", &cities_to_visit);
    // Create the world, and select your itinerary
    MiddleEarth me(width, height, num_cities, rand_seed);
    vector<string> dests = me.getItinerary(cities_to_visit);
    // YOUR CODE HERE
    string start = dests[0];
    dests.erase(dests.begin(),dests.begin()+1);
    sort(dests.begin(),dests.end());
    float mindistance = 1000000000.0;
    vector<string> mindests;
    while(next_permutation(dests.begin(),dests.end()))
    {
      float f = computeDistance (me, start, dests);
      if (f < mindistance)
      {
	mindistance = f;
	mindests = dests;
      }
    }
    
    cout << "Minimum path has distance " << mindistance << ": ";
    printRoute(start, mindests);
    //me.printTable();
    return 0;
}


// This method will compute the full distance of the cycle that starts
// at the 'start' parameter, goes to each of the cities in the dests
// vector IN ORDER, and ends back at the 'start' parameter.
/** @brief computes the total distance between cities in ordered itinerary
 * 
 * @param me The earth containing the given cities
 * @param start start city
 * @param dests vector containing ordered destination cities
 */
float computeDistance (MiddleEarth &me, string start, vector<string> dests) {
    // YOUR CODE HERE
  float dist = me.getDistance(start, dests[0]);
  
  for (int i = 0; i < dests.size()-1; i++)
    dist+= me.getDistance(dests[i],dests[i+1]);

  return dist + me.getDistance(dests[dests.size()-1],start);
  
  
   
}
/** @brief prints the route from start to finish
 * 
 * @param start start city
 * @param dests vector containing ordered destination cities
 */ 
// This method will print the entire route, starting and ending at the
// 'start' parameter.  The output should be of the form:
// Erebor -> Khazad-dum -> Michel Delving -> Bree -> Cirith Ungol -> Erebor
void printRoute (string start, vector<string> dests) {
    cout << start << " -> ";
    for (int i = 0; i < dests.size(); i++)
      cout << dests[i] << " -> ";
    
    cout << start << endl;
    // YOUR CODE HERE
}
