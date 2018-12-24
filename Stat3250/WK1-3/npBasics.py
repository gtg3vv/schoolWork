##
## File: week02a.py (STAT 3250)
## Topic: Numpy and simulation
##

####   Random simulation

# This loads the "numpy" library, which 
# has a variety of functions to generate
# random values (plus other stuff we'll 
# get to later)
import numpy as np # "as np" lets us use "np"
                   # in place of "numpy"

# We can generate random values from a uniform
# distribution.  
x = np.random.uniform(low=0,high=100,size=1000)

# Remark: The above generates an "array" rather
# than a list.  For now these are similar, but
# we will use arrays more later so they are introduced
# here.

# The code below will count the number of
# entries in x that are less than 20.

ct = 0
for xval in x:
    if xval < 20:
        ct += 1  # Adds 1 to ct; same as ct = ct + 1
print(ct)  # We expect about 200 (roughly)

# If we generate a new set of 1000 random values,
# on [0,100], we expect the number of values that are
# less than 20 to vary.  Let's try it again.

x = np.random.uniform(low=0,high=100,size=1000)
ct = 0
for xval in x:
    if xval < 20:
        ct += 1  # Adds 1 to ct
print(ct)  # We expect about 200 (roughly)
 
# We can repeat this experiment numerous times, and 
# record the value of "ct" each time.  Here's 100
# repeats of the experiment, using nested for loops.
ctarray = np.zeros(100)  # An array to hold the values of ct
for i in range(100):
    x = np.random.uniform(low=0,high=100,size=1000)
    ct = 0
    for xval in x:
        if xval < 20:
            ct += 1  # Adds 1 to ct
    print(ct)  # Print count for each iteration
    ctarray[i] = ct # Record count
    
print(ctarray)  # The list of counts

# The numpy function "mean" will compute the mean
# of an array of values. 
np.mean(ctarray)  # We expect this to be near 200.

# A "while" loop repeats until a condition is not
# met.  For example:
ct = 0
while ct <= 5:  # Loop will run until ct > 5
   print("The count is %d" % ct)
   ct += 1

# For the array x generated above, suppose that we randomly
# select an entry in x until we find one that exceeds 90.
# We can use a while loop to perform the random selections,
# and to keep track of the number of selections required.
ct = 1  # Initialize the counter
s = np.random.choice(x, size=1)  # Make an initial random choice
while s <= 90:
    ct += 1  # Increment the counter by 1
    s = np.random.choice(x, size=1)  # Make a new random choice
print(ct)  # Print the number of choices to reach 90    
print(s)   # Print the value that exceeds 90
print(s[0]) # Remove s from the array

# We can do this over and over by nexting the while loop
# in a for loop.  This allows for an estimate of the average
# number of selections required to obtain the first value
# exceeding 90.  Let's try 1000 simulations.
ctarray = np.zeros(1000)  # An array to hold the values of ct
for i in range(1000):
    ct = 1  # Initialize the counter
    s = np.random.choice(x, size=1)  # Make an initial random choice
    while s <= 90:
        ct += 1  # Increment the counter by 1
        s = np.random.choice(x, size=1)  # Make a new random choice
    ctarray[i] = ct  # Record the number of selections required
print(np.mean(ctarray))  # Compute the mean number of selections required

#%%







