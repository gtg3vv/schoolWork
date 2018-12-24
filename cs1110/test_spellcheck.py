from gradetools import expect, student, grader
import re
import cacheurls

correct = 0
wrong = 0

if expect("spellcheck", [""],[None, ''], "Failed when no words entered.", maxtime=5):
    correct += 1
else:
    wrong += 1

if expect("spellcheck", ["Never mind what I say, I mean no harm.", "Why! When? \"oh...\"", ''],[None, '', '', ''], "Failed multi-line punctuation test.", maxtime=5):
    correct += 1
else:
    wrong += 1

if expect("spellcheck", ["Ne'er 'ave I bein' so hurt.", ''],[None, re.compile('^\s*MISSPELLED:  *ave\s*MISSPELLED:  *bein\s*$'), ''], "Failed apostrophe test.", maxtime=5):
    correct += 1
else:
    wrong += 1


if expect("spellcheck", ["yes", 'yess', 'yes']*4+[''],[None]+['',re.compile('^\s*MISSPELLED:  *yess\s*$'), '']*4+[''], "Failed many-line test test.", maxtime=5):
    correct += 1
else:
    wrong += 1


if wrong == 0:
    student("Congratulations, you passed all of our tests!")
else:
    student("You passed",correct,"out of",correct+wrong,"tests.")

grader("Score:",correct,"/",correct+wrong)
