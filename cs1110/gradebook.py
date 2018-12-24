book = {}

def assignment(kind, grade, weight=1):
    if kind not in book:
        book[kind] = [grade, weight]
    else:
        book[kind][0] = (book[kind][0]*book[kind][1] + grade*weight) / (weight + book[kind][1])
        book[kind][1] = book[kind][1] + weight
    
    
def total(proportions):
    grade = 0
    for kind in proportions:
        if kind in book:
            grade += book[kind][0] * proportions[kind]
    return grade
            
syllabus = {
    'exam': 0.5,
    'hw': 0.4,
    'lab': 0.1,
}

print(total(syllabus))
assignment('exam', 83)
assignment('exam', 88)
assignment('exam', 91, 2)
print(total(syllabus))
assignment('hw', 100)
assignment('hw', 100)
assignment('hw', 70)
assignment('hw', 0)
assignment('hw', 100, 4)
assignment('hw', 50)
assignment('lab', 90)
print(total(syllabus))
assignment('extra', 300)
print(total(syllabus))