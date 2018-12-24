//Gabriel Groover (gtg3vv)
// February, 4th 2016 ListItr.cpp

#include <iostream>
#include "ListItr.h"


using namespace std;

void printList(List& theList, bool forward)
{
  if(forward){
	ListItr fwd = theList.first();
	for(int i = 0; i < theList.size(); i++)
	{	
	cout << fwd.retrieve() << endl;
	fwd.moveForward();
	}
}
  else{
	ListItr bkwd = theList.last();
	for(int i = 0; i < theList.size(); i++)
	{	
	cout << bkwd.retrieve() << endl;
	bkwd.moveBackward();
      }
}

  
}

ListItr::ListItr( ) {
  current = NULL;

}
ListItr::ListItr( ListNode* theNode) {
  current = theNode;
}

bool ListItr::isPastEnd( ) const {
  if ((*current).next == NULL ) 
    return true;
  else 
    return false;
}

bool ListItr::isPastBeginning() const {
  if ((*current).previous == NULL ) 
    return true;
  else return false;
}

void ListItr::moveForward( ) {
  if(!isPastEnd())    
	current = current->next;
  }

void ListItr::moveBackward( ) {
  if(!isPastBeginning())
    current = (*current).previous;
}

int ListItr::retrieve( ) const {
  return current->value;
}
