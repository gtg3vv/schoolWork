# Tom Peters trp4fb
# Salary PA21

import urllib.request
import re

def name_to_url(name):
    if "," in name:
        index = name.find(" ")
        name = name[index+1:] + "-" + name[:index-1]

    elif " " in name:
        name = name.replace(" ", "-")
    name = name.lower()
    return name

def report(person):
    name = name_to_url(person)
    try:
        stream = urllib.request.urlopen("http://cs1110.cs.virginia.edu/files/uva2016/" + name)
        full = stream.read().decode("UTF-8")

        title = re.compile(r'Job\stitle:\s(.*)<')   #(.*)
        mo = title.search(full)
        title = mo.group(1)
        if "&amp" in title or "&lt" in title or "&gt" in title:
            title = title.replace("&amp;", "&")
            title = title.replace("&lt;", "<")
            title = title.replace("&gt;", ">")
        title = title

        tot_comp = re.compile(r'>\$([0-9,]*)')
        sal = tot_comp.search(full)
        salary = sal.group(1)
        if "," in salary:
            salary = salary.replace(",", "")
        salary = float(salary)

        try:
            r = re.compile(r'<td>([0-9,0-90-90-9]*) ')
            ra = r.search(full)
            rank = ra.group(1)
            if "," in rank:
                rank = rank.replace(",", "")
            rank = int(rank)
        except:
            rank = 0

        return title, salary, rank

    except:
        title = None
        salary = 0
        rank = 0
    return title, salary, rank