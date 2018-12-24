from gradetools import expect, student, grader
import re

correct = 0
wrong = 0


import timeout
import runpy, sys

name = None
newio = timeout.CustomIO()
oio = sys.stdout, sys.stdin
try:
    sys.stdout, sys.stdin = newio, newio
    try: runpy.run_module('rumple')
    except: pass
    ans = newio.printed[0]
    name = ' '.join(ans.strip().split('\n')[0].split()[7:-3])
finally:
    sys.stdout, sys.stdin = oio

if name is None:
    student('We failed to find the answer on the first line of output')
    grader('Score: 0 / 10')
    quit()

if expect("rumple", [name], [re.compile(r".* $"), re.compile(r".*")], "Failed first example."): correct += 1
else: wrong += 1

if expect("rumple", ['x'+name, name], [re.compile(r".* $"), re.compile(r".* $"), re.compile(r".*")], ""): correct += 1
else: wrong += 1

if expect("rumple", ['x'+str(_) for _ in range(100)]+[name], [None]*102, ""): correct += 1
else: wrong += 1



if wrong == 0:
    student("Congratulations, you passed all of our tests!")
else:
    student("You passed",correct,"out of",correct+wrong,"tests.")

grader("Score:",correct,"/",correct+wrong)

