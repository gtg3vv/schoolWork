import unittest
from hw2_set import OurSet

class TestSet1(unittest.TestCase):

    def setUp(self):
        self.emptySet = OurSet()
        self.s1 = OurSet()
        self.s1.add_list([1,2,3])

    def test_union_nonempty_with_empty(self):
        """S8: Union of nonempty with empty"""
        self.assertEqual(len(self.s1), len(self.s1.union(self.emptySet)))

    def test_union_two_nonempty(self):
        """S9: Union of two nonempty with overlap"""
        s2 = OurSet()
        s2.add_list([2,3,4])
        self.assertEqual(4,len(s2.union(self.s1)))
    
    def test_intersect_empty_nonempty(self):
        """S10: Intersect empty with nonempty"""
        self.assertEqual(0,len(self.s1.intersection(self.emptySet)))
        
    def test_intersect_two_nonempty(self):
        """S11: Intersect two nonempty with some overlap"""
        self.s1.add(4)
        s2 = OurSet()
        s2.add_list([3,4,5,6])
        self.assertEqual(2, len(self.s1.intersection(s2)))
        

if __name__ == '__main__':
    unittest.main()