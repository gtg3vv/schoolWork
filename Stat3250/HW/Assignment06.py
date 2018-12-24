## File: assignment06.py (STAT 3250)
## Topic: Assignment 6
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2


# The file "timing_log.txt" contains a log of all WeBWorK
# log entries on April 1, 2012.  The entries are organized 
# by line, with each line including the following:
#
#  --the date and time of the entry
#  --a number that is related to the user (but not unique)
#  --something that appears to be the epoch time stamp
#  --a hyphen
#  --the WeBWorK element that was accessed
#  --the "runTime" required to process the problem
#
# Answer the questions below based on "timing_log.txt".
#

#Read in initial file and split on spaces
fileLines = []
with open("timing_log.txt", 'r') as f:
    for line in f:
        fileLines.append(line.split())

# 1. How many log entries were for requests for a PDF version of an
#    assignment?  Those are indicated by "hardcopy" appearing in the 
#    WeBWorK element

hardcopies = 0
#Iterate through list of lines
for line in fileLines:
    #If section containing webwork also says hardcopy, increase count
    if 'hardcopy' in line[8]:
        hardcopies += 1
print("Num Hardcopies:", hardcopies)

'''
1.
Num Hardcopies: 138
'''

# 2. What percentage of log entries were for STAT 2120?

statCount = 0
#Iterate through list of lines
for line in fileLines:
    #Check if line matches class
    if 'STAT2120' in line[8]:
        statCount += 1
print("Percent Stat 2120: ", statCount/len(fileLines) * 100,"%",sep="")

'''
2.
Percent Stat 2120: 52.49243925331108%
'''

# 3. Find the percentage of log entries that came from the student's
#    initial log in.  For those, the WeBWorK element has the form
#
#          [/webwork2/ClassName]
#
#    where "ClassName" is the name of a class.

initialCount = 0
for line in fileLines:
    #Iterate through list of lines
    splitWork = line[8].split('/')
    #If line  has proper number of slashes and there is  something other than square brace following last slash
    if len(splitWork) == 3 and len(splitWork[2]) > 1:
        initialCount += 1
    #Also need to account for entries with a trailing slash
    elif len(splitWork) == 4 and splitWork[3] == "]":
        initialCount += 1
print("Initial logins: ", initialCount/len(fileLines) * 100,"%",sep="")

'''
3. 
Initial logins: 3.792105537595161%
'''

# 4. How many log entries were from instructors performing administrative
#    tasks?  Those are indicated by "instructor" in the 3rd position of
#    the WeBWorK element.

instCount = 0
#Iterate through list of lines
for line in fileLines:
    splitWork = line[8].split('/')
    #If there are enough sections to webwork and instructor in right position, count + 1
    if len(splitWork) > 3 and splitWork[3] == 'instructor':
        instCount += 1
print("Instructor tasks:", instCount)

'''
4. 
Instructor tasks: 295
'''

# 5. Which hour of the day had the most log entries?  Which had the least?

hours = {}
#Iterate through list of lines
for line in fileLines:
    #Split time to get hour
    hour = line[3].split(":")[0]
    #If hour already in dictionary, increment
    if hour in hours:
        hours[hour] += 1
    #Otherwise add it
    else:
        hours[hour] = 1
print("Most entries:", max(hours, key=hours.get))
print("Least entries:", min(hours, key=hours.get))

'''
5. 
Most entries: 22
Least entries: 06
'''

# 6. How many different classes use the system? (Treat each
#    different name as a different class, even if there is
#    more than one section.  Multiple sections with a single shared 
#    WeBWorK presence is a single class.)

classes = []
#Iterate through list of lines
for line in fileLines:
    #Divide each section of webwork
    splitWork = line[8].split('/')
    #Check there are enough sections to include class
    if len(splitWork) > 2:
        #Get rid of curly brace
        splitWork[2] = splitWork[2].strip(']')
        #If class isn't blank, add it
        if len(splitWork[2]) > 0:
            classes.append(splitWork[2])
#Cast to set to eliminate duplicates
print("Classes:", len(set(classes)))

#Note: I chose to include admin as a class because it followed the same format and was unspecified

'''
6. 
Classes: 40
'''

# 7. Which 3 classes had the most use?  Answer this two ways:

classes = {}
#Iterate through list  of lines
for line in fileLines:
    #Divide each section of webwork
    splitWork = line[8].split('/')
    if len(splitWork) > 2:
        #Get section for  class and remove brackets
        splitWork[2] = splitWork[2].strip(']')
        #Add new classes to dict as a list containing each value
        if splitWork[2] not in classes and len(splitWork[2]) > 0:
            classes[splitWork[2]] = [1,float(line[11])]
        #Update existing classes in dict
        elif splitWork[2] in classes:
            classes[splitWork[2]][0] += 1
            classes[splitWork[2]][1] += float(line[11])
            
#Get list of tuples representing key value pairs from dictionary (key, [val1,val2])
#Sort in reverse order by first item of list value - listitem[value][0]
byNum = sorted(list(classes.items()), key=lambda x:x[1][0], reverse=True)
#Sort in reverse order by second item of list value - listitem[value][1]
byTime = sorted(list(classes.items()), key=lambda x:x[1][1], reverse=True)
#    (a) Based on the number of entries in the log file
# Access the first part  of each tuple to just get the class name
print("Top three classes by entries:")
print(byNum[0][0], byNum[1][0], byNum[2][0])
#    (b) Based on the total "runTime" required.
print("Top three classes by runtime:")
print(byTime[0][0], byTime[1][0], byTime[2][0])

'''
7a. 
Top three classes by entries:
Spring11-STAT2120 Spring12-STAT2120 Spring11-APMA2130-Fulgham
7b. 
Top three classes by runtime:
Spring11-STAT2120 Spring11-APMA2130-Fulgham Spring12-APMA2130
'''

# 8. Determine which 3 classes had the largest average "runTime".  Report
#    the classes and their runTime.

#Use dictionary from above, cast to list of tuples, sort by dividing second part of value tuple by first
#Also sorts in reverse order
byAvg = sorted(list(classes.items()), key=lambda x:x[1][1]/x[1][0], reverse=True)

#Access first  three list items, divide the second pard of tuple by first (runtime / n)
print("Class:", byAvg[0][0], "Avg: ", byAvg[0][1][1] / byAvg[0][1][0])
print("Class:", byAvg[1][0], "Avg: ", byAvg[1][1][1] / byAvg[1][1][0])
print("Class:", byAvg[2][0], "Avg: ", byAvg[2][1][1] / byAvg[2][1][0])

'''
8. 
Class: APMA2120-Devel Avg:  0.5334690265486726
Class: apma2130-devel Avg:  0.3876734693877551
Class: Spring12-APMA2130 Avg:  0.34805043149946097
'''

# 9. Determine the percentage of log entries that were accessing a problem.  
#    For those, the WeBWorK element has the form
#
#           [/webwork2/ClassName/AssignmentName/Digit/]
#
#    where "ClassName" is the name of the class, "AssignmentName" the
#    name of the assignment, and "Digit" is a positive digit.

countProblems = 0
#Iterate through list of lines
for line in fileLines:
    #Divide up sections of webwork
    splitWork = line[8].split('/')
    #Check there are  enough sections to include assignment number and that it is actually a number
    if len(splitWork) > 5 and str.isdigit(splitWork[4]):
        countProblems += 1
print("Problem accesses: ", countProblems/len(fileLines) * 100, "%",sep="")

'''
9. 
Problem accesses: 78.5079257482532%
'''

# 10. Find the WeBWorK problem that had the most log entries,
#     and the number of entries.  If there is a tie, list all with the most.
#     (Note: The same problem number from different assignments represents
#     different WeBWorK problems.)

problems = {}
#Iterate through list of lines
for line in fileLines:
    #Divide up sections of webwork
    splitWork = line[8].split('/')
    #Check there are enough sections to include assignment number and that it is actually a number
    if len(splitWork) > 5 and str.isdigit(splitWork[4]):
        #Remove open and closing  brackets
        line = line[8].strip('[').strip(']')
        #If new problem set count to one
        if line not in problems:
           problems[line] = 1
        #Otherwise increment
        else:
            problems[line] += 1
            
#Cast to list of tuples, sort by value part of (key, value) tuple
byCount = sorted(list(problems.items()), key=lambda x:x[1], reverse=True)
print("Problem:", byCount[0][0], "Entries:", byCount[0][1])

'''
10. 
Problem: /webwork2/Spring11-STAT2120/Webwork09/22/ Entries: 1215
'''

#%%