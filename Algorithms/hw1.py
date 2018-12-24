# Gabriel Groover (gtg3vv)
#The change algorithm selects the largest coin that is smaller than the remaining change and then decreases
#the remaining change by that amount to produce a minimum number of coins.
import sys
import locale
file = open(sys.argv[1], "r")
locale.setlocale( locale.LC_ALL, '' )

for line in file:
    if line == "-1.00":
        sys.exit()
    change = float(line)

    if change >= 0:
        print(locale.currency(change,grouping=True),end=" ")
        change = change * 100 % 100
        while change > 0:
            if change >= 25:
                print("Q",end=" ")
                #print(change, end=" ")
                change -= 25
            elif change >= 10:
                print("D",end=" ")
                #print(change,end=" ")
                change -= 10
            elif change >= 5:
                print("N",end=" ")
                #print(change,end=" ")
                change -= 5
            elif change >= 1:
                print("P",end=" ")
                #print(change,)
                change -= 1
        print("")
