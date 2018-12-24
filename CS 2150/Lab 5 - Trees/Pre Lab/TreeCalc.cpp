//Gabriel Groover (gtg3vv)
//TreeCalc.cpp February,29,2016

#include "TreeCalc.h"
#include <iostream>

using namespace std;

//Constructor
TreeCalc::TreeCalc() {
  mystack = stack<TreeNode*>();
}

//Destructor- frees memory
TreeCalc::~TreeCalc() {
  if(!mystack.empty())
  cleanTree(mystack.top());
}

//Deletes tree/frees memory
void TreeCalc::cleanTree(TreeNode* ptr) {
  if(ptr->left != NULL)
  {
    cleanTree(ptr->left);
    cleanTree(ptr->right);
  }
  delete ptr;
}

//Gets data from user
void TreeCalc::readInput() {
    string response;
    cout << "Enter elements one by one in postfix notation" << endl
         << "Any non-numeric or non-operator character,"
         << " e.g. #, will terminate input" << endl;
    cout << "Enter first element: ";
    cin >> response;
    //while input is legal
    while (isdigit(response[0]) || response[0]=='/' || response[0]=='*'
            || response[0]=='-' || response[0]=='+' ) {
        insert(response);
        cout << "Enter next element: ";
        cin >> response;
    }
}

//Puts value in tree stack
void TreeCalc::insert(const string& val) {
    // insert a value into the tree
  if(val == "/" || val == "*" || val == "-" || val == "+")
  {
    TreeNode *node = new TreeNode(val);
    node->right = mystack.top();
    mystack.pop();
    node->left = mystack.top();
    mystack.pop();
    mystack.push(node);
  } 
  else
  {
    mystack.push(new TreeNode(val));
  }
}

//Prints data in prefix form
void TreeCalc::printPrefix(TreeNode* ptr) const {
    // print the tree in prefix format
  cout << ptr->value << " ";
    if(ptr->left != NULL)
      printPrefix(ptr->left);
    if(ptr->right != NULL)
      printPrefix(ptr->right);
}

//Prints data in infix form
void TreeCalc::printInfix(TreeNode* ptr) const {
    // print tree in infix format with appropriate parentheses
  if(ptr != NULL)
  {
    if(ptr->left != NULL)
      cout << "(";
    printInfix(ptr->left);
    if(ptr->value == "/" || ptr->value == "*" || ptr->value == "-" || ptr->value == "+")
      cout << " " << ptr->value << " ";
    else
      cout << ptr->value;
    printInfix(ptr->right);
    if(ptr->right != NULL)
      cout << ")";
  }
}

//Prints data in postfix form
void TreeCalc::printPostfix(TreeNode* ptr) const {
    // print the tree in postfix form
  if(ptr != NULL)
  {
    printPostfix(ptr->left);
    printPostfix(ptr->right);
    cout << ptr->value << " ";
  }
}

// Prints tree in all 3 (pre,in,post) forms

void TreeCalc::printOutput() const {
    if (mystack.size()!=0 && mystack.top()!=NULL) {
        cout << "Expression tree in postfix expression: ";
        // call your implementation of printPostfix()
	printPostfix(mystack.top());
        cout << endl;
        cout << "Expression tree in infix expression: ";
        // call your implementation of printInfix()
	printInfix(mystack.top());
        cout << endl;
        cout << "Expression tree in prefix expression: ";
        // call your implementation of printPrefix()
	printPrefix(mystack.top());
        cout << endl;
    } else
        cout<< "Size is 0." << endl;
}

//Evaluates tree, returns value
// private calculate() method
int TreeCalc::calculate(TreeNode* ptr) const {
    // Traverse the tree and calculates the result
  if(ptr->left != NULL)
  {
    int lsum = calculate(ptr->left);
    int rsum = calculate(ptr->right);
    if(ptr->value == "/")
      return lsum / rsum;
    if(ptr->value == "*")
      return lsum * rsum;
    if(ptr->value == "-")
      return lsum - rsum;
    else
      return lsum + rsum;
  }
  else
    return atoi((ptr->value).c_str());
}

//Calls calculate, sets the stack back to a blank stack
// public calculate() method. Hides private data from user
int TreeCalc::calculate() {
    int i = calculate(mystack.top());
    if(!mystack.empty())
      mystack.pop();
    //int i = calculate(mystack.top());
    // call private calculate method here
    return i;
    //return i;
}
