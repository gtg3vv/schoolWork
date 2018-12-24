import cacheurls
from gradetools import grader, student, test_func


correct = 0
mod = 'lous_list'
func = 'instructors'
try:
    correct += test_func(mod, func, ['', 'Alexander Klibanov', 'Brian Helmke', 'Craig Meyer', 'Eli Zunder', 'Farzad Hassanzadeh', 'Frederick Epstein', 'George Christ', 'Jason Papin', 'Jeffrey Holmes', 'Jennifer Munson', 'Kevin Janes', 'Mete Civelek', 'Michael Lawrence', 'Richard Price', 'Shayn Peirce-Cottler', 'Steven Caliari', 'Timothy Allen', 'William Guilford', 'William Levy'], None, ['BME'], full=True)
    correct += test_func(mod, func, ['Andrew Koch'], None, ['MUBD'])
    correct += test_func(mod, func, ['Christopher Berk', 'Paul Morrow'], None, ['PPL'])
    correct += test_func(mod, func, ['Aaron Bloomfield', 'Abdeltawab Hendawi', 'Ahmed Ibrahim', 'Alfred Weaver', 'Andrew Grimshaw', 'Baishakhi Ray', 'Cameron Whitehouse', 'Charles Reiss', 'Collin/Cyrus', 'Connelly Barnes', 'Craig Dill', 'David Edwards', 'David Evans', 'Dimitrios Diochnos', 'Gabriel Robins', 'Haiying Shen', 'Homa Alemzadeh', 'Hongning Wang', 'Jack Davidson', 'James Cohoon', 'John Stankovic', 'Kai-Wei Chang', 'Katherine Holcomb', 'Kevin Angstadt', 'Kevin Sullivan', 'Kong-Cheng Wong', 'Lu Feng', 'Luther Tychonievich', 'Mark Floryan', 'Mark Sherriff', 'Marty Humphrey', 'Mary Smith', 'Mohammad Mahmoody Ghidary', 'Nada Basit', 'Samira Khan', 'Thomas Hall', 'Thomas Horton', 'Thomas Pinckney', 'Upsorn Praphamontripong', 'Vicente Ordonez-Roman'], None, ['CS'])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', correct, 'out of', 6, 'automated test cases')

oc = correct
correct = 0

func = 'class_search'
try:
    correct += test_func(mod, func, [], None, ['MUBD'], full=True)
    correct += test_func(mod, func, [['MUBD', '2601', '001', 'Basketball Band', 'Andrew Koch', 'Lecture', '1', 'false', 'true', 'false', 'true', 'false', '1800', '2000', 'TBA', '113', '100']], None, ['MUBD', False])
    correct += test_func(mod, func, [['GREE', '2020', '001', 'Intermediate Greek II', 'Jon Mikalson', 'Lecture', '3', 'true', 'false', 'true', 'false', 'true', '1000', '1050', 'Cocke Hall 115', '14', '20'], ['GREE', '2240', '001', 'The New Testament II', 'Andrej Petrovic', 'Lecture', '3', 'true', 'false', 'true', 'false', 'true', '1200', '1250', 'Cocke Hall 101', '8', '20']], None, ['GREE', False, 2000])
    correct += test_func(mod, func,  [['GREE', '1020', '102', 'Elementary Greek', 'Brett Evans', 'Discussion', '0', 'false', 'true', 'false', 'true', 'false', '1230', '1345', 'Monroe Hall 113', '5', '18'], ['GREE', '2240', '001', 'The New Testament II', 'Andrej Petrovic', 'Lecture', '3', 'true', 'false', 'true', 'false', 'true', '1200', '1250', 'Cocke Hall 101', '8', '20'], ['GREE', '3020', '001', 'Advanced Reading in Greek', 'Ivana Petrovic', 'Lecture', '3', 'false', 'true', 'false', 'true', 'false', '1100', '1215', 'Office', '3', '9'], ['GREE', '5559', '001', 'New Course in Greek', 'Andrej Petrovic', 'Lecture', '3', 'true', 'false', 'true', 'false', 'false', '1530', '1645', 'New Cabell Hall 066', '6', '15'], ['GREE', '5559', '002', 'New Course in Greek', 'Ivana Petrovic', 'Lecture', '3', 'false', 'true', 'false', 'true', 'false', '1530', '1645', 'New Cabell Hall 042', '8', '15']], None, ['GREE', False, None, 1100])
    correct += test_func(mod, func, [['GREE', '1020', '100', 'Elementary Greek', 'John Dillery', 'Lecture', '4', 'true', 'false', 'true', 'false', 'true', '1000', '1050', 'New Cabell Hall 066', '11', '15'], ['GREE', '1020', '101', 'Elementary Greek', 'Rebecca Frank', 'Discussion', '0', 'false', 'true', 'false', 'true', 'false', '930', '1045', 'New Cabell Hall 066', '6', '15'], ['GREE', '2020', '001', 'Intermediate Greek II', 'Jon Mikalson', 'Lecture', '3', 'true', 'false', 'true', 'false', 'true', '1000', '1050', 'Cocke Hall 115', '14', '20'], ['GREE', '3020', '001', 'Advanced Reading in Greek', 'Ivana Petrovic', 'Lecture', '3', 'false', 'true', 'false', 'true', 'false', '1100', '1215', 'Office', '3', '9']], None, ['GREE', False, None, None, 1100])
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
student(func+' passed', correct, 'out of', 7, 'automated test cases')

correct += oc

grader('Score:', correct, '/', 6+7)

