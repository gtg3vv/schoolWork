import math


#Implements sieve of erastothenes. Checks odd numbers up to n by comparing
#to each prime in list up to sqrt(i). Primes above this are redundant
def find_primes(n):
    #Check value error to determine if int
    try:
        n = int(n)
    except ValueError:
        print("Please enter an integer")
        return
    if (n <= 0):
        print("Please enter a positive, nonzero integer")
        return
    
    if (n == 1):
        return []
    #Assume 2 prime
    primes = [2]
    #Checking each odd up to n
    for i in range(3,n+1,2):
        isPrime = True;
        for j in primes:
            #Break if divisible by any known primes
            if i % j == 0:
                isPrime = False
                break;
            #Don't check any primes above sqrt(i), it's redundant
            if j > math.sqrt(i):
                break;
        if isPrime:
            primes.append(i)
    return(primes)
    
#I implemented fib using the dynamic programming approach to ensure it was
#a linear time and linear space implementation. The space efficiency can be improved
#by only using two temporary values to compute the next member of the sequence,
#but this makes it impossible to store the whole sequence. There are existing
#log(n) implementations to find the nth fibonacci number, but those also do not
#store the sequence.
def fib(n):
    try:
        n = int(n)
    except ValueError:
        print("Please enter an integer")
        return
    if (n <= 0):
        print("Please enter a positive, nonzero integer")
        return
    
    sequence = [0,1]
    tempSum = sequence[-1] + sequence[-2]
    #Summing last to members of sequence
    while tempSum <=n:
        sequence.append(tempSum)
        tempSum = sequence[-1] + sequence[-2]
    return sequence
        
#Beginning with 11, skip by twos until you reach an even 10s digit and then skip 
#by ten. Ignore numbers divisble by 2(achieved above) or numbers divisble by 5.
def oddish_numbers(n):
    try:
        n = int(n)
    except ValueError:
        print("Please enter an integer")
        return
    if (n <= 0):
        print("Please enter a positive, nonzero integer")
        return
    
    oddishNums = []
    i = 11
    #Skip by 10 if even digit, by 2 otherwise
    #Ignore numbers ending in 5 because they are not relatively prime
    while len(oddishNums) < n:
        if i // 10 % 2 == 0:
            i+=10
            continue
        if i % 5 != 0:
            oddishNums.append(i)
        i+=2
    return oddishNums
        
#Did not refer to anything for this section