## File: Assignment3.py (STAT 3250)
## Topic: Assignment 3
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

#### Assignment 3, Part A
##
## The problems in Part A should be done without the use of 
## loops.  They can be done with NumPy functions.

## The different questions in this part use the array
## defined below.

import numpy as np # Load NumPy
arr1 = np.array([[2,5,3,-1,0,1,-6,8,1,-9],[-1,3,4,2,0,1,2,7,8,-1],
                [3,0,-2,-2,5,4,8,-1,0,2],[3,3,-3,2,4,5,1,9,8,6],
                [1,1,0,2,-3,-2,4,-7,0,-9],[0,1,7,8,-5,-4,0,2,5,-9]])

##  (a) Extract a submatrix arr1_slice1 from arr1 that consists of
##      the second and third rows of arr1.

print(arr1[[1,2], :])

'''
Aa.
[[-1  3  4  2  0  1  2  7  8 -1]
 [ 3  0 -2 -2  5  4  8 -1  0  2]]
'''

##  (b) Find a one dimensional array that contains the entries of
##      arr1 that are less than -5.

print(arr1[np.where( arr1 < -5 )])

'''
Ab.
[-6 -9 -7 -9 -9]
'''

##  (c) Determine the number of entries of arr1 that are greater
##      than 3

print(len(arr1[np.where(arr1 > 3)]))

'''
Ac.
17
'''

##  (d) Find the mean of the entries of arr1 that are less than
##      or equal to -2.

print(arr1[np.where(arr1 <= -2)].mean())

'''
Ad.
-5.08333333333
'''

##  (e) Find the sum of the squares of the even entries of arr1.

print(np.square(arr1[np.where(arr1 % 2 == 0)]).sum())

'''
Ae.
512
'''

##  (f) Determine the proportion of positive entries of arr1 
##      that are greater than 3.

print(len(arr1[np.where(arr1 > 3)]) / len(arr1[np.where(arr1 > 0)]))

'''
Af.
0.4722222222222222
'''

#%%

#### Assignment 3, Part B
##
## The problems in Part B should be done without the use of 
## loops.  They can be done with NumPy functions.

## Use the code below to define arr2 and arr3

arr2 = np.arange(-20,28,2)
arr2 = arr2.reshape((4,6))
arr3 = np.arange(-20,12)
arr3 = arr3.reshape((8,4))

##  (a) Extract a submatrix from arr2 of elements that are
##      in rows 0 and 3 and columns 1 and 4 of arr2, then
##      determine the mean and standard deviation of
##      those elements.

#Based on row 0 being used, I am assuming column 1 is the  literal index 1

print("Mean:", arr2[[0,3]][:,[1,4]].mean())
print("Std:", arr2[[0,3]][:,[1,4]].std())

'''
Ba.
Mean: 3.0
Std: 18.2482875909
'''

##  (b) Multiply each element of arr2 by 3, then add 1
##      to each element, then replace the even values
##      of the resulting matrix with 0.

newArray = np.add(np.multiply(arr2, 3),1)
print(np.where(newArray % 2 == 0, 0, newArray))

'''
Bb.
[[-59 -53 -47 -41 -35 -29]
 [-23 -17 -11  -5   1   7]
 [ 13  19  25  31  37  43]
 [ 49  55  61  67  73  79]]
 '''

##  (c) Extract rows 1 and 6 from arr3, find the transpose
##      of the resulting matrix.

#Here I am using 1 and 6 because earlier in the assignment he wrote "row 0"
# so I am assuming this refers to the literal indexes 1 and 6.

print(arr3[[1,6],:].T)

'''
Bc. 
[[-16   4]
 [-15   5]
 [-14   6]
 [-13   7]]
'''

##  (d) Replace the odd negative entries of arr3 with zeros,
##      then determine the means of the rows of the
##      resulting matrix.

print(np.where((arr3 % 2 != 0) & (arr3 < 0), 0 , arr3).mean(axis=1))

'''
Bd. 
[-9.5 -7.5 -5.5 -3.5 -1.5  1.5  5.5  9.5]
'''

##  (e) Find all entries that are in both arr2 and arr3.

print(np.intersect1d(arr2,arr3))

'''
Be. 
[-20 -18 -16 -14 -12 -10  -8  -6  -4  -2   0   2   4   6   8  10]
'''

##  (f) Find all entries that are in arr3 but not arr2.

print(np.setdiff1d(arr3,arr2))

'''
Bf. 
[-19 -17 -15 -13 -11  -9  -7  -5  -3  -1   1   3   5   7   9  11]
'''

#%%


#### Assignment 3, Part C

## C1. Suppose that course grades are assigned based on
##     course average as follows: 90's = A, 80's = B,
##     70's = C, 60's = D, Below 60 = F.
##     
##  (i) Define a function called "grade" that takes a course
##      average as input and returns a grade.

def grade(avg):
    if avg >= 90:
        return 'A'
    if avg >= 80:
        return 'B'
    if avg >= 70:
        return 'C'
    if avg >= 60:
        return 'D'
    return 'F'
    
'''
C1i.
No output unless you call the function and print the return value.
'''

##  (ii) Use a for loop to take the list of course averages
##       defined below and convert it into a list of
##       corresponding course grades. 

avgs = [99, 73, 60, 91, 93, 92, 68, 55, 60, 79, 79, 92, 51, 78, 68, 90, 99,
       62, 58, 76, 78, 65, 92, 83, 95, 82, 92, 85, 83, 65, 85, 61, 69, 72,
       63, 79, 59, 63, 85, 97]

for i in range(len(avgs)):
    avgs[i] = grade(avgs[i])
    
print(avgs)

'''
C1ii. 
['A', 'C', 'D', 'A', 'A', 'A', 'D', 'F', 'D', 'C', 'C', 'A', 'F', 'C', 'D', 'A',
'A', 'D', 'F', 'C', 'C', 'D', 'A', 'B', 'A', 'B', 'A', 'B', 'B', 'D', 'B', 'D',
'D', 'C', 'D', 'C', 'F', 'D', 'B', 'A']
'''

