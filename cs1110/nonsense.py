def check(integer):
    number = str(integer)
    length = len(number)
    if length % 2 == 0:
        first = 0
        i = 1
        while i < length:
            first = first + int(number[i])
            i += 2

        second = []
        j = 0
        while j < length:
            second.append(number[j])
            j += 2
        sum = 0
        for k in range(0, len(second)):
            result = 2 * int(second[k])
            if result < 10:
                sum += result
            elif result >= 10:
                new = str(result)
                other = int(new[0]) + int(new[1])
                sum += other
        final = first + sum
        if final % 10 == 0:
            return True
        else:
            return False

    if length % 2 != 0:
        #print("hi")
        first = int(number[length - 1])
        i = 1
        while i < length:
            print(number[i],end="")
            first = first + int(number[i])
            i += 2
        second = []
        j = 0
        while j < length-1:
            second.append(number[j])
            j += 2
        sum = 0
        for k in range(0, len(second)):
            result = 2 * int(second[k])
            if result < 10:
                sum += result
            elif result >= 10:
                new = str(result)
                other = int(new[0]) + int(new[1])
                sum += other
        final = first + sum
        if final % 10 == 0:
            return True
        else:
            return False

print(check('378282246310005'))