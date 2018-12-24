#Gabriel Groover
__author__ = 'gtg3vv'

import unittest
from graph import Graph
import graph_functions as gf

'''Class to test graph_functions'''
class TestGraph(unittest.TestCase):
    
    '''Set up variables too help testing'''
    def setUp(self):
        self.complete = Graph({'1' : ['2','3'], '2' : ['1','3'], '3' : ['2','1']})
        self.empty = Graph({})
        self.disconnected = Graph({'1' : [], '2': [], '3' : []})
    
    '''Test g18 - test complete on complete graph'''    
    def testg18_isComplete_true(self):
        self.assertTrue(gf.is_complete(self.complete),"G18")
        self.assertTrue(gf.is_complete(self.empty),"G18")
    
    '''Test g19 test complete on non complete graph'''    
    def testg19_isComplete_false(self):
        self.assertFalse(gf.is_complete(self.disconnected),"G19")
        
    '''Test g20 - test complete on invalid type'''    
    def testg20_isComplete_type(self):
        with self.assertRaises(TypeError):
            gf.is_complete('A')
    
    '''Test g21 - test degrees on full graph'''        
    def testg21_nodesByDegree_full(self):
        self.assertEqual(gf.nodes_by_degree(self.complete)[0], ('1',2),"G21")
        self.assertEqual(gf.nodes_by_degree(self.complete)[1], ('3',2),"G21")
        self.assertEqual(gf.nodes_by_degree(self.complete)[2], ('2',2), "G21")
    
    '''Test g22 - test degrees  on empty graph'''    
    def testg22_nodesByDegree_empty(self):
        self.assertEqual(gf.nodes_by_degree(self.empty), [], "G22")
     
    '''Test g23 - test degrees on graph to check ordering'''
    def testg23_nodesByDegree_order(self):
        g = Graph({'1' : ['2','3','4'], '2':['1','3'], '3':['2'], '4':[]})
        self.assertEqual(gf.nodes_by_degree(g)[0][0], '1',"G23")
        self.assertEqual(gf.nodes_by_degree(g)[1][0], '2',"G23")
        self.assertEqual(gf.nodes_by_degree(g)[2][0], '3', "G23")
        self.assertEqual(gf.nodes_by_degree(g)[3][0], '4', "G23")
        
    '''Test g24 - test degrees on invalid type'''
    def testg24_nodesByDegree_type(self):
        with self.assertRaises(TypeError):
            gf.nodes_by_degree(None)

    '''Test g25 - test complete  on graph that is almost  complete'''
    def testg25_isComplete_almost(self):
        self.assertFalse(gf.is_complete(Graph({'1' : ['2'], '2' : ['1','3'], '3' : ['2']})), "G25")
        
        
        
    
if __name__ == "__main__":
    unittest.main()