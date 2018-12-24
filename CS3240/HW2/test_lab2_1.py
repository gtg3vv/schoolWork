from hw2_set import OurSet

def test_add_empty():
    """S1: Add item to empty set"""
    s1 = OurSet()
    s1.add(1)
    assert len(s1) == 1
    assert str(s1) == "<1>"

def test_add_nonempty_dup():
    """S2: Add duplicate item to nonempty set """
    s1 = OurSet()
    s1.add_list([1,2,3])
    s1.add(1)
    assert len(s1) == 3
    assert str(s1) == "<1,2,3>"

def test_add_nonempty():
    """S3: Add unique item to nonempty"""
    s1 = OurSet()
    s1.add_list([2,3])
    s1.add(1)
    assert len(s1) == 3
    assert str(s1) == "<2,3,1>"
    
def test_addlist_empty():
    """S4: Add list to empty"""
    s1 = OurSet()
    s1.add_list([1,2,3])
    assert len(s1) == 3
    assert str(s1) == "<1,2,3>"

def test_addlist_nonempty_dup():
    """S5: Add list to nonempty""" 
    s1 = OurSet()
    s1.add_list([2,3,4])
    s1.add_list([1,2,3])
    assert len(s1) == 4
    assert str(s1) == "<2,3,4,1>"
    
def test_len_empty():
    """S6: Len of  empty set"""
    s1 = OurSet()
    assert len(s1) == 0
    
def test_len_nonempty():
    """S7: Len of nonempty set"""
    s1 = OurSet()
    s1.add_list([1,2,3])
    assert len(s1) == 3
        