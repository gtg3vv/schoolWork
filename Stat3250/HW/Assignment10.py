## File: Assignment10.py (STAT 3250)
## Topic: Assignment 10
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import  zipfile
import  pandas as pd

#Create zipfile from the stocks zip
zipfile = zipfile.ZipFile('Stocks.zip')

dfList = []

#Iterate through each of the items in the zipfile
#File contains all information about a single file
for file in zipfile.infolist():
	#If the file is a  csv, open it and read as csv into dataframe
	if file.filename[-4:] == '.csv':
		df = pd.read_csv(zipfile.open(file))
		#add column for ticker symbol and add dataframe to list
		df['Stock'] = file.filename[7:-4]
		dfList.append(df)

#Combine all frames in list
stocks = pd.concat(dfList)

# 1. Find the mean for the Open, High, Low, and Close entries for all of the records taken as a single group.

#Get  stock columns with correct values and take means for those columns
print(stocks[['Open','Close','High','Low']].mean())

'''
1.
Open     50.863852
Close    50.876482
High     51.459412
Low      50.253368
dtype: float64
'''

# 2. Find the top-5 and bottom-5 stocks in terms of their average Close price. Give tables showing the
# stock ticker symbol and the average Close price. (Print out of a Series or DataFrame is fine.)

#Get relevant columns and group by ticker symbol and take the mean
#Sort values descending based on the means
avgClose = stocks[['Stock','Close']].groupby('Stock').mean().sort_values('Close', ascending=False)

#Print first and last 5 values
print('Top 5 closing avgs:\n', avgClose[:5])
print('Bottom 5 closing avgs:\n', avgClose[-5:])

'''
2.
Top 5 closing avgs:
             Close
Stock            
CME    253.956017
AZO    235.951950
AMZN   185.140534
BLK    164.069088
GS     139.146781
Bottom 5 closing avgs:
            Close
Stock           
HBAN   13.697483
ETFC   12.808103
XRX    11.291864
F      11.174158
FTR     8.969515
'''

# 3. Find the top-5 and bottom-5 stocks in terms of the day-to-day volatility of the price. This is the mean
# of the differences High - Low daily for each stock. Give tables for each, as in the previous problem.

#Add new volatility column based on difference
stocks['Volatility'] = stocks['High'] - stocks['Low']
#Take just ticker and volatility, group by ticker and sort by mean volatility
avgVol = stocks[['Stock','Volatility']].groupby('Stock').mean().sort_values('Volatility', ascending=False)

#Print first and last 5 values
print('Top 5 volatility:\n', avgVol[:5])
print('Bottom 5 volatility:\n', avgVol[-5:])

'''
3.
Top 5 volatility:
        Volatility
Stock            
CME      7.697287
AMZN     4.691407
BLK      4.470693
AZO      4.330294
ICE      4.056189
Bottom 5 volatility:
        Volatility
Stock            
NI       0.363250
HBAN     0.343893
F        0.323567
XRX      0.308743
FTR      0.205275
'''

# 4. Repeat the previous problem, this time using the relative volatility, which is given by
# High − Low
# 0.5(Open + Close)
# for each day. As above, provide tables.

#Add relative volatility column as formula of other columns
stocks['RelVolatility'] = (stocks['High'] - stocks['Low']) / (.5 * (stocks['Open'] + stocks['Close']))
#Take just ticker  and relative volatility, group by ticker and sort by mean relative volatility
avgRelVol = stocks[['Stock','RelVolatility']].groupby('Stock').mean().sort_values('RelVolatility', ascending=False)

#Print first and last 5 values
print('Top 5 rel volatility:\n', avgRelVol[:5])
print('Bottom 5 rel volatility:\n', avgRelVol[-5:])

'''
4.
Top 5 rel volatility:
        RelVolatility
Stock               
AAL         0.055533
LVLT        0.054870
EQIX        0.051295
REGN        0.048172
ETFC        0.045381
Bottom 5 rel volatility:
        RelVolatility
Stock               
WEC         0.015761
CL          0.015521
K           0.014992
PG          0.014192
GIS         0.013966
'''

# 5. For each day the market was open in February 2010, find the average daily price for all stocks for each
# of Open, High, Low, Close, and Volume

#Change date column to be datetime objects
stocks['Date'] = pd.to_datetime(stocks['Date'])
#Get only rows that are in the  month feb and the year 2010
febStocks = stocks[(stocks['Date'].dt.month == 2) & (stocks['Date'].dt.year == 2010)]
#Group by day of month and take mean of each relevant column for that day
print(febStocks.groupby(febStocks['Date'])[['Open', 'Close', 'Low','Volume']].mean())

'''
5.
                 Open      Close        Low        Volume
Date                                                     
2010-02-01  42.267199  42.704181  41.912471  7.200101e+06
2010-02-02  42.573926  43.083780  42.178253  7.996646e+06
2010-02-03  43.074528  42.996122  42.596412  7.173997e+06
2010-02-04  42.869744  41.799597  41.666130  9.732287e+06
2010-02-05  41.487291  41.628338  40.569602  1.075256e+07
2010-02-08  41.954153  41.565881  41.349668  7.132838e+06
2010-02-09  41.371208  41.500219  40.934578  7.972704e+06
2010-02-10  41.783087  41.722352  41.212389  6.744782e+06
2010-02-11  41.814452  42.391167  41.417809  7.037806e+06
2010-02-12  41.403247  41.823831  41.018028  7.246792e+06
2010-02-16  42.663708  43.075126  42.331781  6.649753e+06
2010-02-17  43.571721  43.627508  43.134688  6.623697e+06
2010-02-18  43.396970  43.769598  43.125218  6.460454e+06
2010-02-19  43.390687  43.704347  43.154311  6.660305e+06
2010-02-22  44.004548  43.785487  43.455306  6.427562e+06
2010-02-23  43.152945  42.754581  42.491308  7.270832e+06
2010-02-24  43.480865  43.755306  43.167400  6.697727e+06
2010-02-25  43.201386  43.771350  42.772043  7.895413e+06
2010-02-26  43.703560  43.767877  43.281258  7.223996e+06
'''

# 6. For 2012, find the date with the maximum average relative volatility for all stocks and the date with
# the minimum average relative volatility for all stocks. (Consider only days when the market is open.)

#Get all stocks where the date is in 2012
yearStocks = stocks[stocks['Date'].dt.year == 2012]
#Group by date to get each individual date and find mean of rel volatility
yearVols = yearStocks.groupby('Date')['RelVolatility'].mean()

#Index of max and min rel vol is the top and bot day
print('Top volatility: ', yearVols.idxmax().strftime("%D"))
print('Bottom volatility: ', yearVols.idxmin().strftime("%D"))

'''
6.
Top volatility:  06/21/12
Bottom volatility:  12/24/12
'''


# 7. For 2008-2013, for each day of the week, find the average relative volatility for all stocks. (Consider
# only days when the market is open.)

#Get  all stocks where date is in range
rangeStocks = stocks[(stocks['Date'].dt.year >= 2008) & (stocks['Date'].dt.year <= 2013)]
#Groub by english weekdays and take mean of Relvolatility for each weekday
weekdayVols = rangeStocks.groupby(rangeStocks['Date'].dt.strftime('%A'))[['RelVolatility']].mean()
print(weekdayVols)

'''
7.
          RelVolatility
Date                    
Friday          0.029041
Monday          0.028542
Thursday        0.031066
Tuesday         0.029436
Wednesday       0.029766
'''

# 8. The “Python Index” is designed to capture the collective movement of all of our stocks. For each date,
# this is defined as the average price for all stocks for which we have data on that day, weighted by the
# volume of shares traded for each stock. That is, for stock values S1, S2, . . . with corresponding sales
# volumes V1, V2, . . ., the average weighted by volume is
# S1V1 + S2V2 + · · ·
# V1 + V2 + · · ·
# Find the Open, High, Low, and Close for the Python Index for each day the market was open in
# October 2010. Give a table the includes the Date, Open, High, Low, and Close, with one date per row.

#Get all stocks within month and year
dayStocks = stocks[(stocks['Date'].dt.month == 10) & (stocks['Date'].dt.year == 2010)]
#Create new column to specify weight of each stock value based on volume
#Weight is the  volume for that stock, divided all volumes for that day summed
#Groupby date gives us all stocks for that day and transform sum gives the volume sum for that day (group object)
dayStocks['weight']  = dayStocks['Volume'] / dayStocks.groupby('Date')['Volume'].transform('sum')
#Make columns for each index value, by multiplying each rows values by its corresponding weight
dayStocks['OpenIndex'] = dayStocks['Open'] * dayStocks['weight']
dayStocks['CloseIndex'] = dayStocks['Close'] * dayStocks['weight']
dayStocks['HighIndex'] = dayStocks['High'] * dayStocks['weight']
dayStocks['LowIndex'] = dayStocks['Low'] * dayStocks['weight']

print(dayStocks.groupby('Date')[['OpenIndex','CloseIndex','HighIndex','LowIndex']].sum())

'''
8.
            OpenIndex  CloseIndex  HighIndex   LowIndex
Date                                                   
2010-10-01  39.272779   38.961689  39.540464  38.574467
2010-10-04  36.513664   36.473198  36.973598  36.039906
2010-10-05  36.868819   37.154517  37.448798  36.515236
2010-10-06  40.069422   39.453984  40.526281  38.790438
2010-10-07  38.738979   38.494185  38.982299  38.023149
2010-10-08  33.953131   34.141493  34.418515  33.601610
2010-10-11  36.415035   36.331342  36.840357  35.996804
2010-10-12  36.550699   36.956121  37.148552  36.185750
2010-10-13  36.769845   36.830507  37.277431  36.410377
2010-10-14  31.929174   31.746258  32.188759  31.399433
2010-10-15  31.379396   31.058207  31.574286  30.611508
2010-10-18  34.735203   34.947873  35.208943  34.389509
2010-10-19  33.418144   33.171654  33.812511  32.833834
2010-10-20  33.225863   33.555329  33.908320  32.849706
2010-10-21  40.968005   40.945613  41.634092  40.219655
2010-10-22  40.206448   40.424731  40.821101  39.843407
2010-10-25  35.196479   35.002647  35.525335  34.779042
2010-10-26  37.425957   38.095958  38.443149  37.176602
2010-10-27  40.800620   40.981265  41.430831  40.293345
2010-10-28  38.377249   38.085284  38.645428  37.617353
2010-10-29  40.159713   40.279059  40.638799  39.741861
'''