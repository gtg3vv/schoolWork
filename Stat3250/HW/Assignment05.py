## File: Assignment05.py (STAT 3250)
## Topic: Assignment 05
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2


import pandas as pd
import numpy as np

#### Part 1
##
## The questions in Part 1 refer to the data in the file
## 'fastfood2.csv'.  The file has several columns: "storenum"
## gives the store number, "secs" that gives the number of seconds 
## to fill the order, "dayofweek" gives the day of the week,
## "meal" gives which meal ordered, "drinkonly" is Yes if only
## a drink was ordered, "cost" gives the amount spent in cents.

#Read in inital csv
ffData = pd.read_csv('fastfood2.csv')

##  (a) Determine the proportion of meals that were for Lunch.

#Count rows where meal column is lunch and divide by all meals
print((ffData[ffData['meal'] == 'Lunch'].count() / ffData['meal'].count())[0])

'''
1a.

0.516522415444
'''

##  (b) Determine the mean time for each day of the week.

#Group seconds col based on weekday value and find mean
dailyMeans = ffData['secs'].groupby(ffData['dayofweek']).mean()
print("Friday:", dailyMeans['Fri'])
print("Thursday:", dailyMeans['Thur'])
print("Wednesday:", dailyMeans['Wed'])
print("Tuesday:", dailyMeans['Tues'])
print("Monday:", dailyMeans['Mon'])

'''
1b.
Friday: 216.234940657
Thursday: 216.605129495
Wednesday: 216.282449267
Tuesday: 215.742299693
Monday: 216.774747074
'''


##  (c) Find a 95% confidence interval for the proportion of "drink only"
##      orders for each of Breakfast, Lunch, and Dinner.  Does there appear
##      to be any difference among the three meals? 

meals = ['Breakfast', 'Lunch', 'Dinner']

#Loop through days to simplify code
for meal in meals:
	#Total number of meals of that type
	n = ffData[ffData['meal'] == meal].count()[0]
	#Proportion of meals that are correct type and drinkonly
	p_ = ffData[(ffData['meal'] == meal) & (ffData['drinkonly'] == 'Yes')].count()[0] / n
	print(meal + ":", (p_ - 1.96 * np.sqrt((p_ * (1 - p_)) / n), p_ + 1.96 * np.sqrt((p_ * (1 - p_)) / n)))

#There seems to be a substantially higher portion  of drink only meals for breakfast

'''
1c.
Breakfast: (0.22117406656754271, 0.23613394334162327)
Lunch: (0.12675719458238568, 0.13254281893086697)
Dinner: (0.12730476118757109, 0.1342341232723899)
'''

##  (d) Find the mean cost for each of the meal types.

#Group cost data by meal value and find mean of each
mealMeans = ffData['cost'].groupby(ffData['meal']).mean()
print("Dinner:", mealMeans['Dinner'])
print("Lunch:", mealMeans['Lunch'])
print("Breakfast:", mealMeans['Breakfast'])

'''
1d.
Dinner: 502.017676004
Lunch: 372.363622324
Breakfast: 292.079190751
'''

##  (e) Find the proportion of meals of each type, for each day of the week.

week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri']

#Loop through days of week
for day in week:
	#Get given day values
	oneDay = ffData[ffData['dayofweek'] == day]
	#Proportion of each meal type to total orders
	print(day, 'Breakfast:', oneDay[oneDay['meal'] == 'Breakfast'].count()[0] / oneDay.count()[0])
	print(day, 'Lunch:', oneDay[oneDay['meal'] == 'Lunch'].count()[0] / oneDay.count()[0])
	print(day, 'Dinner:', oneDay[oneDay['meal'] == 'Dinner'].count()[0] / oneDay.count()[0])

'''
1e.
Mon Breakfast: 0.120164649871
Mon Lunch: 0.515572307082
Mon Dinner: 0.364263043047
Tues Breakfast: 0.119837575517
Tues Lunch: 0.516440526889
Tues Dinner: 0.363721897593
Wed Breakfast: 0.119901547117
Wed Lunch: 0.514466546112
Wed Dinner: 0.365631906771
Thur Breakfast: 0.122454111139
Thur Lunch: 0.516067387478
Thur Dinner: 0.361478501383
Fri Breakfast: 0.121418284749
Fri Lunch: 0.520037741471
Fri Dinner: 0.35854397378
'''


##  (f) Identify all stores with average order fill time 2 standard 
##      deviations below the mean average fill time for the 892 stores. 
##      (These are the high performing stores.) Similarly, identify all 
##      stores with average order fill time 2 standard deviations above 
##      the mean average fill time for the 892 stores. (These are the 
##      low performing stores.). For each, sort the store number from 
##      smallest to largest.
##      Note: Here the standard deviation is of the set of 892 store
##      averages, not of the 100,288 separate order times.

#Group stores by their number and take mean seconds
storeMeans = ffData.groupby(ffData['storenum'])['secs'].mean()
#Mean and std dev of  means
stdMean = storeMeans.std(ddof=1)
avgMean = storeMeans.mean()
#Extract stores beyond two stdevs
lowPerfMean = storeMeans[storeMeans <= avgMean - 2*stdMean]
highPerfMean = storeMeans[storeMeans >= avgMean + 2*stdMean]
print("High Performing Stores:\n", lowPerfMean)
print("Low Performing Stores:\n", highPerfMean)

'''
1f.
High Performing Stores:
 storenum
27     184.487179
43     188.419643
53     188.631148
122    180.400000
201    185.615385
243    173.637931
312    187.411765
500    187.403509
511    175.470000
514    184.151786
550    180.363636
570    183.800000
651    186.946429
699    186.082192
722    188.973451
852    189.460674
859    187.463158
Name: secs, dtype: float64
Low Performing Stores:
 storenum
30     247.413534
47     245.446809
59     244.228571
128    247.854167
149    254.926316
154    247.103774
155    244.339130
231    255.208696
233    245.375000
281    249.500000
318    245.991453
387    248.477064
392    245.058252
402    246.212598
422    254.519231
452    243.153846
474    243.724771
528    250.406250
614    243.913793
621    250.213592
657    264.463918
718    248.175000
723    248.692308
725    245.333333
726    244.935780
887    250.571429
Name: secs, dtype: float64
'''


##  (g) Some stores claim that using the mean is unfair due to outliers.
##      Repeat part (f) using the median in place of the mean, and determine
##      which stores (if any) are in both "high performing" groups or both
##      "low performing" groups.

#Group by storenums and find median seconds value for each
storeMedians = ffData.groupby(ffData['storenum'])['secs'].median()
#Find mean and std dev for medians
avgMed = storeMedians.mean()
stdMed = storeMedians.std(ddof=1)
#Extract stores beyond two std devs
lowPerfMedian = storeMedians[storeMedians <= avgMed - 2*stdMed]
highPerfMedian = storeMedians[storeMedians >= avgMed + 2*stdMed]
print("High Performing Stores:\n", lowPerfMedian)
print("Low Performing Stores:\n", highPerfMedian)

#Find indexes where each group intersects, then get those indexes
print("High Intersections:", lowPerfMedian[lowPerfMedian.index.intersection(lowPerfMean.index)])
print("Low Intersections:", highPerfMedian[highPerfMedian.index.intersection(highPerfMean.index)])

'''
1g.
High Performing Stores:
 storenum
27     141.0
243    136.5
312    140.5
722    141.0
Name: secs, dtype: float64
Low Performing Stores:
 storenum
14     190.0
59     200.0
130    187.0
149    209.0
161    193.0
173    187.5
200    187.0
233    201.0
240    192.0
242    193.0
267    188.5
290    191.0
304    194.0
318    188.0
320    187.5
365    191.0
402    188.0
438    193.0
448    191.0
452    191.0
478    190.0
517    188.0
528    187.0
531    187.5
546    191.0
568    190.5
611    188.0
640    189.0
657    233.0
702    191.0
718    191.5
723    187.0
725    190.0
726    196.0
755    188.0
796    192.0
875    200.0
887    192.0
Name: secs, dtype: float64
High Intersections: storenum
27     141.0
243    136.5
312    140.5
722    141.0
Name: secs, dtype: float64
Low Intersections: storenum
59     200.0
149    209.0
233    201.0
318    188.0
402    188.0
452    191.0
528    187.0
657    233.0
718    191.5
723    187.0
725    190.0
726    196.0
887    192.0
Name: secs, dtype: float64
'''

#### Part 2
##
## The questions in Part 2 refer to the data in the file
## 'fastfood3.csv'.  This file has the columns in 'fastfood2.csv'
## plus a new column 'satisfaction'.  This new column gives the
## customer's satisfaction on a scale of 1-10 (10 being most satisfied)

#Read in inital csv
ffData = pd.read_csv('fastfood3.csv')
#print(ffData)

##  (a) What percentage of customers gave the highest possible satisfaction 
#       rating?  What percentage gave the lowest rating?

#Divide total max/min satisfied by total customers
print("Highest:", ffData[ffData['satisfaction'] == 10].count()[0]  / ffData.count()[0] * 100, '%',sep="")
print("Lowest:", ffData[ffData['satisfaction'] == 1].count()[0]  / ffData.count()[0] * 100, '%',sep="")

'''
2a.
Highest:0.129626675175%
Lowest:0.0049856413529%
'''

##  (b) Determine the mean satisfaction for each day of the week.

#For each day from above, find mean satisfaction for that day by grouping by dayofweek
for day in week:
	print(day + ":", ffData['satisfaction'].groupby(ffData['dayofweek']).mean()[day])

'''
2b.
Mon: 6.13201745685
Tues: 6.1421214222
Wed: 6.14175205947
Thur: 6.11858184561
Fri: 6.11615434275
'''

##  (c) The company considers a satisfaction rating of 7 or higher 
##      to indicate a "satisfied" customer.  Find a 95% confidence interval
##      for the proportion of satisfied customers for each of Breakfast,
##      Lunch, and Dinner.  

#For each meal from above
for meal in meals:
	#Total meals of givel type
	n = ffData[ffData['meal'] == meal].count()[0]
	#Customers of that meal and satisfied / n
	p_ = ffData[(ffData['meal'] == meal) & (ffData['satisfaction'] >= 7)].count()[0] / n
	print(meal + ":", (p_ - 1.96 * np.sqrt((p_ * (1 - p_)) / n), p_ + 1.96 * np.sqrt((p_ * (1 - p_)) / n)))

'''
2c.
Breakfast: (0.54399335890671141, 0.56170441153094353)
Lunch: (0.35876723189754983, 0.3670488720386676)
Dinner: (0.43303525024777823, 0.44323272127268798)
'''

##  (d) The company suspects that the time required to fill an order can
##      influence customer satisfaction.  Find a 95% confidence interval
##      for the proportion of satisfied customers among those whose orders
##      took no more than 180 seconds to fill.  Do the same for those
##      whose orders took at least 360 seconds to fill.

#Note: I am assuming that this is the proportion of orders under 180 for which customers are satisfied
# The question could be interpreted as the proportion of satisfied customers that are also under 180s
# to do it this way you would  just change n to be all the orders that are satisfied

#Total number of customers under 180
n = ffData[ffData['secs'] <= 180].count()[0]
#Proportion that were also satisfied
p_ = ffData[(ffData['secs'] <= 180) & (ffData['satisfaction'] >= 7)].count()[0] / n
print("Less than 180:", (p_ - 1.96 * np.sqrt((p_ * (1 - p_)) / n), p_ + 1.96 * np.sqrt((p_ * (1 - p_)) / n)))
#Total number of satisfied customers
n = ffData[ffData['secs'] >= 360].count()[0]
#Proportion that also took more than 360
p_ = ffData[(ffData['secs'] >= 360) & (ffData['satisfaction'] >= 7)].count()[0] / n
print("More than 360:", (p_ - 1.96 * np.sqrt((p_ * (1 - p_)) / n), p_ + 1.96 * np.sqrt((p_ * (1 - p_)) / n)))

'''
2d.
Less than 180: (0.53217460518638282, 0.54038739287204096)
More than 360: (0.1024361195473813, 0.11139622888772485)
'''

##  (e) Company analysts have developed a formula for predicting customer
##      satisfaction ratings.  It is
##
##         predicted satisfaction= 4 + 0.002*cost - 0.005*secs + m,
##
##      where m = 1 if the meal is Breakfast, and 0 otherwise.
##
##      Predict each customer's satisfaction based on this formula, and
##      add this prediction as a new column on the data frame named
##      "predsatis".  Then compute the mean predicted rating.

#Function to apply formula to row
def prediction(row):
	return 4 + .002 * row['cost'] - .005 * row['secs'] + (1 if row['meal'] == 'Breakfast' else 0)
#Define new column as dataframe with  prediction function applied to each row (axis 1)
ffData['predsatis'] = ffData.apply(prediction, axis=1)
print("Mean predicted:", ffData.mean()['predsatis'])

'''
2e.
Mean predicted: 3.85851251396
'''


##  (f) For all the customers, find the maximum difference between the 
##      predicted satisfaction rating and the actual satisfaction rating.
##      (This should be the absolute value of the difference.)  Do the same
##      for the minimum difference, and then find the average of all the
##      differences.

print("Max:", abs(ffData['predsatis'] - ffData['satisfaction']).max())
print("Min:", abs(ffData['predsatis'] - ffData['satisfaction']).min())
print("Mean Difference", abs(ffData['predsatis'] - ffData['satisfaction']).mean())

'''
2f.
Max: 4.896
Min: 0.0
Mean Difference 2.27289870174
'''