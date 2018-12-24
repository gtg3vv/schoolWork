## File: Assignment07.py (STAT 3250)
## Topic: Assignment 07
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import pandas as pd
import numpy as np

#Read file into series of  lines
lines = pd.Series(open('pizza_requests.txt').read().splitlines())

#1. What proportion of requests were successful? (The requester received pizza.)

#Find n based on line common to all entries
n = len(lines[lines.str.contains("giver_username_if_known")])
#Check lines that received pizza and divide by n
print(len(lines[lines.str.contains('"requester_received_pizza", true')]) / n)

'''
1.
0.24634103332745547
'''

#2. Find the median account age at the time of request for all requests.

#Find line containing age, split to find number and cast to float
ages = lines[lines.str.contains('"requester_account_age_in_days_at_request"')].str.split(", ").str[1].astype(float)
#Take median age
medAge = ages.median()
print(medAge)

'''
2.
155.6475925925926
'''

#3. Divide the requests into those with account age greater than the median found in the previous question,
# and those with account age less than or equal to the median. Find a 95% confidence interval for the
# difference in proportion of successful pizza requests between the two groups. The formula is
# pˆ1 − pˆ2 ± 1.96s
# pˆ1(1 − pˆ1)
# n1
# +
# pˆ2(1 − pˆ2)
# n2
# where ˆp1 is the proportion of successful requests among older accounts (age greater than the median
# age), n1 is the number of older accounts, and ˆp2 and n2 are the same for the newer accounts.

#Take ages from above above median age
older = ages[ages > medAge]
#Take indexes and offset by thirteen to get corresponding pizza_request line
successfulOlder = lines[older.index + 13]
#All requests from above that were successful
successfulOlder = successfulOlder[successfulOlder.str.contains("true")]

#Take ages at or below median age
younger = ages[ages <= medAge]
#Take indexes and offset by thirteen to get corresponding pizza_request line
successfulYounger = lines[younger.index + 13]
#All requests from above that were successful
successfulYounger = successfulYounger[successfulYounger.str.contains("true")]

#Set up proportions
n1 = len(older)
n2 = len(younger)
p1 = len(successfulOlder) / n1
p2 = len(successfulYounger) / n2

difference = p1 - p2
#Plug into formula and add to difference
upperBound = difference + 1.96 * np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
lowerBound = difference - 1.96 * np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
#Print as tuple
print((lowerBound, upperBound))

'''
3.
(0.021770947082183623, 0.066570682209140045)
'''

#4. Determine the percentage of request texts that mention the word “student” or “children”. (Upper or
#lower case.)

#Get all lines that contain text and force lowercase
requests = lines[lines.str.contains('"request_text"')].str.lower()
#Get request lines that match keyword
matchingRequests = requests[requests.str.contains("student") | requests.str.contains("children")]
#Print as percent
print(len(matchingRequests) / n * 100, "%",sep="")

'''
4.
9.222359372244753%
'''

#5. Determine the number of requests from Canada
#Get request title lines and force lowercase
requests = lines[lines.str.contains('"request_title"')].str.lower()
#Check lines from those that also contain keyword
matchingRequests = requests[requests.str.contains("canada")]
print(len(matchingRequests))

'''
5.
103
'''

#6. Find a 95% confidence interval for the proportion of successful pizza requests donated anonymously
#Get  all successful pizza lines
successful = lines[lines.str.contains('"requester_received_pizza", true')]
#get index and shift by -23 to get username line from corresponding request
successfulAnon = lines[successful.index - 23]
#Check if those lines are  anonymous
successfulAnon = successfulAnon[successfulAnon.str.contains('"giver_username_if_known", "N/A"')]

n_  = len(successful)
p_ = len(successfulAnon) / n_

#Plug into formulas and print range as a tuple
upperBound = p_ + 1.96 * np.sqrt(p_*(1-p_)/n_)
lowerBound = p_ - 1.96 * np.sqrt(p_*(1-p_)/n_)
print((lowerBound, upperBound))

'''
6.
(0.68996720497778263, 0.73737710425629033)
'''

#7. Find the maximum number of subReddits subscribed to by a single requestor.
#Find index of lines that show start of reddit  lists
startReddits = lines[lines.str.contains('"requester_subreddits_at_request", {')]
#Find index of lines that show end of reddit lists
endReddits = lines[lines.str.contains('"requester_upvotes_minus_downvotes_at_request"')]
#Subtract indexes to find num reddits, -2 to account for closing brace
print(max(endReddits.index - startReddits.index) - 2)

'''
7.
235
'''

# 8. Determine the number of distinct subReddits among all the requests, and the number of times that
# each appears. Place a table of the 10 most frequently occurring (in order, starting with most frequent)
# in your Python code file, organized

#Find all lines that don't contain anything but letters and "" 
#Remove the quotes to clean up output
reddits = lines[lines.str.startswith('  "')]
reddits = reddits.str.replace('"',"").str.replace(" ","").str.lower()
#Count occurences of each value and print first ten
print(reddits.value_counts()[:10])
#Send values to csv with correct name
reddits.value_counts().to_csv("gtg3vv-assignment07-subreddits.txt")

'''
8.
AskReddit               3241
pics                    2734
funny                   2704
IAmA                    2138
WTF                     2133
gaming                  2079
Random_Acts_Of_Pizza    1978
videos                  1620
todayilearned           1556
AdviceAnimals           1452
'''
