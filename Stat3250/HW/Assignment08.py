## File: Assignment08.py (STAT 3250)
## Topic: Assignment 08
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

## The focus of this assignment is dates.  Not the fruit, but the time
## and date that data is put into a file.

## 1. The questions below require the data frame 'reviews.txt' that
##    is described in the README_assign08.txt file.  You can use the
##    code below to read in the data as a dataframe.

import pandas as pd # load pandas as pd
import datetime

#Read in csv file, tab separated and label the columns
reviews = pd.read_csv('reviews.txt', 
                        sep='\t',
                        header=None,
                        names=['Reviewer','Movie','Rating','Date'])

##  (a) Find the date and time of the oldest review, and the 
##      most recent review.  Give the result in the form
##      matching "2016-10-18 17:50:43".  (Times UTC)

#Get date column and find min
oldest = reviews['Date'].min()
#Convert value to datetime object and then format to year-month-day hour:min:sec
print("Oldest:", pd.to_datetime(oldest, unit='s').strftime("%Y-%m-%d %H:%M:%S"))
#Get date column and find max
newest = reviews['Date'].max()
#Convert value to datetime object and then format to year-month-day hour:min:sec
print("Newest: ", pd.to_datetime(newest, unit='s').strftime("%Y-%m-%d %H:%M:%S"))

'''
1a.
Oldest: 1997-09-20 03:05:10
Newest:  1998-04-22 23:10:38
'''

##  (b) Determine the median date and time for the reviews.
##      Give the result in the form "Tuesday October 18 2016 17:50:43"
##      (Times UTC)

#Get date column and  find median
medDate = reviews['Date'].median()
#Convert value to datetime object and then format Weekday Month Day Year Hr:Min:sec
print(pd.to_datetime(medDate, unit='s').strftime("%A %B %d %Y %H:%M:%S"))

'''
1b.
Monday December 22 1997 21:42:24
'''

##  (c) Find the average rating for each month of the year.

#Convert date column of reviews to a datetime and format to just contain Month
#Use those values to group reviews
#Find means of grouped values and get rating column
print(reviews.groupby(pd.to_datetime(reviews['Date'],unit='s').dt.strftime("%B")).mean()['Rating'])

'''
1c.
Date
April        3.574848
December     3.580388
February     3.455009
January      3.397730
March        3.548831
November     3.559842
October      3.591421
September    3.540125
Name: Rating, dtype: float64
'''

##  (d) Determine which day of the week produced the most reviews.

#Convert date column to datetime object and format to contain only Weekdays
#Count unique values
values = pd.to_datetime(reviews['Date'],unit='s').dt.strftime("%a").value_counts()
#Get index of max value b/c weekdays are index
maxDay = values.idxmax()
#Print day with max and corresponding max value
print(maxDay, values[maxDay])

'''
1d.
Wed 16621
'''

##  (e) Determine the date and time of the first review for the 5 reviewers 
##      who had the most reviews.

#Group reviews by reviewer column and count occurences of each reviewer
byReviewer = reviews.groupby(reviews['Reviewer']).count()
#Take the counts for the reviews and sort them descending and get the indexes of those values
indexes = byReviewer.sort_values('Movie',ascending=False).index
#Get all the reviews where the reviewer is in the indexes found above (top 5)
#Group the reviews for just the top 5 by reviewer
#Find the min of the date column for each and format the date correctly
print(pd.to_datetime(reviews[reviews['Reviewer'].isin(indexes[:5])].groupby('Reviewer').min()['Date'],unit='s').dt.strftime("%Y-%m-%d %H:%M:%S"))

'''
1e.
Reviewer
13     1997-12-07 17:11:23
276    1997-09-20 20:12:17
405    1998-01-23 08:37:15
450    1997-12-15 19:53:37
655    1998-02-14 02:52:00
Name: Date, dtype: object
'''

## 2. The questions below require the file 'pizza_requests.txt' seen 
##    previously.  All questions refer to the date and time given in 
##    the variable "unix_timestamp_of_request_utc" for each request.

#Read in as series by separating at newline
lines = pd.Series(open('pizza_requests.txt').read().splitlines())

##  (a) Find the date and time of the oldest request, and the 
##      most recent request.  Give the result in the form
##      matching "2016-10-18 17:50:43".  (Times UTC)

#Isolate series lines containing timestamp
dateLines = lines[lines.str.contains("unix_timestamp_of_request_utc")]
#Get the section containing the actual epoch by splitting at comma and gettin second part
#Convert epochs to datetime and find min/max
dateLines = pd.to_datetime(dateLines.str.split(', ').str[1],unit='s')
print("Newest: ", dateLines.max())
print("Oldest: ", dateLines.min())

'''
2a.
Newest:  2013-10-12 01:30:36
Oldest:  2011-02-14 22:28:57
'''

##  (b) Determine the median date and time for the requests.
##      Give the result in the form "Tuesday October 18 2016 17:50:43"
##      (Times UTC)

#Get lines containing timestamp and just get epoch
epochLines =  lines[lines.str.contains("unix_timestamp_of_request_utc")].str.split(', ').str[1]
#Get median of epochs, convert to datetime and formate appropriately 
print(pd.to_datetime(epochLines.median(),unit='s').strftime("%A %B %d %Y %H:%M:%S"))

'''
2b.
Friday July 20 2012 17:54:08
'''

##  (c) Determine the number of requests for each hour of the day.  Report
##      the 5 one-hour periods with the most requests, and the number of
##      requests for each.

print("Hour   Requests")
#Group datelines from above by converting to date object containing only hour
#Count occurences of each hour and sort to find top
#Slice first 5 requests
print(dateLines.groupby(dateLines.dt.strftime("%H")).count().sort_values(ascending=False)[:5])

'''
2c.
Hour   Requests
00    508
22    497
23    491
21    464
01    441
dtype: int64
'''

##  (d) Find the hour of the day that resulted in the highest proportion
##      of successful pizza requests.

#Get lines that indicate success and split to get True/False Value
pizzaLines = lines[lines.str.contains("requester_received_pizza")].str.split(', ').str[1]
#Make new dataframe with times column by taking datelines from above and formatting to just contain hour
#Take all true false values and put in success column
#Indexes match in final dataframe b/c values in supplied dict are same length
timeFrame = pd.DataFrame(data = {'times':dateLines.dt.strftime("%H"), 'success':pizzaLines.values})

#Take success values and group first by success, then by time
#Now have each hour divided into true and false groups
#Count all occurences and just take true values - we want proportion of successful requests
successfulByHour= timeFrame['success'].groupby([timeFrame['success'], timeFrame['times']]).count()['true ']
#Group success values just by time. We want total requests by hour and don't care about success
allByHour = timeFrame['success'].groupby(timeFrame['times']).count()

#Divide group containing success counts for each hour by all requests for each hour to get proportion successful for each hour
proportionByHour = successfulByHour / allByHour
#The hour is the index - so get index with max value
print("Most successful hour: ", proportionByHour.idxmax())

'''
2d.
13
'''

##  (e) Repeat (d), this time finding the hour with the lowest success rate.

#The hour is the index - so get index with min value using above proportions
print("Least successful hour:", proportionByHour.idxmin())

'''
2e.
08
'''