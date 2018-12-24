import urllib.request

page = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/louslist/CS')
#all = page.readline()
#for line in page:
    #print(line.decode('utf-8').strip())

def instructors(department):
    teachers = list()
    page = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/louslist/'+department)
    for line in page:
        line = line.decode('utf-8').strip().split('|')
        x = line[4].replace('+1', '').replace('+2','')
        if x not in teachers:
            teachers.append(x)
        teachers.sort()
    print(teachers)

def class_search(dept_name, has_seats_available=True, level=None, not_before=None, not_after=None):
    page = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/louslist/' + dept_name)
    final = list()
    seats = list()
    levellist = list()
    timelist = list()
    time2list = list()
    for line in page:
        line = line.decode('utf-8').strip().split('|')
        if has_seats_available == True:
            total = int(line[16])
            total2 = int(line[15])
            if total - total2 != 0:
                seats.append(line)
        else:
            seats.append(line)
        if not level:
            level = str(level)
            courselevel = line[1]
            courselevel2 = courselevel[0]
            if level[0] == courselevel2:
                levellist.append(line)
        else:
            levellist.append(line)
        if not not_before:
            not_before = str(not_before)
            time = line[12]
            if not_before >= time:
                timelist.append(not_before)
        else:
            timelist.append(not_before)
        if not not_after:
            not_after = str(not_after)
            time2 = line[13]
            if not_after <= time2:
                time2list.append(not_after)
        else:
            time2list.append(not_after)
        if line in final and seats and levellist and timelist and time2list:
            final.append(line)
    print(final)


class_search('GREE', False, None, None, 1100)
class_search('MUBD')
class_search('MUBD', False)
class_search('GREE', False, 2000)