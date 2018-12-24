##
## File: assignment01.py (STAT 3250)
## Topic: Assignment 1
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

#### Assignment 1, Part A
##
## For the questions in this part, use the following
## lists as needed:
mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]

## A1. Find the last four digits of the 13th Mersenne
##     prime, which is equal to 2^521 - 1.

print(str(2**521 - 1)[-4:])

'''
# A1
7151
'''

## A2. Find the product of the 7th entry in mylist01,
##     the 13th entry in mylist01, and the 4th entry
##     in mylist02.

print(mylist01[6] * mylist01[12] * mylist02[3])

'''
# A2
-75
'''

## A3. Extract the sublist of mylist02 that goes from
##     the 5th to the 9th elements (inclusive).

print(mylist02[4:9])

'''
# A3
[-5, -2, 4, 6, 7]
'''

## A4. Concatenate mylist01 to mylist02, sort the new
##     combined list, then extract the sublist that 
##     goes from the 8th to the 19th elements (inclusive).


#Here I'm following the order he suggested in class that we should add list 2 on to the 
# end of list1. The question suggests the reverse, but he stated this in class.
newList = mylist01 + mylist02
print(sorted(newList)[7:19])

'''
# A4
[-3, -3, -2, -2, 0, 0, 1, 2, 2, 2, 3, 3]
'''

## A5. Determine the number of times 8 appears in the 
##     combined list in A4.

print(newList.count(8))

'''
#  A5
3
'''
        

## A6. Create a new list be removing all of the 3's from
##     mylist01.
newList2 = [i for i in mylist01 if i != 3]
print(newList2)

'''
# A6
[2, 5, 4, 9, 10, -3, 5, 5, -8, 0, 2, 8, 8, -2, -4, 0, 6]
'''

## A7. Extract a sublist of mylist02 consisting of every
##     3rd entry, starting at the end and going in 
##     reverse.

print(mylist02[-1::-3])

'''
# A7
[1, 13, 9, 6, -5, -3]
'''

## A8. From the combined list in A4, extract a sublist of
##     every 5th entry, starting with the 3rd entry.

print(newList[2::5])

'''
# A8
[4, 5, 3, 0, -5, 7, 13]
'''

#%%

#### Assignment 1, Part B
##
## For the questions in this part, use the following
## lists as needed:
mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]

## B1. Use a for loop to add up the cubes of the entries
##     of mylist01.

cubeSum = 0
for i in mylist01:
    cubeSum += i**3
print(cubeSum)

'''
# B1
2867
'''

## B2. Use a for loop to create mylist03, which has 15
##     entries, each the product of the corresponding 
##     entry from mylist01 multiplied by the corresponding
##     entry from mylist02.  That is,
##     mylist03[i] = mylist01[i]*mylist02[i] 
##     for each 0 <= i <= 14.

mylist03 = []
for i in range(15):
    mylist03.append(mylist01[i]*mylist02[i])
print(mylist03)

'''
# B2
[-14, -15, 32, -45, -50, 6, 20, 30, 21, -40, 0, 20, 6, 104, -96]
'''
    

## B3. Use a for loop to compute the mean of the entries
##     of mylist02.  (Hint: len(mylist02) gives the number
##     of entries in mylist.  This is potentially useful.)

sum = 0 
for i in mylist02:
    sum += i
print(sum/len(mylist02))

'''
# B3
1.588235294117647
'''

#%%

#### Assignment 1, Part C
##
## For the questions in this part, use the following
## lists as needed:
mylist01 = [2,5,4,9,10,-3,5,5,3,-8,0,2,3,8,8,-2,-4,0,6]
mylist02 = [-7,-3,8,-5,-5,-2,4,6,7,5,9,10,2,13,-12,-4,1]
mylist03 = [2,-5,6,7,-2,-3,0,3,0,2,8,7,9,2,0,-2,5,5,6]
biglist = mylist01 + mylist02 + mylist03

## C1. Use a for loop to determine the number of entries
##     in "biglist" that are greater than 4.

n = 0
for i in biglist:
    n += i > 4
print(n)

'''
# C1
23
'''

## C2. Use a for loop to determine the number of entries
##     in "biglist" that are between -1 and 3 (inclusive).

n = 0
for i in biglist:
    n += -1 <= i <= 3
print(n)

'''
# C2
15
'''

## C3. Create a new list called "mylist04" that contains 
##     the elements of biglist that are not divisible by 3.

mylist04 = [x for x in biglist if x % 3 != 0]
print(mylist04)

'''
# C3
[2, 5, 4, 10, 5, 5, -8, 2, 8, 8, -2, -4, -7, 8, -5, -5, -2, 4, 7, 5, 10, 2, 13, -4, 1, 2, -5, 7, -2, 2, 8, 7, 2, -2, 5, 5]
'''

#%%








