import urllib,csv
from bs4 import BeautifulSoup

#Open url into beautifulsoup object
target = BeautifulSoup(urllib.request.urlopen("http://www.boxofficemojo.com/yearly/").read())
file = csv.writer(open('movies.csv','w'),delimiter=',',quotechar='"')
#Find hard coded table location
table = target.find_all('table',id=False)[2].find_all("tr")

#Read each table line except first
for line in table[1:]:
    row = line.find_all("td")
    movie = []
    #Append each field
    for col in row:
        movie.append(col.contents[0].text)
    #Check row valid
    if len(movie) == 10:
        file.writerow(movie)

#referred to https://docs.python.org/3/library/csv.html
#https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        
