## File: Assignment04.py (STAT 3250)
## Topic: Assignment 4
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2


import pandas as pd
import numpy as np

#### Part 1
##
## The questions in Part 1 refer to the data in the file
## 'fastfood1.csv'.  The file has two columns, "storenum"
## that gives the store number, and "secs" that gives the 
## number of seconds required to fill the order.

##  (a) Determine the average amount of time required to fill
##      all orders in the data set.

#Read in inital csv
ffData = pd.read_csv('fastfood1.csv',index_col=0)

#Find mean of key secs
print(np.mean(ffData['secs']))

'''
1A.
216.327107929

'''

##  (b) Find the maximum and minimum amount of time required to
##      fill an order.  Then determine the number of orders with
##      the maximum time, and the number of orders with the minimum time.

#Min/Max for key secs
ffMin = ffData['secs'].min()
ffMax = ffData['secs'].max()
print("Max time: ", ffMax)
print("Min time: ", ffMin)
print("Num max: ", ffData[ffData['secs'] == ffMax].count()[0])
print("Num min: ", ffData[ffData['secs'] == ffMin].count()[0])

'''
1b.
Max time:	600
Min time:	30
Num max:	23
Num min:	123
'''


##  (c) Determine the average amount of time required by store 777 to fill
##      its orders.

#Find instances where index(storenum) is 777 and get mean
print(np.mean(ffData.loc[ffData.index == 777])[0])

'''
1c.
198.519083969
'''


##  (d) Determine the number of records from store 321 in the data set. 

#Number of entries in dataframe for store 321
print(len(ffData.loc[ffData.index == 321]))

'''
1d.
97
'''

##  (e) Find the mean number of seconds 
##      needed to fill an order by stores 700-750.
# Assuming inclusive on both ends for 700 and 750

#Find all indexes that are both >= 700 and <= 750
print(np.mean(ffData.loc[(700 <= ffData.index) & (ffData.index <= 750)])[0])

'''
1e.
215.892454467
'''

##  (f) Find a 95% confidence interval for the proportion of orders for 
##      stores 500-600 that required more than 200 seconds to fill.

#Get all stores within range
orderRange = ffData.loc[(500 <= ffData.index) & (ffData.index <= 600)]
#Samplesize
n = orderRange.count()[0]
#P hat
p_ = orderRange[orderRange > 200].count()[0] / n
#Plug in to formula and print as a tuple
print((p_ - 1.96 * np.sqrt((p_ * (1 - p_)) / n), p_ + 1.96 * np.sqrt((p_ * (1 - p_)) / n)))

'''
1f.
(0.3683886862227696, 0.38620552814459169)
'''


##  (g) Determine the number of distinct stores in the data set.

#Group unique indexes in the storenum column and count the resulting array
print(len(ffData.groupby('storenum').nunique()))

'''
1g.
892
'''

##  (h) Determine which store has the lowest mean order time, and which
##      store has the highest mean order time.

#Group unique storenums together, but not as an index (keep the original store number) and find the mean
storeMeans = ffData.groupby('storenum',as_index=False).mean()
#Get index of min and  max (plus one because we index from 0 and stores index from 1)
print(storeMeans.idxmin()[0]+1)
print(storeMeans.idxmax()[0]+1)

'''
1h.
243
657
'''


##  (i) Determine the median number of orders for a single store.

#Group by unique storenums and count each one, find median of resulting array
print(np.median(ffData.groupby('storenum').count()))

'''
1i,
112.0
'''

#%%

#### Part 2
##
## The questions in Part 2 refer to the data in the file
## 'samplegrades.csv'.


##  (a) Compute the mean and sample standard deviation for 
##      both the Course Average and the SAT Writing score.

#Read new csv
gradeData = pd.read_csv('samplegrades.csv',index_col=0)

#Mean and std of each column of dataframe
print("CourseAve mean: ", gradeData['CourseAve'].mean())
print("CourseAve std: ", gradeData['CourseAve'].std(ddof=1))
print("Write mean: ", gradeData['Write'].mean())
print("Write std: ", gradeData['Write'].std(ddof=1))

'''
2a.
CourseAve mean:  80.4011501767
CourseAve std:  10.6664673725
Write mean:  666.723404255
Write std:  94.4556172505
'''

##  (b) Find the mean Final exam score for all females
##      in the class.

#Get all rows that have  gender female, get the meal, and take final column
print(gradeData[gradeData['Gender'] == 'F'].mean()['Final'])

'''
2b.
71.3517915309
'''

##  (c) Repeat (b), this time for all males in the TR930
##      section.

#Get all M,TR930 rows,take mean and final column
print(gradeData[(gradeData['Gender'] == 'M') & (gradeData['Sect'] == 'TR930')].mean()['Final'])

'''
2c.
68.1534090909
'''

##  (d) Compute the mean Homework score for all 1st-years
##      and then for all 4th-years.

#Get all rows that have years 1 and 4, get mean for HW column
print("First year mean: ", gradeData[gradeData['Year'] == 1].mean()['HW'])
print("Fourth year mean: ", gradeData[gradeData['Year'] == 4].mean()['HW'])

'''
2d.
First year mean:  189.243768116
Fourth year mean:  192.951724138
'''

##  (e) Find the probability that a randomly selected 2nd-year
##      was in the MW200 section.

#Find all rows with year 2 in correct section and divide by total rows in year 2
print(len(gradeData[(gradeData['Year'] == 2) & (gradeData['Sect'] == 'MW200')]) / len(gradeData[gradeData['Year'] == 2]))

'''
2e.
0.321428571429
'''

##  (f) Sort the DataFrame on the CourseAve
##      variable, then determine the mean course average
##      for the students with the top-20 averages.


#Make new DF sorted by course average
sortedDf = gradeData.sort_values(by = ['CourseAve'])
#Tail(n) takes last n values in the dataframe and finds the mean for the courseave column
print(sortedDf.tail(20).mean()['CourseAve'])

'''
2f.
95.21865
'''

##  (g) Determine the bottom-10 final exam scores for 
##      students in the MW200 section.

#Sort by final scores, use head to get top ten scoresv that  match section
sortedByFinal = gradeData.sort_values(by = ['Final'])
print(sortedByFinal[sortedByFinal['Sect'] == 'MW200'].head(10)[['Final']])

'''
2g.
        Final
StudID       
CRAMQ     0.0
ISCWI    27.5
HBTSX    35.0
BEYTQ    40.0
HYXDY    45.0
ZMERR    45.0
CBDIH    45.0
WQHKF    45.0
EFTKY    50.0
TVKOR    50.0
'''

##  (h) Among the students in the top-20% for APDE,
##      determine the percentage that finished in the
##      top-20% for course average.
##      (The top-20% is the top 113 stduents.  Be careful of ties!)



#Sort the list by APDE - use quantile to find value at top 20% mark for APDE col
topAPDE = sortedDf[sortedDf.APDE >= sortedDf.quantile(.8)['APDE']]
#Find num of values in APDE top 20 that are above 20% quantile for Course average and divide by total num in top APDE
#Convert to %
print(len(topAPDE[topAPDE.CourseAve >= sortedDf.quantile(.8)['CourseAve']]) /  len(topAPDE) * 100)

'''
2h.
16.9811320755
'''
