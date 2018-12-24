#Gabriel Groover
__author__ = 'gtg3vv'

from graph import Graph

'''Checks to see if a given graph is complete
    -Raises TypeError if given invalid type
    -Does not validate the graph itself
    '''
def is_complete(grph):
    if not isinstance(grph, Graph):
        raise TypeError
    
    isConnected = True
    for node in grph:
        for n in grph:
            if n not in grph.get_adjList(node) and n != node:
                isConnected = False
    
    return isConnected

'''Returns a list of nodes in graph sorted  by degree
    - Raises TypeError if given invalid type
    - Does not validate the graph itself
    '''
def nodes_by_degree(grph):
    if not isinstance(grph, Graph):
        raise TypeError
    listDegrees = []
    
    for node in grph:
        listDegrees.append((node, len(grph.get_adjList(node))))
        
    return sorted(listDegrees, key=lambda x: x[1],reverse=True)
        