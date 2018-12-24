#Gabriel Groover
#Polaris Alpha Coding Challenge #2
#5/14/2017

# Please run the program using python3 and specify the testfile as the first
# command line parameter.
# ex) python3 polaris.py polaristest.txt

import sys

#Attempt to open test case file
try:
    tests = open(str(sys.argv[1]),"r")
except FileNotFoundError:
    print("The file was not found in directory.")
    exit()
except IndexError: 
    print("Please enter the file path as the first system argument.")
    exit()
except:
    print("Error opening file.")
    exit()


#Sorts by X and y coordinates separately and then finds the median of each.
#When restricted to four directional movement solving the X and Y coordinates are 
#independent problems.
#mobPositions is a list of coordinate pair tuples
#n is the size of the mob (not strictly necessary as len(list) is constant time in python)
def meetingPoint(mobPositions,n):
    
    #Sorts by first and then second tuple value. Each is n*log(n)
    sortX = sorted(mobPositions, key = lambda i : i[0])
    sortY = sorted(mobPositions, key = lambda i : i[1])
    
    if n % 2 != 0:
        meetPoint = (sortX[n//2][0],sortY[n//2][1])
    else:
        medianX = int((sortX[(n//2)-1][0] + sortX[(n//2)][0])/2)
        medianY = int((sortY[(n//2)-1][1] + sortY[(n//2)][1])/2)
        meetPoint = (medianX,medianY)
    
    distanceX = sum([abs(pair[0] - meetPoint[0]) for pair in mobPositions])
    distanceY = sum([abs(pair[1] - meetPoint[1]) for pair in mobPositions])
    
    return(meetPoint, distanceX + distanceY)

caseNum = 1

#Reads in test cases one at a time and calculates meeting points.
while tests:
    coords = []
    mobSize = 0
    testCase = tests.readline().strip()
    
    if testCase == "0":
        tests.close()
        break
    else:
        testCase = [int(i) for i in testCase.split()]
        
    #Break list of coordinates into pairs of tuples
    mobSize = int(testCase[0])
    for i in range(1, len(testCase), 2):
        coords.append(tuple(testCase[i:i + 2]))
        
    soln = meetingPoint(coords,mobSize)
    print('Case ',caseNum,': ',soln[0],' ',soln[1], sep='')
    caseNum += 1
    
