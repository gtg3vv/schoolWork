from gradetools import grader, student, test_func


correct = 0
mod = 'salary'
func = 'report'
try:
    correct += test_func(mod, func, {'title': 'President - University of Virginia', 'breakdown': {'Base salary': 188617.0, 'Additional compensation': 4100.0, 'Non-state salary': 346083.0, 'Deferred compensation': 180000.0}, 'rank': 1, 'pay': 733800.0}, None, ['Sullivan, Teresa'], full=True)
    correct += test_func(mod, func, {'title': 'President - University of Virginia', 'breakdown': {'Base salary': 188617.0, 'Additional compensation': 4100.0, 'Non-state salary': 346083.0, 'Deferred compensation': 180000.0}, 'rank': 1, 'pay': 733800.0}, None, ['Teresa Sullivan'])
    correct += test_func(mod, func, {'title': 'President - University of Virginia', 'breakdown': {'Base salary': 188617.0, 'Additional compensation': 4100.0, 'Non-state salary': 346083.0, 'Deferred compensation': 180000.0}, 'rank': 1, 'pay': 733800.0}, None, ['teresa-sullivan'])
    correct += test_func(mod, func, {'title': 'Multimedia Creative Technician', 'breakdown': {'Base salary': 41000.0}, 'pay': 41000.0}, None, ['151028368'])
    correct += test_func(mod, func, {'title': 'Research Scientist', 'breakdown': {'Base salary': 58500.0}, 'rank': 3976, 'pay': 58500.0}, None, ['Polanowska-Grabow, Renata'])
    correct += test_func(mod, func, {'title': 'Lab Specialist 3-LAB49', 'breakdown': {'Base salary': 60770.0}, 'rank': 3807, 'pay': 60770.0}, None, ['Ali Reza Forghani Esfahani'])
    correct += test_func(mod, func, {'title': 'Laboratory & Research Spec II', 'breakdown': {'Base salary': 58496.0}, 'rank': 3978, 'pay': 58496.0}
, None, ['pamela-neff'])
    correct += test_func(mod, func, {}, None, ['thomas-jefferson'])
    correct += test_func(mod, func, {'rank': 2992, 'pay': 75000.0, 'breakdown': {'Base salary': 75000.0}, 'title': 'Lecturer'}, None, ['luther-tychonievich'])
    correct += test_func(mod, func, {}, None, ['upsorn-praphamontripong'])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', correct, 'out of', 12, 'automated test cases')

grader('Score:', correct, '/', 12)

