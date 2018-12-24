from gradetools import expect, student, grader

failed_test = ""
failed_test_student = ""
found_emails = []
correct = 0
wrong = 0
bonus_correct = 0

URL = "https://cs1110.cs.virginia.edu/e-m-a-i-l-s.html"
correct_emails = ['one@two.com','three-four@five.edu','six-seven@cs.virginia.edu','Mrs.N0way@l4rd-frAMers.info','d@e.tv','with-at-sign@vt.edu','other-email@virginia.com','last.first.name@seas.virginia.edu','my-little@PoNy.ORG','king@queen.gov','prince@princess.uk','a.b@c.d.e.com']
bad_function = False

def check_email(test_email, grade_email):
    if grade_email in found_emails:
        found_emails.remove(grade_email)
        correct_emails.remove(grade_email)
        student("Test:",test_email,"PASSED")
        return "PASSED"
    else:
        student("Test:",test_email,"FAILED!")
        grader("Test:",test_email,"FAILED!")
        return "FAILED"

def check_bonus_email(test_email, grade_email):
    if grade_email in found_emails:
        found_emails.remove(grade_email)
        student("Bonus:",test_email,"PASSED (+1 bonus!)")
        return "PASSED"
    else:
        student("Bonus:",test_email,"fail (does not count against you)")
        return "FAILED"

try:
    import email_finder
except:
    student("You are missing at least one function or a function's header is incorrect.  Tests will not run until you fix this problem.")
    grader("Exception thrown - missing function")
    bad_function = True
    exit()

program_search = open("email_finder.py", "r")
for line in program_search:
    if "print(" in line:
        student("You are calling print from inside your code.  Please remove all testing statements before submitting.")
        bad_function = False
        exit()

if not bad_function:
    try:

        found_emails = email_finder.find_emails_in_website(URL)

        # test basic@virginia.edu
        test_email = 'basic@virginia.edu'
        grade_email = 'one@two.com'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test link-only@virginia.edu
        test_email = 'link-only@virginia.edu'
        grade_email = 'three-four@five.edu'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test multi-domain@cs.virginia.edu
        test_email = 'multi-domain@cs.virginia.edu'
        grade_email = 'six-seven@cs.virginia.edu'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test Mr.N0body@cand3lwick-burnERS.rentals
        test_email = 'Mr.N0body@cand3lwick-burnERS.rentals'
        grade_email = 'Mrs.N0way@l4rd-frAMers.info'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test a@b.ca
        test_email = 'a@b.ca'
        grade_email = 'd@e.tv'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test no-at-sign@virginia.edu
        test_email = 'no-at-sign@virginia.edu'
        grade_email = 'with-at-sign@vt.edu'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test no-at-or-dot@virginia.edu
        test_email = 'no-at-or-dot@virginia.edu'
        grade_email = 'other-email@virginia.com'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test first.last.name@cs.virginia.edu
        test_email = 'first.last.name@cs.virginia.edu'
        grade_email = 'last.first.name@seas.virginia.edu'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test with-parenthesis@Virginia.EDU
        test_email = 'with-parenthesis@Virginia.EDU'
        grade_email = 'my-little@PoNy.ORG'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test added-words1@virginia.edu
        test_email = 'added-words1@virginia.edu'
        grade_email = 'king@queen.gov'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test added-words2@virginia.edu
        test_email = 'added-words2@virginia.edu'
        grade_email = 'prince@princess.uk'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # test may.end@with-a-period.com
        test_email = 'may.end@with-a-period.com'
        grade_email = 'a.b@c.d.e.com'
        if check_email(test_email, grade_email) == "PASSED":
            correct += 1
        else:
            wrong += 1

        # bonus test NO mst3k@virginia.Edu
        test_email = 'mst3k@virginia.edu'
        if grade_email not in found_emails:
            print("Bonus:",test_email,"PASSED (+1 bonus)!")
            bonus_correct += 1
        else:
            print("Bonus:",test_email,"fail (does not count against you)")

        # bonus test underscore@virginia.edu
        test_email = 'underscore@virginia.edu'
        grade_email = 'alligator@gmail.com'
        if check_bonus_email(test_email, grade_email) == "PASSED":
            bonus_correct += 1

        # bonus test backwards@virginia.edu
        test_email = 'reverse@virginia.edu'
        grade_email = 'backwards@virginia.com'
        if check_bonus_email(test_email, grade_email) == "PASSED":
            bonus_correct += 1

        # bonus test JohnD@virginia.edu
        test_email = 'JohnD@virginia.edu'
        grade_email = 'GregoryR@vt.com'
        if check_bonus_email(test_email, grade_email) == "PASSED":
            bonus_correct += 1

        # bonus test markdown@virginia.edu
        test_email = 'markdown@virginia.edu'
        grade_email = 'moo@cow.com'
        if check_bonus_email(test_email, grade_email) == "PASSED":
            bonus_correct += 1

        if len(found_emails) > 3:
            student(len(found_emails), "extra emails found and will count against you (4 or more extra emails count against you).")
            wrong += len(found_emails) // 2
        elif len(found_emails) > 0:
            student(len(found_emails), "extra emails found (3 or less do not count against you).")

        grader("Extra Emails Found:", found_emails)
        student("Correct:",correct,"/ Incorrect:",wrong, "/ Bonus:", bonus_correct)
        grader("Correct:",correct,"/ Incorrect:",wrong, "/ Bonus:", bonus_correct)


        final_score = correct*10/12 + bonus_correct - wrong/2
        if final_score >= 9:
            final_score = 10
        elif final_score >= 7:
            final_score = 9
        elif final_score >= 5:
            final_score = 7
        elif final_score >= 3:
            final_score = 5
        else:
            final_score = 3
        grader("Score to give:", final_score)
        student("Final Score:", final_score)

        if wrong == 0:
            student("Congratulations, you passed all of our tests!")


    except IndexError as inst:
        student("Your program has crashed due to trying to access a location in a list or string that does not exist. Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)
    except NameError as inst:
        student("Your program has crashed due to trying to use a variable that is not available in scope. Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)
    except TypeError as inst:
        student("Your program has crashed due to trying to use a variable that is not allowed with its particular type (i.e. add a string to an int). Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)
    except KeyError as inst:
        student("Your program has crashed due to trying to access something from a dictionary or list that does not exist. Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)
    except ValueError as inst:
        student("Your program has crashed due to trying to access something from a dictionary or list that does not exist. Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)
    except AttributeError as inst:
        student("Your program has crashed due to trying to access something from an object that does not exist.  For example, your .group() method may not exist if nothing is returned (it will be type None). Error Message: " + str(inst))
        grader(inst)
        student("Test Crashed!:", test_email)
        grader("Crashed Test:", grade_email)