#include <stdio.h>

struct list_item {
  struct list_item *next;
  int datum;
} list_item_t;

struct list {
  struct list_item *head;
};


int main() {
  int n;
  printf("Enter n: ");
  scanf("%d",&n);
  int i;
  struct list *myList = (struct list*) malloc(sizeof(struct list));
  
  struct list_item *temp  = (struct list_item*) malloc(sizeof(struct list_item));
  myList->head = temp;
  struct list_item *itr  = myList->head;
  for(i = 1; i <= n; i++)
  {
    int a;
    printf("Enter value: ");
    scanf("%d", &a);
    struct list_item *new  = (struct list_item*) malloc(sizeof(struct list_item));
    new->datum = a;
    itr->next = new;
    itr=new;
  }
  
  
  temp = myList->head->next;
  while(temp->next != 0)
  {
    printf("%d\n", temp->datum);
    temp = temp->next;
  }
  printf("%d\n", temp->datum);
  free(myList);
  return 0;
  
}