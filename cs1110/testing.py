
    
def duples(string):
    d = {}
    for i in range(len(string)-1):
        if string[i] in d:
            d[string[i]].append(string[i+1])
        else:
            d[string[i]] = [string[i+1]]
    return d
    
print(duples("x").insert(3))
