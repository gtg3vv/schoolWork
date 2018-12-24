def agreement(i1, i2):
    imman = []
    for i in i1:
        if i in i2:
            imman.append(i)
    return imman

def disagreement(i1, i2):
    object = []
    for i in i1:
        if i not in i2:
            object.append(i)
    return object

def compatibility(i1, i2):
    imman = agreement(i1, i2)
    object = disagreement(i1, i2)

    return len(imman)/(len(imman)+len(object))

def bestmatch(me, others):
    whom = 'no one'
    comp = -1
    for person in others:
        name, likes = person
        match = compatibility(me, likes)
        if match > comp:
            comp = match
            whom = name
    return whom
