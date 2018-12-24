from gradetools import expect, student, grader
import re

correct = 0
wrong = 0

def roman(num):
    if (num <= 0 or num >= 4000) :
    # bounds checking (0,4000)
        return("Input must be between 1 and 3999")
    else:
        thousands = ["", "M", "MM", "MMM"]
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
        return(thousands[int(num/1000)] + hundreds[int(num%1000/100)] + tens[int(num%100/10)] + ones[int(num%10)])

if expect("roman", ['1'],[re.compile(r".*"),re.compile(r".*I.*")], "Failed when we tested value: 1", maxtime=1):
    i = 1
    for i in range(1, 4000, 9):
        result = roman(i)
        if expect("roman", [str(i)],[re.compile(r".*"),re.compile(r".*%s.*"%result)], "Failed when we tested value: " + str(i), maxtime=0.1):
            correct += 1
        else:
            wrong += 1

    if expect("roman", ["1997"],[re.compile(r".*"),re.compile(r".*(MCMXCVII).*")], "Failed basic test from example."):
        correct += 1
    else:
        wrong += 1

    if expect("roman", ["0"],[re.compile(r".*"),re.compile(r".*(Input must be between 1 and 3999).*")], "Failed out of bounds test where number is less than 1."):
        correct += 1
    else:
        wrong += 1

    if expect("roman", ["4000"],[re.compile(r".*"),re.compile(r".*(Input must be between 1 and 3999).*")], "Failed out of bounds test test where number higher than 3999 #1."):
        correct += 1
    else:
        wrong += 1

    if expect("roman", ["4001"],[re.compile(r".*"),re.compile(r".*(Input must be between 1 and 3999).*")], "Failed out of bounds test where number higher than 3999 #2."):
        correct += 1
    else:
        wrong += 1

    # if expect("roman", ["3999"],[re.compile(r".*"),re.compile(r".*(MMMCMXCIX).*")], "Failed large number"):
    #     correct += 1
    # else:
    #     wrong += 1
    #
    # if expect("roman", ["2015"],[re.compile(r".*"),re.compile(r".*(MMXV).*")], "Failed current year"):
    #     correct += 1
    # else:
    #     wrong += 1
    #
    # if expect("roman", ["27"],[re.compile(r".*"),re.compile(r".*(XXVII).*")], "Failed small number"):
    #     correct += 1
    # else:
    #     wrong += 1
    #
    # if expect("roman", ["1"],[re.compile(r".*"),re.compile(r".*(I).*")], "Failed very small number"):
    #     correct += 1
    # else:
    #     wrong += 1
    #
    # if expect("roman", ["184"],[re.compile(r".*"),re.compile(r".*(CLXXXIV).*")], "Failed  small number 2"):
    #     correct += 1
    # else:
    #     wrong += 1
else:
    wrong += 1
    student('Because you failed when the input was 1, we did not test anything else')

if wrong == 0:
    student("Congratulations, you passed all of our tests!")
else:
    student("You passed",correct,"out of",correct+wrong,"tests.  If you failed all tests, but your values look correct, make sure to double check your spelling, punctuation, capitalization, and spacing!  It must match the assignment page exactly!")

grader("Score:",correct,"/",correct+wrong)
