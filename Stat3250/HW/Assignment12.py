## File: Assignment12.py (STAT 3250)
## Topic: Assignment 12
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 1. Suppose $50,000 is invested on the investor’s 40th birthday at a fixed rate of return µ = 7.6% continuous.
# Determine the account balance each year from until the investor’s 65th birthday, and print
# a table that shows the investor’s age and the investment balance each year, with the balance given to
# the nearest cent. The first three table entries are shown below.
# 40 50000.00
# 41 53948.13
# 42 58208.01

#Dictionary to hold first three values
balance = { 40:50000.00, 41:53948.13, 42:58208.01 }

#For each value to age 65
for i in range(43,66):
	#Set balance for that year to previous * e^rate
	balance[i] = balance[i-1] * np.exp(.076)

#Create new dataframe from values and rename column
balanceDf = pd.DataFrame.from_dict(balance, orient='index').sort_index()
balanceDf.columns = ['balance']
#Print rounded dataframe to 2 digits
print(np.round(balanceDf, 2))

'''
1.
      balance                                                                       
40   50000.00                                                                       
41   53948.13
42   58208.01
43   62804.26
44   67763.45
45   73114.23
46   78887.51
47   85116.68
48   91837.71
49   99089.45
50  106913.81
51  115356.00
52  124464.80
53  134292.86
54  144896.98
55  156338.41
56  168683.30
57  182002.96
58  196374.39
59  211880.61
60  228611.25
61  246662.99
62  266140.13
63  287155.24
64  309829.76
65  334294.71
'''

# 2. Suppose we have the same investment as in the previous question, except that the annual rate of
# return has a lognormal distribution with mean µ = 7.6% and standard deviation σ = 16.7%. Simulate
# 100,000 times the balance on the investor’s 65th birthday, then use the results to answer the following
# questions regarding these balances:

#Initialize array of values and mu/sigma
balance65 = np.zeros(100000)
mu = .076
sigma = .167

#For 100000 tests
for i in range(100000):
	#Initial investment
	x = 50000
	#For ages 41 to 65
	for j in range(41,66):
		#Multiply previous value based on return function 
		x *= np.exp(np.random.normal(mu, sigma))
	#Set year in array
	balance65[i] = x


# (a) What is the mean balance?

#Mean of array
print(round(np.mean(balance65), 2))

'''
2a.
474154.51
'''

# (b) What is the median balance?

#Median of array
print(round(np.median(balance65),2))

'''
2b.
334416.26
'''

# (c) Give a 95% confidence interval for the balance. (That is, find the range of balances that make up
# the middle 95% of simulated balances.)

#Sort by balances and find bottom and top 5% value
balance65 = np.sort(balance65)
print(round(balance65[2499],2),round(balance65[97499],2))

'''
2c.
64582.09 1695294.77
'''

# (d) The investor’s goal is to have a 65th-birthday balance of at least $300,000. What proportion of
# times was the investor successful?

#Divide set of balances at/above success value and divide by total set of values
print(len(balance65[balance65 >= 300000]) / len(balance65))

'''
2d.
0.55233
'''

# (e) Plot a histogram of balances from this simulation

#Plot histogram with yearly values
plt.hist(balance65, bins=80, range=[0, 2000000])  
plt.show()

# 3. Repeat question 1, but now suppose that in addition to the initial deposit of $50,000 on the investor’s
# 40th birthday, there are also deposits of $3000 made on each birthday 41, 42, ..., 65. Assuming a
# fixed rate of return µ = 7.6% continuous as before, find the balance on the investor’s 65th birthday,
# immediately after the last deposit. Make a table of the birthdays from 40 to 65, and the balances. The
# first three table entries are below.
# 40 50000.00
# 41 56948.13
# 42 64444.90

#Dictionary to hold first three values
balance = { 40:50000.00, 41:56948.13, 42:64444.90 }

#For each age up to 65
for i in range(43,66):
	#Set balance for year based on previous year * growth + deposit
	balance[i] = (balance[i-1] * np.exp(.076)) + 3000

#Make new dataframe from year values and sort years, then relabel columns
balanceDf = pd.DataFrame.from_dict(balance, orient='index').sort_index()
balanceDf.columns = ['balance']

#Print dataframe rounded to nearest cent
print(np.round(balanceDf, 2))

'''
3.
      balance
40   50000.00
41   56948.13
42   64444.90
43   72533.64
44   81261.08
45   90677.66
46  100837.80
47  111800.22
48  123628.25
49  136390.25
50  150159.98
51  165017.00
52  181047.16
53  198343.11
54  217004.80
55  237140.05
56  258865.24
57  282305.91
58  307597.51
59  334886.20
60  364329.68
61  396098.09
62  430375.01
63  467358.53
64  507262.36
65  550317.11
'''

# 4. Repeat question 2, but now suppose that in addition to the initial deposit of $50,000 on the investor’s
# 40th birthday, there are also deposits of $3000 made on each birthday 41, 42, ..., 65. Assume the annual
# rate of return has a lognormal distribution with mean µ = 7.6% and standard deviation σ = 16.7%, and
# simulate 100,000 times the balance on the investor’s 65th birthday immediately after the last deposit.
# Use the simulations to answer (a)–(e).

#Set up intial array and mu/sigma values
balance65 = np.zeros(100000)
mu = .076
sigma = .167

#For each test
for i in range(100000):
	#Initial deposit
	x = 50000
	#For remaining years
	for j in range(41,66):
		#Multiply x by growth and add deposit
		x *= np.exp(np.random.normal(mu, sigma))
		x += 3000
	#Add to array
	balance65[i] = x

balance65 = np.round(balance65,2)


# (a) What is the mean balance?

#Mean of array
print(round(np.mean(balance65),2))

'''
4a.
745906.78
'''


# (b) What is the median balance?

#Median of array
print(round(np.median(balance65),2))

'''
4b.
564769.76
'''

# (c) Give a 95% confidence interval for the balance. (That is, find the range of balances that make up
# the middle 95% of simulated balances.)

#Sort by balances and find top and belowttom 5% values
balance65 = np.sort(balance65)
print(round(balance65[2499],2),round(balance65[97499],2))

'''
4c.
150537.39 2406157.8
'''

# (d) The investor’s goal is to have a 65th-birthday balance of at least $300,000. What proportion of
# times was the investor successful?

#Divide set of balances at/above success value and divide by total set of values
print(len(balance65[balance65 >= 300000]) / len(balance65))

'''
4d.
0.81745
'''

# (e) Plot a histogram of balances from this simulation

#Plot  histogram of balances
plt.hist(balance65, bins=80, range=[0, 2000000])  
plt.show()


# 5. Now let’s factor in inflation. Repeat question 3, but suppose that the birthday deposits start at $3000
# on the 41st birthday, and increase by 3% continuous each year until the 65th birthday, so that the
# 42nd-birthday is $3000e
# .03 = $3091.36, the 43rd-birthday deposit is $3091.36e
# .03 = $3185.51, and so
# on. Make a table of the birthdays from 40 to 65, and the balances. The first three table entries are
# below.
# 40 50000.00
# 41 56948.13
# 42 64536.26

#Set up inital dictionary and deposit
balance = { 40:50000.00 }
deposit = 3000

#For each age
for i in range(41,66):
	#Balance of age = previous * growth + the deposit
	balance[i] = (balance[i-1] * np.exp(.076)) + deposit
	#Update deposit
	deposit *= np.exp(.03)

#New dataframe from the balance values and sort by year
balanceDf = pd.DataFrame.from_dict(balance, orient='index').sort_index()
balanceDf.columns = ['balance']

#Print rounded dataframe
print(np.round(balanceDf, 2))

'''
5.
      balance
40   50000.00
41   56948.13
42   64536.26
43   72817.72
44   81850.12
45   91695.71
46  102421.74
47  114100.87
48  126811.61
49  140638.73
50  155673.82
51  172015.80
52  189771.51
53  209056.35
54  229994.92
55  252721.79
56  277382.29
57  304133.33
58  333144.36
59  364598.32
60  398692.74
61  435640.90
62  475673.06
63  519037.80
64  566003.51
65  616859.91
'''


# 6. Repeat question 4, but suppose that the birthday deposits start at $3000 on the 41st birthday, and
# increase by 3% continuous each year until the 65th birthday as in 5. Use the simulations to answer
# (a)–(e).

#Initialize array and mu/sigma values
balance65 = np.zeros(100000)
mu = .076
sigma = .167

#For 100000 tests
for i in range(100000):
	#Initial deposit values
	x = 50000
	deposit = 3000
	#For each age
	for j in range(41,66):
		#Multiply by growth, add deposit, and update deposit
		x *= np.exp(np.random.normal(mu, sigma))
		x += deposit
		deposit *= np.exp(.03)
	#Save value
	balance65[i] = x

balance65 = np.round(balance65, 2)

# (a) What is the mean balance?

#Array mean
print(round(np.mean(balance65),2))

'''
6a.
817764.05
'''

# (b) What is the median balance?

#Array median
print(round(np.median(balance65),2))

'''
6b.
631455.57
'''

# (c) Give a 95% confidence interval for the balance. (That is, find the range of balances that make up
# the middle 95% of simulated balances.)

#Sort by balance and find top and bottom 5% values
balance65 = np.sort(balance65)
print(round(balance65[2499],2),round(balance65[97499],2))

'''
6c.
186197.18 2580768.03
'''

# (d) The investor’s goal is to have a 65th-birthday balance of at least $300,000. What proportion of
# times was the investor successful?

#Print total values in success range over all values
print(len(balance65[balance65 >= 300000]) / len(balance65))

'''
6d.
0.87468
'''

# (e) Plot a histogram of balances from this simulation

#Plot new histogram
plt.hist(balance65, bins=80, range=[0, 2000000])  
plt.show()

# 7. Assume the savings pattern and rate of return until the 65th birthday given in question 5. After
# that, the investor adopts a more conservative investment strategy that produces an annual fixed rate
# of return µ = 3.5% continuous. Suppose the investor plans to make withdrawals of $25,000 on each
# birthday 66, 67, 68, ... 100. Find the balance on the investor’s 100th birthday, immediately after the
# last withdrawal. Make a table of the birthdays from 65 to 100, and the balances.

#Initial values
balance = { 40:50000.00 }
deposit = 3000

#For first set of ages
for i in range(41,66):
	#Calculate balance based on previous year and add deposit
	balance[i] = (balance[i-1] * np.exp(.076)) + deposit
	deposit *= np.exp(.03)

#For second set  of ages
for i in range(66,101):
	#Calculate balance based on previous year and subtract withdrawal
	balance[i] = (balance[i-1] * np.exp(.035)) - 25000

#Create new dataframe from the balance, sort by ages, and round
balanceDf = pd.DataFrame.from_dict(balance, orient='index').sort_index()
balanceDf.columns = ['balance']
balanceDf = np.round(balanceDf, 2)
print(balanceDf.tail(36))

'''
7.
       balance
65   616859.91
66   613832.28
67   610696.80
68   607449.64
69   604086.82
70   600604.22
71   596997.57
72   593262.45
73   589394.28
74   585388.34
75   581239.70
76   576943.29
77   572493.84
78   567885.90
79   563113.83
80   558171.78
81   553053.70
82   547753.31
83   542264.13
84   536579.42
85   530692.22
86   524595.32
87   518281.25
88   511742.28
89   504970.39
90   497957.29
91   490694.38
92   483172.78
93   475383.25
94   467316.26
95   458961.93
96   450310.02
97   441349.93
98   432070.69
99   422460.92
100  412508.86
'''

# 8. Assume the savings pattern and rate of return until the 65th birthday given in question 6. After that,
# the investor adopts a more conservative investment strategy that produces an annual rate of return has
# a lognormal distribution with mean µ = 3.5% and standard deviation σ = 5.1%. Suppose the investor
# plans to make withdrawals of $25,000 on each birthday 66, 67, 68, ... 100. Simulate 100,000 times
# the balance on the investor’s 100th birthday, then use the results to answer the following questions
# regarding these balances:

#Initialize array
balance65 = np.zeros(100000)

#For 100000 tests
for i in range(100000):
	#Initial values
	x = 50000
	deposit = 3000
	mu = .076
	sigma = .167

	#For first set of ages
	for j in range(41,66):
		#Calculate balance from previous year and add deposit, update the deposit
		x *= np.exp(np.random.normal(mu, sigma))
		x += deposit
		deposit *= np.exp(.03)

	#Update the deposit mu/sigma
	mu = .035
	sigma = .051

	#For second set of ages
	for j in range(66, 101):
		#Calculate balance from previous year and subtract withdrawal
		x *= np.exp(np.random.normal(mu, sigma))
		x -= 25000

	balance65[i] = x

balance65 = np.round(balance65, 2)


# (a) What is the mean balance?

#Mean of array
print(round(np.mean(balance65),2))

'''
8a.
1188915.51
'''


# (b) What is the median balance?

#Median of array
print(round(np.median(balance65),2))

'''
8b.
446040.34
'''

# (c) Give a 95% confidence interval for the balance. (That is, find the range of balances that make up
# the middle 95% of simulated balances.)

#Sort by balance and find top and bottom 5% values
balance65 = np.sort(balance65)
print(round(balance65[2499],2),round(balance65[97499],2))

'''
8c.
-1106065.02 7859097.26
'''


# (d) The investor’s goal is to have a 100th-birthday balance that is positive. What proportion of times
# was the investor successful?


#Print total values in success range over all values
print(len(balance65[balance65 >= 0]) / len(balance65))

'''
0.63436
'''

# (e) Plot a histogram of balances from this simulation

#Plot histogram
plt.hist(balance65, bins=150, range=[-2000000, 7000000])  
plt.show()