import regexs, re
from gradetools import student, grader

ret = type(re.compile(''))

def full_match(regex, text):
    '''Gives a list of all complete matches'''
    ans = []
    for match in regex.finditer(text):
        ans.append(match.group(0))
    return ans

text = '''
CS1110-001/smile ! hi there
mst3k +3o-___26 t.j t.j.
"hi there" but not " hi there" or "hi there " or "I said "hi" just now"
3,4, 3.0, 4.5 and -3.14159265 1110 but not 3.4.5, 1 or 1   2 or 3 - 4
Thomas Jefferson and Edmund Jennings Randolph and J. Pierpont Finch and T. Jefferson
but not T Jefferson or Thomas J. or Flannery O'Connor
'''

score = 0

if 'nospace' in dir(regexs) and type(regexs.nospace) is ret:
    ns = full_match(regexs.nospace, text)
    nss = sum(['CS1110-001/smile' in ns, '!' in ns, 'hi there' not in ns, '' not in ns])
    student('nospace: passed', nss, 'out of', 4, 'tests')
    score += nss
else:
    student('nospace was not a compiled regular expression in regexs.py')
    

#if 'email_name' in dir(regexs) and type(regexs.email_name) is ret:
#    en = full_match(regexs.email_name, text)
#    ens = sum(['mst3k' in en, '+3o-___26' in en, 't.j' in en, 't.j.' not in en])
#    student('email_name: passed', nss, 'out of', 4, 'tests')
#    score += nss
#else:
#    student('email_name was not a compiled regular expression in regexs.py')

if 'quotation' in dir(regexs) and type(regexs.quotation) is ret:
    q = full_match(regexs.quotation, text)
    qs = sum(['"hi there"' in q, '" hi there"' not in q, '"hi there "' not in q, '"I said "hi" just now"' not in q])
    student('quotation: passed', qs, 'out of', 4, 'tests')
    score += qs
else:
    student('quotation was not a compiled regular expression in regexs.py')


if 'twonum' in dir(regexs) and type(regexs.twonum) is ret:
    tn = full_match(regexs.twonum, text)
    tns = sum([
    '3,4' in tn,
    '3.0, 4.5' in tn,
    '-3.14159265 1110' in tn,
    '3.4.5, 1' not in tn,
    '1   2' not in tn,
    '3 - 4' not in tn])

    for match in regexs.twonum.finditer(text):
        if match.group(0) == '3,4':
            tns += sum(['3' in match.groups(), '4' in match.groups()])
        if match.group(0) == '-3.14159265 1110':
            tns += sum(['-3.14159265' in match.groups(), '1110' in match.groups()])

    student('twonum: passed', tns, 'out of', 10, 'tests')
    score += nss
else:
    student('twonum was not a compiled regular expression in regexs.py')


if 'likely_name' in dir(regexs) and type(regexs.likely_name) is ret:
    ln = full_match(regexs.likely_name, text)
    lns = sum(['Thomas Jefferson' in ln,
    'Edmund Jennings Randolph' in ln,
    'J. Pierpont Finch' in ln,
    'T. Jefferson' in ln,
    'T Jefferson' not in ln,
    'Thomas J.' not in ln,
    "Flannery O'Connor" not in ln])
    student('likely_name: passed', lns, 'out of', 7, 'tests')
    score += nss
else:
    student('likely_name was not a compiled regular expression in regexs.py')
