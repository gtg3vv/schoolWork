from gradetools import test_func, student, grader, checkSource


correct = 0
mod = 'matchmaker'

fcor = 0
func = 'agreement'
try:
    fcor += test_func(mod, func, [], None, [[], []], full=True, sort=True)
    fcor += test_func(mod, func, [2], None, [(1, 2), (2, 3)], sort=True)
    fcor += test_func(mod, func, [1,3,2], None, [[0,1,2,3,4], [-1,1,3,5,2]], sort=True)
    fcor += test_func(mod, func, [1,3,2], None, [[1,2,3], [-1,1,3,5,2]], sort=True)
    fcor += test_func(mod, func, [1,3,2], None, [[0,1,2,3,4], [1,3,2]], sort=True)
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 7, 'automated test cases')

correct += fcor

fcor = 0
func = 'disagreement'
try:
    fcor += test_func(mod, func, [], None, [[], []], full=True, sort=True)
    fcor += test_func(mod, func, [1,3], None, [(1, 2), (2, 3)], sort=True)
    fcor += test_func(mod, func, [0,4,-1,5], None, [[0,1,2,3,4], [-1,1,3,5,2]], sort=True)
    fcor += test_func(mod, func, [-1,5], None, [[1,2,3], [-1,1,3,5,2]], sort=True)
    fcor += test_func(mod, func, [0,4], None, [[0,1,2,3,4], [1,3,2]], sort=True)
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 7, 'automated test cases')

correct += fcor

fcor = 0
func = 'compatibility'
try:
    fcor += test_func(mod, func, 1.0, None, [[1],[1]], full=True)
    fcor += test_func(mod, func, 1.0, None, [[1,3,2],[2,3,1]])
    fcor += test_func(mod, func, 0.0, None, [[-1,-3,-2],[2,3,1]])
    fcor += test_func(mod, func, 0.5, None, [[-1,3,2],[2,3,1]])
    fcor += test_func(mod, func, 0.375, None, [[1,3,2,4,5,6,7,8],[2,3,1]])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', fcor, 'out of', 7, 'automated test cases')

correct += fcor


if checkSource(mod, r'\bset\s*\('):
    student('used set(), sometimes a sign of code-by-google instead of code-with-understanding')
    correct -= 1



grader('Score:', correct, '/', 21)
