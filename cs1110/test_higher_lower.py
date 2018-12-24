from gradetools import expect, student, grader
import re

correct = 0
wrong = 0


if expect("higher_lower", ['19','9','9','40','19'], [
    re.compile(r".* $"), re.compile(r".* $"), re.compile(r".* $"),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*low.*',re.I),
    re.compile(r'.*win.*',re.I),
], "Wrong format output."): correct += 1
else: wrong += 1



if expect("higher_lower", ['19','9','9','40','19'], [
    None, None, None,
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*low.*',re.I),
    re.compile(r'.*win.*',re.I),
], "Failed to let player win eventually."): correct += 1
else: wrong += 1


if expect("higher_lower", ['19','8','1','1','1','1','1','1','1','1'], [
    None, None, None,
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*high.*',re.I),
    re.compile(r'.*lose.*\b19\b.*',re.I),
], "Failed to let player lose eventually."): correct += 1
else: wrong += 1


if expect("higher_lower", ['8','1','5'], [
    None, None, None,
    re.compile(r'.*lose.*\b8\b.*',re.I),
], "Failed to let player lose immediately."): correct += 1
else: wrong += 1

if expect("higher_lower", ['8','1','8'], [
    None, None, None,
    re.compile(r'.*win.*',re.I),
], "Failed to let player win immediately."): correct += 1
else: wrong += 1


if wrong == 0:
    student("Congratulations, you passed all of our tests!")
else:
    student("You passed",correct,"out of",correct+wrong,"tests.")

grader("Score:",correct,"/",correct+wrong)

