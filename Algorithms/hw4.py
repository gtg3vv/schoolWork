
import sys

tests = open(str(sys.argv[1]),"r")
grid = []
solnGrid = []

def longestPath(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (solnGrid[i][j] == -1):
                getPath(i,j)
                
    
    
def getPath(x,y):
    checkNearby = []
    if solnGrid[x][y] != -1:
        return solnGrid[x][y]
    if x-1 >= 0:
        if grid[x-1][y] < grid[x][y]:
            checkNearby.append(getPath(x-1,y))
    if y-1 >= 0:
        if grid[x][y-1] < grid[x][y]:
            checkNearby.append(getPath(x,y-1))
    if x+1 < len(grid):
        if grid[x+1][y] < grid[x][y]:
         checkNearby.append(getPath(x+1,y))
    if y+1 < len(grid[0]):
        if grid[x][y+1] < grid[x][y]:
            checkNearby.append(getPath(x,y+1))
    if len(checkNearby) == 0:
        solnGrid[x][y] = 1
        return 1
    else:
        solnGrid[x][y] = max(checkNearby) + 1
        return solnGrid[x][y]


while tests:
    numCases = tests.readline().strip()
    if numCases == "":
        break
    else:
        numCases = int(numCases)
    for i in range(0, numCases):
        grid = []
        solnGrid = []
        maxLength = []
        line = tests.readline().strip().split(" ")
        for j in range(0,int(line[1])):
            row = [int(k) for k in tests.readline().strip().split(" ")]
            solnRow = [-1 for l in row]
            solnGrid.append(solnRow)
            grid.append(row)
        longestPath(grid)
        print(line[0] + ": " + str(max([max(x) for x in solnGrid])))
            

    