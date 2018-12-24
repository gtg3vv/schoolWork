import sys
import math
import time
tests = open(str(sys.argv[1]),"r")

graph = {}

def pathSearch(path):
    if path[-1] == "anooseyourcaboose":
        return path
    for edge in graph[path[-1]]:
        if edge not in path and graph[path[-1]][edge][0] > 0:
            path.append(edge)
            val = pathSearch(path)
            if val:
                return val
            else:
                path.remove(path[-1])
    return False   

def validateSol():
    valid = True
    for student in graph["startyourengines"]:
        if graph["startyourengines"][student][0] > 0:
            valid = False
    return "Yes" if valid else "No"

while tests:
    numRegs = tests.readline().strip()
    if numRegs == "0 0 0":
        break
    else:
        numRegs = numRegs.split()
        x = []
        graph = {}
        graph["startyourengines"] = {}
    for i in range(0, int(numRegs[0])):
        line = tests.readline().strip().split(" ")
        if line[0] not in graph:
            graph[line[0]] = {}
            graph["startyourengines"][line[0]] = [int(numRegs[2]),True]
        if line[1] not in graph:
            graph[line[1]] = {}
        graph[line[0]][line[1]] = [1,True]
        graph[line[1]][line[0]] = [0,False]
    for i in range(0, int(numRegs[1])):
        line = tests.readline().strip().split()
        graph[line[0]]["anooseyourcaboose"] = [int(line[1]),True]
    graph["anooseyourcaboose"] = {}
    tests.readline()

    myPath = pathSearch(["startyourengines"])
    while myPath:
        for edge in range(len(myPath) - 1):
            if myPath[edge] == "startyourengines" or myPath[edge+1] == "anooseyourcaboose":
                graph[myPath[edge]][myPath[edge+1]][0] -= 1
            elif graph[myPath[edge]][myPath[edge+1]][1]:
                graph[myPath[edge]][myPath[edge+1]][0] -= 1
                graph[myPath[edge+1]][myPath[edge]][0] += 1
            elif not graph[myPath[edge]][myPath[edge+1]][1]:
                graph[myPath[edge]][myPath[edge+1]][0] += 1
                graph[myPath[edge+1]][myPath[edge]][0] -= 1
        myPath = pathSearch(["startyourengines"])
    print(validateSol())
    
    


        




    

    
        
                
                
            
       
            
