from gradetools import grader, student, test_func


correct = 0
mod = 'seive'
func = 'primes'
try:
    correct += test_func(mod, func, [2], None, [3], full=True)
    correct += test_func(mod, func, [2, 3, 5, 7], None, [10])
    correct += test_func(mod, func, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47], None, [50])
    correct += test_func(mod, func, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43], None, [47])
    correct += test_func(mod, func, [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199], None, [200])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', correct, 'out of', 7, 'automated test cases')
grader('Score:', correct, '/', 7)
