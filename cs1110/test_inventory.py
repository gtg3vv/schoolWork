#import cacheurls
from gradetools import grader, student, test_func
import os, os.path, re


correct = 0
mod = 'inventory'
func = 'restock'
try:
    if os.path.exists('s1.csv'): os.remove('s1.csv')
    
    correct += test_func(mod, func, 11, [re.compile(r'.*widget.* $'), ''], ['s1.csv', 'widget', 11], inputs=['23.50'], full=True)

    if os.path.exists('s1.csv'):
        correct += 1
        s = open('s1.csv').read()
        if 'widget,11,23.5' in s: correct += 1
        else: grader('after restock, wrong file content on disk for new item in new file')
    else:
        grader('after calling', func, 'no file named filename exists')

    
    with open('s2.csv', 'w') as s2:
        print('thunk,1,15.5', file=s2)
        print('wig,1000,0.23', file=s2)
    
    correct += test_func(mod, func, 2, None, ['s2.csv', 'thunk', 1])
    correct += test_func(mod, func, 1098, None, ['s2.csv', 'wig', 98])
    correct += test_func(mod, func, 98, [None, None, ''], ['s2.csv', 'thaum', 98], inputs=['1.2.3', '0.03'])
    
    if os.path.exists('s2.csv'):
        correct += 1
        s = open('s2.csv').read()
        if 'thunk,2,15.5' in s and 'wig,1098,0.23' in s: correct += 1
        else: grader('after restock, wrong file content on disk for pre-exisiting item')
        if 'thaum,98,0.03' in s: correct += 1
        else: grader('after restock, wrong file content on disk for new item in old file')
    else:
        grader('after calling', func, 'no file named filename exists')
    
except BaseException as ex:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
    grader('test suite raised', ex)
student(func+' passed', correct, 'out of', 12, 'automated test cases')

oc = correct
correct = 0
func = 'sell'
try:
    if os.path.exists('s1.csv'): os.remove('s1.csv')
    with open('s2.csv', 'w') as s2:
        print('thunk,1,15.5', file=s2)
        print('wig,1000,0.23', file=s2)
        print('thaum,98,0.03', file=s2)
    
    correct += test_func(mod, func, 87, None, ['s2.csv', 'thaum', 11], full=True)
    correct += test_func(mod, func, 0, None, ['s2.csv', 'wig', 1000])
    correct += test_func(mod, func, None, None, ['s2.csv', 'thunk', 2])
    correct += test_func(mod, func, None, None, ['s1.csv', 'wig', 1])
    
    if os.path.exists('s2.csv'):
        correct += 1
        s = open('s2.csv').read()
        if 'thunk,1,15.5' in s and 'thaum,87,0.03' in s: correct += 1
        else: grader('after sell, wrong file content on disk for items in stock')
        if 'wig' not in s: correct += 1
        else: grader('after sell, still has entry for item sold away entirely')
    else:
        grader('after calling', func, 'no file named filename exists')

    
except:
    student("something unexpected happened in our autograding; your score below might be incorrectly small")
    grader('test suite raised', ex)
student(func+' passed', correct, 'out of', 7, 'automated test cases')




grader('Score:', correct+oc, '/', 19)

