##
## File: week02b.py (STAT 3250)
## Topic: Simulating confidence intervals
##

####   More on simulation

import numpy as np # load "numpy"

# Suppose that a large city has 500,000 voters that
# are evenly divided on an upcoming ballot issue.  The
# code below will simulate the population, assigning
# 0 (does not support) or 1 (supports) at random with
# equal probability to each voter.
pop = np.random.choice([0,1], size=500000, p=[0.5,0.5])

# According to the American Research Group online
# calculator (http://americanresearchgroup.com/sams.html)
# a sample of size 1067 is required to obtain an estimate 
# of the true population proportion within a margin of
# error of 3% for 95% of samples.  We can test the 95% figure 
# with simulation on our population.

# We use the "choice" function again, this time to choose
# a random sample from the population array pop.
s = np.random.choice(pop, size=1067)
s[0:20] # View the first 20 values in the random sample s

# Remark: The default sampling method for "choice" is
# with replacement.  Typically for surveys sampling is
# without replacement, but the simulation runs much
# slower when sampling is without replacement, and the
# large population makes repeats unlikely, so we use
# the default.

# The function "mean" adds up the entries in a list and
# divides by the length of the list, which (for this list)
# is exacly the proportion sampled who support the ballot
# issue
np.mean(s)

# A margin of error of 3% means a sample proportion between
# 0.47 and 0.53.  We can generate a lot of samples, the 
# determine if approximately 95% yield proportions between
# 0.47 and 0.53, as claimed.
ct = 0  # Counter of "successful" samples between 0.47 and 0.53
for i in range(10000):
    s = np.random.choice(pop, size=1067)
    prop = np.mean(s)  # Prop. sampled that support issue
    if prop >= 0.47 and prop <= 0.53: # True if 0.47<= prop <=0.53
        ct += 1  # Increment counter if 0.47<= prop <=0.53
ct/10000  # Proportion of samples that have 0.47<= prop <=0.53
          # Is this close to 95%?

# We can reduce the margin of error, but doing so also 
# reduces the probability that the sample proportion
# will be within the margin of error.  Here's the
# percentage for a 2% margin of error.
ct = 0  # Counter of "successful" samples between 0.48 and 0.52
for i in range(10000):
    s = np.random.choice(pop, size=1067)
    prop = np.mean(s)  # Prop. sampled that support issue
    if prop >= 0.48 and prop <= 0.52: # True if 0.48<= prop <=0.52
        ct += 1  # Increment counter if 0.48<= prop <=0.52
ct/10000  # Proportion of samples that have 0.48<= prop <=0.52

# Suppose that we want a margin of error large enough 
# so that 98% of samples are within the margin of error.
# This time we record all sample proportions, sort
# them, and find the 1st and 99th percentiles.  Then
# approximately 90% of proportions are between these
# values, giving us an approximate 98% confidence interval.
props = np.zeros(10000)  # Array to hold proportions
for i in range(10000):
    s = np.random.choice(pop, size=1067)
    props[i] = np.mean(s)  # Prop. sampled that support issue
props.sort()  # Sort the array of proportions
props[99]  # 1st percentile
props[9899] # 99th percentile
# We can pull these together for the approximate 98% confidence 
# interval for the population proportion.
[props[99],props[9899]]

# We can try the same thing for a 95% confidence interval, and
# compare to the results above.
props = np.zeros(10000)  # Array to hold proportions
for i in range(10000):
    s = np.random.choice(pop, size=1067)
    props[i] = np.mean(s)  # Prop. sampled that support issue
props.sort()  # Sort the array of proportions
props[249]  # 2.5th percentile
props[9749] # 97.5th percentile
[props[249],props[9749]]


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









