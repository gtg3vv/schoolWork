##
## File: week03a.py (STAT 3250)
## Topic: If/else and more numpy
##

import numpy as np # Load NumPy

#### if/else/elif 

sizes = [12, 16, 12, 20, 18, 20]
for s in sizes:
    if s == 12:
        print("Small")
    else:
        print("Not small")
        
# We can use "elif" (short for "else if")
# to refine the decisions.
        
for s in sizes:
    if s == 12:
        print("Small")
    elif s == 16:
        print("Medium")
    elif s == 20:
        print("Large")
    else:
        print("Not a size")
        
# The elif's are evaluated until the first one is
# True, then the rest are skipped.
   
rvals = np.random.choice(range(-3,4),size=20)
print(rvals)

for x in rvals:
    if x < 0:
        print("Negative")
    elif x == 0:
        print("Zero")
    else:
        print("Positive")

#%%

#### NumPy: Arrays and Vectorized Computation

## Creating arrays

arr1 = np.array([1,2,3,4,5,6,7])  # Define a 1-D array
arr1

## NumPy arithmetic operations on arrays

3*arr1  # Multiply each entry by 3
arr1 + arr1  # Add array values term by term
arr1*arr1  # Multiply array values term by term
arr1**3  # Raise array values to 3rd power

# Subsets and new values

arr1[3]  # The 4th value
arr1[3:5]  # The 4th and 5th values, returned as an array

arr1[2] = 20  # Replace 3rd element with 20
arr1
arr1[2:5] = 12  # Replace 3rd to 5th elements with 12
arr1

arr1_slice = arr1[1:4]  # A subset of arr1
arr1_slice

arr1_slice[2] = 30  # Changes the 3rd entry in arr1_slice
arr1_slice
arr1  # The change to arr1_slice also changes arr1!

arr1_slice = arr1[1:4].copy()  # Make a copy of arr1[1:4]
arr1_slice
arr1_slice[1] = 100
arr1_slice
arr1  # Now change to arr1_slice does not transmit back to arr1

# 2-dimensional arrays

arr2 = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])  # Define a 2-D array
arr2  # Kind of looks like a matrix

arr2[1]  # 2nd row
arr2[1][3]  # 2nd row, 4th entry
arr2[1,3]  # Same
arr2[:2]  # 1st and 2nd rows
arr2[2:]  # 3rd row
arr2[1:,:3]  # Rows 2-3 and columns 1-3
arr2[:,2]  # Column 3

arr3 = np.array([[3,2,-3,0,7],[0,5,2,-1,1],[2,-2,3,0,1],[6,4,7,2,2]])
arr3

# We can test values
arr3 == 2  # Test which entries are equal to 2
arr3 < 0 # Test which entries are negative

# Count and add values
arr3[arr3 < 0]  # Extract the values that are negative
(arr3 < 0).sum()  # Count the number of values that are negative
arr3[arr3 < 0].mean()  # Mean of the values that are negative
((arr3 < 2) & (arr3 > -2)).sum() # Count of entries x with -2<x<2








