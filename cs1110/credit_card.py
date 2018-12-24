def check(num):
    digitSum = 0
    for i in str(num)[-1::-2]:
        digitSum += int(i)
    
    for i in  str(num)[-2::-2]:
        for j in str(2*int(i)):
            digitSum += int(j)
    
    return (digitSum % 10 == 0)
    
