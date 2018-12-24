#Gabriel Groover
__author__ = 'gtg3vv'
import unittest
from graph import Graph

'''Test class for graph functions'''
class TestGraph(unittest.TestCase):
    
    '''Initialize some variables to help testing'''
    def setUp(self):
        self.emptyGraph = Graph()
        self.fullGraph = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        
    '''Test g1 - get filled adjacency list from graph'''
    def testg1_adjList_full(self):
        self.assertEqual(self.fullGraph.get_adjList('A'), ['B','D'],"G1")
    
    '''Test g2 - get empty adjacency list from graph'''
    def testg2_adjList_empty(self):
        self.assertEqual(self.fullGraph.get_adjList('E'), [], "G2")
    
    '''Test g3 - get adjacency list that is not in graph'''   
    def testg3_adjList_none(self):
        self.assertEqual(self.emptyGraph.get_adjList('E'), None, "G3")
    
    '''Test g4 - test adjacency for basic pairs that are/aren't adjacent'''    
    def testg4_adj_basic(self):
        self.assertTrue(self.fullGraph.is_adjacent('A','B'), "G4")
        self.assertFalse(self.fullGraph.is_adjacent('A','C'), "G4")
    
    '''Test g5 - test adjacency for one node that hass no neighbors'''
    def testg5_adj_empty(self):
        self.assertFalse(self.fullGraph.is_adjacent('E','A'), "G5")
       
    '''Test g6 - test adjacency for node not in graph'''    
    def testg6_adj_none(self):
        self.assertEqual(self.emptyGraph.is_adjacent('A','B'), None, "G6")
    
    '''Test g7 - test num nodes in graph for filled graph'''    
    def testg7_numNodes_basic(self):
        self.assertEqual(self.fullGraph.num_nodes(), 5, "G7")
        self.assertEqual(self.fullGraph.num_nodes(), len(self.fullGraph), "G7")
    
    '''Test g8 - test num nodes  for empty graph'''
    def testg8_numNodes_empty(self):
        self.assertEqual(self.emptyGraph.num_nodes(), 0, "G8")
        self.assertEqual(self.emptyGraph.num_nodes(), len(self.emptyGraph),"G8")
      
    '''Test g9 - add node to filled  graph'''   
    def testg9_addNode_full(self):
        g = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        self.assertTrue(g.add_node('F'), "G9")
        self.assertTrue('F' in g, "G9")
        self.assertEqual(len(g), 6, "G9")
        self.assertEqual(g.get_adjList('F'), [], "G9")
    
    '''Test g10 - add repeat node to graph'''
    def testg10_addNode_false(self):
        self.assertFalse(self.fullGraph.add_node('A'), "G10")
        self.assertEqual(len(self.fullGraph), 5, "G10")
    
    '''Test g11 - add node to empty graph'''
    def testg11_addNode_empty(self):
        g = Graph({})
        self.assertTrue(g.add_node('A'), "G11")
        self.assertEqual(len(g), 1, "G11")
        
    '''Test g12 - contains for basic nodes that are/aren't in graph'''
    def testg12_contains_basic(self):
        self.assertTrue('A' in self.fullGraph,"G12")
        self.assertFalse('Z' in self.fullGraph,"G12")
        self.assertFalse('A' in self.emptyGraph, "G12")
        
    '''Test g13 - test link nodes for two nodes that are/aren't adjacent'''    
    def testg13_linkNodes_basic(self):
        g = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        self.assertTrue(g.link_nodes('A','C'), "G13")
        self.assertTrue(g.is_adjacent('A','C'), "G13")
        self.assertFalse(g.link_nodes('A','B'), "G13")
     
    '''Test g14 - unlink nodes for two nodes that are/aren't adjacent'''    
    def testg14_unlinkNodes_basic(self):
        g = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        self.assertTrue(g.unlink_nodes('A','B'),"G14")
        self.assertFalse(g.is_adjacent('A','B'),"G14")
        self.assertFalse(g.unlink_nodes('A','B'),"G14")
    
    '''Test g15 - delete node for node that is in graph'''    
    def testg15_delNode_true(self):
        g = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        self.assertTrue(g.del_node('A'),"G15")
        self.assertEqual(len(g), 4,'G15')
        self.assertFalse('A' in g,"G15")
    
    '''Test g16 - delete node not in graph'''    
    def testg16_delNode_false(self):
        g = Graph( { 'A': ['B', 'D'], 'B': ['A', 'D', 'C'], 'C': ['B'], 'D': ['A', 'B'], 'E' : [] } )
        self.assertFalse(g.del_node('Z'),"G16")
        self.assertEqual(len(g),5,"G16")
    
    '''Test g17 - delete node from empty graph'''
    def testg17_delNode_empty(self):
        self.assertFalse(self.emptyGraph.del_node('A'),"G17")
        self.assertEqual(len(self.emptyGraph), 0, "g17")
        
    

if __name__ == '__main__':
    unittest.main()
    