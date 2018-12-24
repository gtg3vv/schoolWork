#Gabriel Groover
"""
Class that defines a list implementation of the set ADT

add          - adds existing item to set
add_list     - adds existing  list to set
union        - returns union of self and supplied set
intersection - returns intersection of self and supplied set
defines operations for str,len,iter,+

"""

class OurSet:
    
    """Default constructor"""
    def __init__(self):
        self.contents = []
        
    """Add existing item to set"""
    def add(self, item):
        if item not in self.contents:
            self.contents.append(item)
            return True
        else:
            return False
            
    """Add existing list to set"""
    def add_list(self, list1):
        addedItem = False
        for item in list1:
            addedItem = self.add(item) or addedItem
            
        return addedItem
    
    """Return formatted string for set"""
    def __str__(self):
        return "<"+ str(",".join(str(i) for i in self.contents))+">"
     
    """Return number of  items in set"""   
    def __len__(self):
        return len(self.contents)
        
    """Add an existing set to self"""
    def __add__(self, set2):
        for item in set2:
            self.add(item)
        return self
    
    """Return iterator to underlying list  object"""
    def __iter__(self):
        return iter(self.contents)
        
    """Return union of self and supplied set"""
    def union(self, set2):
        return OurSet() + self + set2
    
    """Return intersection of self  and  supplied set"""
    def intersection(self,set2):
        interSet = OurSet()
        
        for item in self.contents:
            if item in set2:
                interSet.add(item)
                
        return interSet

if __name__ == '__main__': 
    set1 = OurSet()
    set2 = OurSet()
    set3 = OurSet()
    
    set1.add(1)
    set1.add(3)
    set1.add(2)
    
    print(set2.add_list([1,5,7,2,8,3,5,2,3]))
    print(set2.add_list([1,5,7,2,8,3,5,2,3]))
            
    print(set1.union(set2))
    print(set2.union(set1))
    
    print(len(set1.intersection(set2)))
    print(set1.intersection(set1))
    print(set2.intersection(set1))
    
    print(set1.union(set3))
    print(len(set2.intersection(set3)))