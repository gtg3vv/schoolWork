import random
file = open("writetothisfile.txt","w")
classes =[]
for i in range(500):
    classes.append(str(random.randint(0,100000)))
classes=list(set(classes))

file.write("2000 " + str(len(classes)) + " 2\n")

for i in range(1000):
    i = str(i)
    file.write(i + " " + random.choice(classes) + "\n")
    file.write(i + " " + random.choice(classes) + "\n")
for i in range(len(classes)):
    file.write(str(i) + " 2\n")
file.write("0 0 0")