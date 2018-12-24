#Gabriel Groover (gtg3vv)

def maxmin(mylist):
    if len(mylist) == 0:
        return None
        
    _max = mylist[0]
    _min = mylist[0]
    
    for i in mylist:
        if i < _min:
            _min = i
        if i > _max:
            _max = i
    
    return (_max,_min)
    

def common_items(list1, list2):
    common = [x for x in list1 if x in list2]
    nodup = []
    for i in common:
        if i not in nodup:
            nodup.append(i)
            
    return nodup
    
if __name__ == "main":
    assert maxmin([1,2,3]) == (3,1), "Wrong max min for [1,2,3]"
    assert maxmin([3,1,-2]) == (3,-2), "Wrong max min for [3,1,-2]"
    assert maxmin(['Q','Z','C','A']) == ('Z', 'A'), "Wrong max min for ['Q','Z','C','A']"
    assert common_items([1,2,3,4,6,6],[6,8,8,9,10]) == [6], "Wrong common items for duplicates"
    assert common_items([1],[2]) == [], "Wrong common items when none in common"