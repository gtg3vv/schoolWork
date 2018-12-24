
import sys
import math
tests = open(str(sys.argv[1]),"r")
x = []

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def closest(points):
    if len(points) == 3:
        if (distance(points[0],points[1]) < distance(points[1],points[2])) and (distance(points[0],points[1]) < distance(points[0],points[2])):
            return [points[0],points[1]]
        elif (distance(points[1],points[2]) < distance(points[0],points[1])) and (distance(points[1],points[2]) < distance(points[0],points[2])):
            return [points[1],points[2]]
        else: return [points[0],points[2]]
    elif len(points) == 2:
        return points
    else:
        points.sort(key=lambda x:x[0])
        leftmin = closest(points[0:len(points)//2])
        rightmin = closest(points[len(points)//2:])
        if distance(leftmin[0],leftmin[1]) < distance(rightmin[0],rightmin[1]):
            dist_from_line=distance(leftmin[0],leftmin[1])
            overallmin=[leftmin[0],leftmin[1]]
        else:
            dist_from_line=distance(rightmin[0],rightmin[1])
            overallmin=[rightmin[0],rightmin[1]]
        points[len(points)//2]
        points_by_line=[]
        for p in points:
            if   points[len(points)//2][0] - dist_from_line < p[0] < points[len(points)//2][0] + dist_from_line:
                points_by_line.append(p)
        points_by_line.sort(key=lambda x:x[1])
        for i in range(len(points_by_line)):
            for j in range(1,min(7,len(points_by_line)-i)):
                if distance(points_by_line[i],points_by_line[i+j]) < dist_from_line:
                    overallmin = [points_by_line[i],points_by_line[i+j]]
        return(overallmin)
        
        

while tests:
    numClasses = tests.readline().strip()
    if numClasses == "0":
        break
    else:
        numClasses = int(numClasses)
        x = []
    for i in range(0, numClasses):
        line = tests.readline().strip().split(" ")
        x.append((float(line[0]),float(line[1])))
    minpair=closest(x)
    print("{0:.4f}".format(round(distance(minpair[0],minpair[1]),4)) \
        if distance(minpair[0],minpair[1]) < 10000 else "infinity")
   

