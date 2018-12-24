import os
from Crypto.Hash import SHA256
from Crypto.Hash import MD5

userPairs = {}

newUser = str(input("Enter a username and password separated by space: "))

while(newUser != ""):
    newUser = newUser.split()
    userPairs[newUser[0]] = SHA256.new(str.encode(newUser[1])).hexdigest()
    newUser = str(input("Enter a username and password separated by space: "))
    
testUser = input("Enter a username and password: ")

while (testUser != ""):
    testUser = str(testUser).split()
    print(userPairs, testUser)
    if (testUser[0] not in userPairs):
        print("User not found")
    elif (userPairs[testUser[0]] == SHA256.new(str.encode(testUser[1])).hexdigest()):
        print("Valid login")
    else:
        print("Invalid login")
        
    testUser = input("Enter a username and password: ")
        