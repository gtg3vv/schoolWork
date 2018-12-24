#Gabriel Groover (gtg3vv)

"""Given a single list as input, returns list max and min in format (max,min)"""
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
    
"""Returns a list containing common items between two lists"""
def common_items(list1, list2):
    common = [x for x in list1 if x in list2]
    nodup = []
    for i in common:
        if i not in nodup:
            nodup.append(i)
            
    return nodup

"""Returns a list containing items unique to each of two lists"""    
def notcommon_items(list1, list2):
    notcommon = []
    
    for x in list1:
        if x not in list2 and x not in notcommon:
            notcommon.append(x)
            
    for x in list2:
        if  x not in list1 and x not in notcommon:
            notcommon.append(x)
            
    return notcommon
    
"""Returns count of unique items in a list input"""    
def count_list_items(list1):
    numItems = {}
    
    for x in list1:
        if x not in numItems:
            numItems[x] = 1
        else:
            numItems[x] +=1
    return numItems
    
if __name__ == '__main__':    
    print(notcommon_items([1,1,3],[1,5,6]))
    print(count_list_items([1,3,2,2,3,1,1,2]))