
from gradetools import grader, student, test_func


correct = 0
mod = 'credit_card'
func = 'check'
try:
    correct += test_func(mod, func, False, None, [1], full=True)
    for num in [5490123456789129, 5490123456789122, 54906789122]:
        correct += test_func(mod, func, False, None, [num])
    for num in [378282246310005, 6011111111111117, 5555555555554444]:
        correct += test_func(mod, func, True, None, [num])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', correct, 'out of', 9, 'automated test cases')
grader('Score:', correct, '/', 9)


