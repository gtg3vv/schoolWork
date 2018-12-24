#Gabriel Groover (gtg3vv)
#Room swapping algorithm
#Algorithm considers smallests rooms first that have positive deltas.
#Negative deltas are saved for last in increasingly negative order
import sys

def greedy(rooms):
    trailerSize = 0
    spaceAvailable = 0
    rooms.sort(key=lambda x: (x[0],-x[1]))
    # print(rooms)
    # print("pos")
    negs = []
    for x in rooms:
        # print("Space:",spaceAvailable)
        # print("Trailer:",trailerSize)
        if x[1] >= 0:
            if x[0] > spaceAvailable:
                trailerSize += x[0] - spaceAvailable
                spaceAvailable += (x[0] - spaceAvailable) + x[1]
            else:
                spaceAvailable += x[1]
        else:
            negs.append(x)
    negs.sort(key=lambda x: -x[1])
    # print(negs)
    # print('neg')
    for x in negs:
        # print("Space:",spaceAvailable)
        # print("Trailer:",trailerSize)
        if x[0] > spaceAvailable:
                trailerSize += x[0] - spaceAvailable
                spaceAvailable += (x[0] - spaceAvailable) + x[1]
                if spaceAvailable < 0:
                    trailerSize -= spaceAvailable
                    spaceAvailable = 0
        else:
            spaceAvailable += x[1]
            if spaceAvailable < 0:
                    trailerSize -= spaceAvailable
                    spaceAvailable = 0

    print(trailerSize)
                
    
tests = open(str(sys.argv[1]),"r")
x = []

while tests:
    numClasses = tests.readline().strip()
    if numClasses == "":
        break
    else:
        numClasses = int(numClasses)
        x = []
    for i in range(0, numClasses):
        line = tests.readline().strip().split(" ")
        x.append((int(line[0]),int(line[1]) - int(line[0])))
    greedy(x)
