##
## File: week03b.py (STAT 3250)
## Topic: More numpy
##

#### More NumPy Features

import numpy as np # load numpy     

## Creating arrays

np.empty((5,3)) # 5-by-3 array, initialized but not always zeros
np.zeros((5,3)) # 5-by-3 array of 0's
np.ones((5,3)) # 5-by-3 array of 1's

arr = np.arange(40)  # Define a 1-D array [0,...,39]
arr
arr = arr.reshape((10,4)) # Convert values into a 10-by-4 array
arr

## Fancy indexing

# NumPy supports extended indexing of values from arrays.
arr[2]  # Row indexed by 2
arr[[1,3,5]]  # Rows indexed by 1, 3, and 5
arr[[3,5,1]]  # Same rows, different order
arr[:,[0,2]]  # All rows, columns indexed by 0 and 2
arr[[2,4,5],[0,1,2]] # Entries indexed by (2,0),(4,1),(5,2)

# If we want the "grid" of rows indexed 2,4,5 and columns indexed 0,1,2:
arr[[2,4,5]][:,[0,1,2]]  # A bit awkward, but it works.

# The transpose "T" interchanges the rows and columns
arr[[2,4,5]][:,[0,1,2]].T
arr.T

## np.where
# The command below will replace any element divisible
# by 3 with -1, and replace all other elements with 1.
np.where(arr % 3 == 0, -1, 1)

# This time we just replace elements divisible by 3 with
# -1, keep others the same.
np.where(arr % 3 == 0, -1, arr)

# Here we change the sign of elements divible by 3, keeping
# the others the same.
np.where(arr % 3 == 0, -arr, arr)

## Math & Stat Functions
arr.mean()  # The mean of all entries in arr
np.mean(arr)  # The same thing
arr.sum()  # The sum of all entries
np.sum(arr)  # The same thing

arr.mean(axis=0)  # The mean of each column
arr.mean(axis=1)  # The mean of each row
arr.std(axis=0)  # The standard devision of each column
arr.std(axis=1)  # The standard devision of each row

## Set operations
arr1 = np.array([2,4,6,8,2,4,6,8,10])
arr2 = np.array([2,3,4,2,4,8])

np.unique(arr1)  # Eliminate all duplicates
np.intersect1d(arr1,arr2)  # Intersetion of arr1 and arr2
np.union1d(arr1,arr2)  # Union of arr1 and arr2
np.in1d(arr1,arr2)  # Test which elements of arr1 are in arr2
np.setdiff1d(arr1,arr2)  # Elements in arr1 that are not in arr2
np.setxor1d(arr1,arr2)  # Elements in eactly one of arr1 and arr2

#%%

## Defining Functions
   
def myabs(x):
    if x < 0:
        print(-x)
    else:
        print(x)

myabs(5)
myabs(-7)
y = myabs(-4) # This does not set y = 4
y
sizes = [12, 16, 12, 20, 18, 20]
myabs(sizes) # Doesn't work with lists as defined.

# Functions can take different types of objects
# as input.
def mycountval(a,list):
    ct = 0
    for x in list:
        if x == a:
            ct += 1
    return(ct)

v = [3,4,2,-1,0,2,5,6,2,0,3,2,1]
z = mycountval(2, v)
z
ct  # Variables inside function stay inside
    
# Functions can return lists and other things
def mylistmult(n, list):
    newlist = n*list
    return(newlist)
    
mylistmult(3,[8,9,10])

#%%






