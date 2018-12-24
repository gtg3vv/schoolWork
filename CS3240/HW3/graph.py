#Gabriel Groover (gtg3vv)
__author__ ='gtg3vv'
'''
Graph class
Accepts dictionary as adjacency list in constructor
get_adjList  - get adjacency list for single node
is_adjacent  - check if two nodes are adjacent
num_nodes    - count nodes in graph
add_node     - add node to graph
link_nodes   - make two nodes  adjacent
unlink_nodes - disconnect two nodes
del_node     - remove node  from graph
'''

class Graph:
    '''Constructor that  accepts dictionary adjacency list'''
    def __init__(self, adjList = {}):
        self.adjList = adjList
        
    '''Get adjacecncy list for single node'''    
    def get_adjList(self, node):
        if node not in self.adjList:
            return None
        
        return self.adjList[node]
        
    '''Check if two nodes are adjacent'''    
    def is_adjacent(self, node1, node2):
        if node1 not in self.adjList:
            return None
        
        if node2 in self.adjList[node1]:
            return True
        else: 
            return False
            
    '''Count unique nodes in graph'''        
    def num_nodes(self):
        return len(self.adjList.keys())
      
    '''Return formatted string for graph'''    
    def __str__(self):
        return str(self.adjList)
    
    '''Return iterator to underlying dictionary'''
    def __iter__(self):
        return iter(self.adjList.keys())
    
    '''Return length of adjacency list'''
    def __len__(self):
        return self.num_nodes()
    
    '''Check if node in graph'''
    def __contains__(self,node):
        return node in self.adjList
        
    '''Add node to graph'''    
    def add_node(self, node):
        if node in self.adjList:
            return False
        self.adjList[node] = []
        return True
    
    '''Connect two nodes'''
    def link_nodes(self, node1, node2):
        if node2 in self.adjList[node1]:
            return False
        self.adjList[node1].append(node2)
        self.adjList[node2].append(node1)
        return True
    
    '''Disconnect two nodes'''
    def unlink_nodes(self, node1, node2):
        if node2 not in self.adjList[node1]:
            return False
        
        self.adjList[node1].remove(node2)
        self.adjList[node2].remove(node1)
        
        return True
    
    '''Remove node  from graph'''    
    def del_node(self, node):
        if node not in self.adjList:
            return False
        
        for n in self.adjList:
            if node in self.adjList[n]:
                self.adjList[n].remove(node)
            
        self.adjList.pop(node, None)
        return True
        
if __name__ == "__main__":
    g = Graph({ 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] })
    
    print(g)
    print(g.num_nodes())
    print(len(g))
    print(g.get_adjList('B'))
    print(g.is_adjacent('A','B'))
    print(g.is_adjacent('A','C'))
    print('z' in g)
    g.add_node('Z')
    g.unlink_nodes('A','B')
    g.link_nodes('Z','A')
    print(g)
    g.del_node('B')
    print(g)
        
    
    
                
        
    
        
    