from gradetools import expect, student, grader
import re

correct = 0
wrong = 0

if expect("higher_lower_player", ['5','lower','higher','lower','higher', 'lower', '33'], [
    re.compile(r".* $"),
    re.compile(r".*\b50\b.* $"),
    re.compile(r".*\b25\b.* $"),
    re.compile(r".*\b37\b.* $"),
    re.compile(r".*\b31\b.* $"),
    re.compile(r".*\b34\b.* $"),
    re.compile(r'.*los[et].*',re.I),
    None,
], "Wrong format output."): correct += 1
else: wrong += 1


if expect("higher_lower_player", ['5','lower','higher','lower','higher', 'lower', '33'], [
    re.compile(r".*"),
    re.compile(r".*\b50\b.*"),
    re.compile(r".*\b25\b.*"),
    re.compile(r".*\b37\b.*"),
    re.compile(r".*\b31\b.*"),
    re.compile(r".*\b34\b.*"),
    re.compile(r'.*los[et].*',re.I),
    None,
], "Failed first example run."): correct += 1
else: wrong += 1

if expect("higher_lower_player", ['8','lower','higher','lower','higher', 'lower', 'higher', 'lower'], [
    re.compile(r".*"),
    re.compile(r".*\b50\b.*"),
    re.compile(r".*\b25\b.*"),
    re.compile(r".*\b37\b.*"),
    re.compile(r".*\b31\b.*"),
    re.compile(r".*\b34\b.*"),
    re.compile(r".*\b32\b.*"),
    re.compile(r".*\b33\b.*"),
    re.compile(r'.*\b32\b.*\b33\b.*',re.I)
], "Failed second example run."): correct += 1
else: wrong += 1

if expect("higher_lower_player", ['1','higher','20'], [
    re.compile(r".*"),
    re.compile(r".*\b50\b.*"),
    re.compile(r'.*los[et].*',re.I),
    re.compile(r'.*\b50\b.*',re.I)
], "Failed third example run."): correct += 1
else: wrong += 1

if expect("higher_lower_player", ['3','higher','same'], [
    re.compile(r".*"),
    re.compile(r".*\b50\b.*"),
    re.compile(r'.*\b75\b.*'),
    re.compile(r'.*\bw[io]n\b.*',re.I)
], "Failed fourth example run."): correct += 1
else: wrong += 1


if expect("higher_lower_player", ['2','higher','lower','99'], [
    re.compile(r".*"),
    re.compile(r".*\b50\b.*"),
    re.compile(r'.*\b75\b.*'),
    re.compile(r'.*los[et].*',re.I),
    re.compile(r'.*\b75\b.*',re.I)
], "Failed a case not on the writeup."): correct += 1
else: wrong += 1

if wrong == 0:
    student("Congratulations, you passed all of our tests!")
else:
    student("You passed",correct,"out of",correct+wrong,"tests.")

grader("Score:",correct,"/",correct+wrong)

