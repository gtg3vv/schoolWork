#import <Foundation/NSObject.h>

@interface ListNode : NSObject
{
@public
  int value;
  ListNode* next;
}
- (id) value: (int) newvalue;
- (id) next: (id) newNode;
@end

@implementation ListNode
- (id) value: (int) newvalue
{
  value = newvalue;
  return self;
}
- (id) next: (id) newNode
{
  next = newNode;
  return self;
}
@end



int main (void) {
  int n;
  printf("Enter n: ");
  scanf("%d",&n);
  
  ListNode *myhead = [ListNode new];
  ListNode *temp = myhead;
  
  int i;
  for(i = 1; i <= n; i++)
  {
    int a;
    printf("Enter value: ");
    scanf("%d", &a);
    ListNode *newnode = [ListNode new];
    [newnode value:a];
    
    if (i == 1)
    {
      [myhead next:newnode];
      temp = myhead->next;
     }
      
    else
      {
      [temp next:newnode];
      temp = temp->next;
      }
  }
  temp = myhead->next;
  while(temp->next != NULL)
  {
    printf("%d\n", temp->value);
    myhead = temp;
    temp = temp->next;
    [myhead release];
  }
  printf("%d\n", temp->value);
  [temp release];
  
    return 0;
} 
