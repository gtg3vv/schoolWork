from gradetools import *

task = "nonsense"

correct = 0
if expect(task, ['elbow'], [re.compile(' $'), re.compile(' '.join(['elbow']*12)+'.*\n"elbow"')], "wrong output", maxtime=1): correct += 1
if expect(task, ['caper'], [re.compile(' $'), re.compile(' '.join(['caper']*12)+'.*\n"caper"')], "wrong output", maxtime=1): correct += 1

grader("Passed",correct,"out of",2,"automated test cases.'")
if correct == 2:
    student("Your program passed our automated tests.")
student("A human will check for reasonable output text and assign your grade.")
