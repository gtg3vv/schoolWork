## File: assignment02.py (STAT 3250)
## Topic: Assignment 2
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import numpy as np

#### Assignment 2, Part A
##
## A1. Generate an array x of 10000 random values from 
##     a uniform distribution on the interval [0,20],
##     then use a for loop to determine the percentage     
##     of values that are in the interval [5,12].
arrayX = np.random.uniform(low=0,high=20,size=10000)
def randomDist():
    x = np.random.uniform(low=0,high=20,size=10000)
    
    numInRange = 0
    for val in x:
        if 5 <= val <= 12:
            numInRange+=1
    
    return numInRange / 10000 * 100
    
print(round(randomDist(),2),"%",sep="")

'''
A1.
34.85%
'''
    
## Note: A1 asks for a percentage, not a count and not
##       a proportion.

## A2. Repeat A1 500 times, then compute the average
##     of the 500 percentages found.

sumAvg = 0.0
for x in range(0,500):
    sumAvg += randomDist()

print(round(sumAvg/500,2),"%",sep="")

'''
A2.
34.97%
'''

## A3. For the array x in A1, use a while loop to determine 
##     the number of random entries required to find the
##     first that is less than 4.

def a3():
    numEntries = 1
    randomChoice = np.random.choice(arrayX, size=1)
    while randomChoice >= 4:
        numEntries +=1
        randomChoice = np.random.choice(arrayX, size=1)
    
    return numEntries
    
print(a3())

'''
A3.
6
'''

## A4. Repeat A3 1000 times, then compute the average for the
##     number of random entries required.

sumAvg = 0
for x in range(1000):
    sumAvg += a3()

print(sumAvg / 1000)

'''
A4.
5.13
'''


## A5. For the array x in A1, use a while loop to determine 
##     the number of random entries required to find the
##     third entry that exceeds 12.

def a5():
    numEntries = 0
    countGreater = 0
    randomChoice = np.random.choice(arrayX, size=1)
    while countGreater < 3:
        if randomChoice > 12:
            countGreater += 1
        numEntries += 1
        randomChoice = np.random.choice(arrayX, size=1)
        
    return numEntries

print(a5())

'''
A5.
9
'''

## A6. Repeat A5 1000 times, then compute the average for the
##     number of random entries required.

sumAvg = 0
for x in range(1000):
    sumAvg += a5()

print(sumAvg / 1000)

'''
A6.
7.535
'''

#%%


#### Assignment 2, Part B
##

#    For this problem you will draw samples from a normal
#    population with mean 40 and standard deviation 12.
#    Run the code below to generate your population, which
#    will consist of 500,000 elements.

p1 = np.random.normal(40,12,size=500000)
popMean = np.mean(p1)    
popStd = np.std(p1,ddof=1)

#  a) The formula for a 95% confidence interval for the 
#     population mean is given by
#     
#     [xbar - 1.96*sigma/sqrt(n), xbar + 1.96*sigma/sqrt(n)]
#
#     where xbar is the sample mean, sigma is the population
#     standard deviation, and n is the sample size.
#
#   i) Select 10,000 random samples of size 10 from p1.  For
#      each sample, find the corresponding confidence 
#      interval, and then determine the proportion of
#      confidence intervals that contain the population mean.

def confidence(sampleSize):

    sqrt = np.sqrt(sampleSize)
    numInInterval = 0
    for x in range(10000):    
        sample = np.random.choice(p1, sampleSize)
        intervalWidth = 1.96 * popStd / sqrt
        
        if np.mean(sample) - intervalWidth <= popMean <= np.mean(sample) + intervalWidth:
            numInInterval += 1
    
    return numInInterval / 10000
        
print(confidence(10))

'''
BAi.
.948
'''
    
#   ii) Repeat part i) using samples of size 20.
print(confidence(20))

'''
BAii.
.951
'''

#   iii) Repeat part i) using samples of size 30.
print(confidence(30))

'''
BAiii.
.9519
'''

#

#  b) Frequently in applications the population standard
#     deviation is not known. In such cases, the sample
#     standard deviation is used instead.  Repeat part a)
#     replacing the population standard deviation with the
#     standard deviation from each sample, so that the
#     formula is
#
#     [xbar - 1.96*stdev/sqrt(n), xbar + 1.96*stdev/sqrt(n)]
#
#     Tip: The command for the standard deviation is 
#          np.std(data, ddof=1)

def confidence2(sampleSize):
    sqrt = np.sqrt(sampleSize)
    numInInterval = 0
    for x in range(10000):    
        sample = np.random.choice(p1, sampleSize)
        sampleStd = np.std(sample, ddof=1)
        intervalWidth = 1.96 * sampleStd / sqrt
        
        if np.mean(sample) - intervalWidth <= popMean <= np.mean(sample) + intervalWidth:
            numInInterval += 1
    
    return numInInterval / 10000
        
print(confidence2(10))
'''
BBi.
.9148    
'''

#   ii) Repeat part i) using samples of size 20.
print(confidence2(20))

'''
BBii.
.9319
'''

#   iii) Repeat part i) using samples of size 30.
print(confidence2(30))

'''
BBiii.
.9362
'''

#
#  c) Your answers in part b) should be a bit off.  The 
#     problem is that a t-distribution is appropriate when
#     using the sample standard deviation.  Repeat part b),
#     this time using t* in place of 1.96 in the formula,
#     where: t* = 2.262 for n = 10, t* = 2.093 for n = 20,
#     and t* = 2.045 for n = 30.

def confidence3(sampleSize, tFactor):
    sqrt = np.sqrt(sampleSize)
    numInInterval = 0
    for x in range(10000):    
        sample = np.random.choice(p1, sampleSize)
        sampleStd = np.std(sample, ddof=1)
        intervalWidth = tFactor * sampleStd / sqrt
        
        if np.mean(sample) - intervalWidth <= popMean <= np.mean(sample) + intervalWidth:
            numInInterval += 1
    
    return numInInterval / 10000

#   i)

print(confidence3(10,2.262))

'''
BCi.
.9508
'''
    
#   ii) Repeat part i) using samples of size 20.
print(confidence3(20,2.093))

'''
BCii.
.9485
'''

#   iii) Repeat part i) using samples of size 30.
print(confidence3(30,2.045))

'''
BCiii.
.945
'''


