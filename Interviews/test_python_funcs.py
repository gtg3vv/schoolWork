import math
import numpy as np

def E(data, func= lambda x: math.pow(x,1)):
	count = 0.0
	sum = 0.0
	list1 = []
	list2 = []
	for val in np.nditer(data):
		sum += func(val)
		count += 1
	return sum/count

def var(data, func= lambda x: math.pow(x,1)):
	mu = E(data)
	expected_sq = E(data, func= lambda x: pow(x,2))
	return (expected_sq - mu**2)

#Read in csv files
#Changed data to uint16 to avoid integer overflow problems. In the existing 
#implementation it would not satisfy and of the the linearity contraints.
red = np.loadtxt("red.csv",dtype = np.uint16, delimiter = ",")
blue = np.loadtxt("blue.csv",dtype = np.uint16, delimiter = ",")

#Python also has a unittest framework. I chose not to use it here for the purposes
#of more easily checking the few conditions.

#Test each linear condition in turn on red and blue csvs
#The last test fails
def testLinearity(expected):
	isValid = True
	isValid = expected(red)+5 == expected(red+5)
	isValid = isValid and expected(blue)+5 == expected(blue+5)
	isValid = isValid and (expected(red+blue) == expected(red) + expected(blue))
	isValid = isValid and ((expected(red) * 5) == expected(red*5))
	return isValid

#Test each variance condition on red and blue
#The multiplication tests fail
def testVariance(variance):
	isValid = True
	
	isValid = isValid and variance(5 * red) == 25 * variance(red)
	isValid = isValid and variance(red + 5) == variance(red)
	isValid = isValid and variance(5 * red + 5) == 25 * variance(red)
	
	isValid = isValid and variance(3 * blue) == 9 * variance(blue)
	isValid = isValid and variance(blue + 3) == variance(blue)
	isValid = isValid and variance(3 * red + 2) == 9 * variance(blue)
	
	return isValid

	
#Referred to given numpy link and rest of numpy api

