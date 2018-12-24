__author__ = 'horton'

from ourqueue import OurQueue

def test_front_empty():
    """Q1: test calling front on empty queue"""
    q1 = OurQueue()
    res = q1.front()
    assert res == None

def test_remove_empty():
    """Q2: test calling remove on empty queue"""
    q1 = OurQueue()
    res = q1.remove()
    assert res == None, "removing from empty Queue should return None"
    assert len(q1) == 0,  "removing from empty Queue should leave len==0"

def test_remove_size1():
    """Q3: test calling remove on queue of size 1"""
    q1 = OurQueue([1])
    res = q1.remove()
    assert res == 1
    assert len(q1) == 0
    
def test_add_empty():
    """Q5: test adding item to empty queue"""
    q1 = OurQueue()
    q1.add(1)
    assert len(q1) == 1
    assert q1.front() == 1
    
def test_front_size1():
    """Q6: test front of full queue"""
    q1 = OurQueue([3])
    assert q1.front() == 3