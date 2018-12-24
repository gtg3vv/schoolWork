#include <iostream>
#include "List.h"


List::List( ) {
  count = 0;
  head = new ListNode();
  tail = new ListNode();
  (*head).next = tail;
  (*tail).previous = head;
}
List::List(const List& source) {      // Copy Constructor
    head=new ListNode;
    tail=new ListNode;
    head->next=tail;
    tail->previous=head;
    count=0;
    ListItr iter(source.head->next);
    while (!iter.isPastEnd()) {       // deep copy of the list
        insertAtTail(iter.retrieve());
        iter.moveForward();
    }
}

List& List::operator=(const List& source) { //Equals operator
    if (this == &source)
        return *this;
    else {
        makeEmpty();
        ListItr iter(source.head->next);
        while (!iter.isPastEnd()) {
            insertAtTail(iter.retrieve());
            iter.moveForward();
        }
    }
    return *this;
}

List::~List( ) {
  // makeEmpty();
  // delete head;
  // delete tail;
}

bool List::isEmpty( ) const {
  if ( count == 0 ) 
    return true;
  else
    return false;
}

void List::makeEmpty( ) {
  ListItr itr = ListItr(head);
  itr.moveForward();
  for(int a = 0; a < count; a++)
    {
      itr.moveForward();
      delete  itr.current->previous;
    }
  head->next = tail;
  tail->previous = head;
}

ListItr List::first( ) {
  ListItr first = ListItr( (*head).next );
  return first;
	
}

ListItr List::last( ) {
  ListItr last = ListItr( (*tail).previous );
  return last;
}

void List::insertAfter( int x, ListItr position) {
  ListNode node = ListNode();
  node.value = x;
  node.next = position.current->next;
  node.previous = position.current;
  count++;

}

void List::insertBefore( int x, ListItr position) {
  ListNode node = ListNode();
  node.value = x;
  node.next = position.current;
  node.previous = position.current->previous;
  count++;

}

void List::insertAtTail( int x) {
  ListNode node = ListNode();
  node.value = x;
  node.next = tail;
  node.previous = (*tail).previous;
  (*(*tail).previous) = node;
  count++;


}

void List::remove( int x ) {
  ListItr itr = find(x);
  if(itr.current != tail){
 
  itr.current->previous->next = itr.current->next;
  itr.current->next->previous = itr.current->previous;
  }
  delete itr.current;
  
}

ListItr List::find( int x ) {
  ListItr itr = ListItr(head);
  for(int a = 0; a < count; a++)
    {
      if(itr.current->value == x)
	return itr;
      itr.moveForward();
    }
  itr.moveForward();
  return itr;

}

int List::size( ) const {
  return count;
}
