import urllib.request

def find_average_temp(day_1, day_2):
    datafile = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/cho-temp.csv')

    temp_1 = 0
    temp_2 = 0
    
    for line in datafile:
        line = line.decode('utf-8').strip()
        date = line.split(",")

        if date[0] == day_1[0] and date[1] == day_1[1] and date[2] == day_1[2]:
            temp_1 = int(date[5])

        if date[0] == day_2[0] and date[1] == day_2[1] and date[2] == day_2[2]:
            temp_2 = int(date[5])

    datafile.close()
    average_temp = (temp_1 + temp_2) / 2
    return average_temp


def find_max_temp(year, month):
    datafile = urllib.request.urlopen('http://cs1110.cs.virginia.edu/files/cho-temp.csv')
    max_temp = 999
    for line in datafile:
        line = line.decode('utf-8').strip()
        date = line.split(",")
        if date[0] == year and date[1] == month and int(date[3]) > max_temp:
            max_temp = int(date[3])

    datafile.close()

    return max_temp


print("What would you like to do?")
print("1 - find the average temperature between two days")
print("2 - find the max temp in a month")
choice = int(input("?: "))

if choice == 1:
    input_1 = input("Enter the year, month, and day for the first day (int,str,int -- no spaces): ")
    day_1 = input_1.split(",")
    input_2 = input("Enter the year, month, and day for the second day (int,str,int -- no spaces): ")
    day_2 = input_2.split(",")
    print(find_average_temp(day_1, day_2))
elif choice == 2:
    input_1 = input("Enter the year and month (int,str -- no spaces): ")
    year_and_month = input_1.split(",")
    print(find_max_temp(year_and_month[0], year_and_month[1]))
