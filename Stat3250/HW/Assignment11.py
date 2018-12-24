## File: Assignment11.py (STAT 3250)
## Topic: Assignment 11
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import  zipfile
import  pandas as pd
import numpy as np

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
stocks['Date'] = pd.to_datetime(stocks['Date'])


# 1. Use the collective data to determine when the market was open from January 2, 2005 to December 31,
# 2014. (Do not use external data for this question.) Report the number of days the market was open
# for each year 2005-2014. (Include the year and the number of days in table form.)

#Get all entries within timeframe
yearRange = stocks[(stocks['Date'].dt.year >= 2005) & (stocks['Date'].dt.year <= 2014)]
#Count days in each year by grouping by each and counting
yearRangeDays = yearRange.groupby('Date').count()
yearRangeYears = yearRangeDays.groupby(yearRangeDays.index.year).count()

#Rename column and  print
yearRangeYears['NumDays'] = yearRangeYears['Open']
print(yearRangeYears[['NumDays']])

'''
1.
      NumDays
Date         
2005      252
2006      251
2007      251
2008      253
2009      252
2010      252
2011      252
2012      250
2013      252
2014      252
'''

# 2. Determine the total number of missing records for all stocks for the period 2005-2014.

#Create a list of all unique stock symbols
stockList = stocks['Stock'].unique()
#List of dataframe for each stock
dfList = []

#Iterate through each stock
for s in stockList:

	#Get all entries for a given stock and find the min and  max
	stockDates =  stocks[stocks['Stock'] == s]
	minDate = stockDates['Date'].min()
	maxDate = stockDates['Date'].max()

	#Get all stock entries within timeframe for given stock and find uniques (days market was open)
	numDays = stocks[(stocks['Date'] >= minDate) & (stocks['Date'] <= maxDate)]['Date'].unique()
	#Get unique days just for given stock
	stockDays = stockDates['Date'].unique()
	#Find difference between two sets (days market was open but stock has no entry)
	missingDays = np.setdiff1d(numDays, stockDays)

	#Construct a frame from all missing dates and mark with stock symbol
	missingDays_frame = pd.DataFrame({'Date':missingDays, 'Stock':s})
	#Mask final dataframe to correct range
	missingDays_frame = missingDays_frame[(missingDays_frame['Date'].dt.year >= 2005) & (missingDays_frame['Date'].dt.year <= 2014)]
	#Get open days within timeframe
	numDaysInRange = yearRange[(yearRange['Date'] >= minDate) & (yearRange['Date'] <= maxDate)]['Date'].unique()
	#Add new dataframe column with proportion of missing days
	missingDays_frame['Proportion'] = len(missingDays_frame) / len(numDaysInRange)

	#Add stock's frame to list
	dfList.append(missingDays_frame)

#Concat all frames together
missingDf = pd.concat(dfList)
missingDf = missingDf[(missingDf['Date'].dt.year >= 2005) & (missingDf['Date'].dt.year <= 2014)]

#Count all missing entries
print(len(missingDf))

'''
2.
9459
'''

# 3. For the period 2005-2014, find the 10 stocks (plus ties) that had the most missing records, and the 10
# stocks (plus ties) with the fewest missing records. (For the latter, don’t include stocks that have no
# records for 2005-2014.) Report the stocks and the number of missing records for each.

#Group missing entries by stock and count each
countMissing = missingDf.groupby('Stock').count()
#Use list of tickers and combine with list missing stock counts, fill rows that aren't  missing any with 0 and sort
countMissing = pd.Series(index=stockList).align(countMissing, fill_value=0)[1].sort_values(by='Date',ascending=False)

#Print top 14 entries to include ties
print(countMissing[:14]['Date'])
#Print bottom 10
print(countMissing[-10:]['Date'])

'''
3.
PDCO    45
STJ     44
SO      44
FLR     44
GE      43
RF      43
PPG     43
QCOM    42
HOT     42
LVLT    42
BBT     42
GAS     42
SWN     42
LB      42
Name: Date, dtype: int64
TRIP    0
NWSA    0
NLSN    0
NAVI    0
LYB     0
GM      0
FB      0
XYL     0
ADT     0
ZTS     0
Name: Date, dtype: int64
'''

# 4. Repeat the previous question, this time for the stocks with the greatest and least proportion of missing
# records during 2005-2014. Report the stocks and the number of missing records for each.

#Group missing  entries by stock and sort by proportion values from earlier dataframe
countProp = missingDf.groupby('Stock').mean()
#Use list of tickers and combine with list missing stock counts, fill rows that aren't  missing any with 0 and sort
countProp = pd.Series(index=stockList).align(countProp, fill_value=0.000000)[1].sort_values(by='Proportion',ascending=False)

#Print top and bottom 10 including ties
print(countProp[:15])
print(countProp[-10:])

'''
4.
       Proportion
Stock            
SO       0.018242
PDCO     0.017878
QCOM     0.017744
FLR      0.017481
STJ      0.017481
RF       0.017084
GE       0.017084
PPG      0.017084
GGP      0.016859
BBT      0.016687
HOT      0.016687
SWN      0.016687
LB       0.016687
LVLT     0.016687
GAS      0.016687
      Proportion
TRIP         0.0
NWSA         0.0
NLSN         0.0
NAVI         0.0
LYB          0.0
GM           0.0
FB           0.0
XYL          0.0
ADT          0.0
ZTS          0.0
'''

# 5. Identify the top-10 dates (plus ties) in 2005-2014 that were missing from the, most stocks.

#Group missing entries by day to count number on each day and sort
countDates = missingDf.groupby('Date').count().sort_values(by='Proportion',ascending=False)
#Get  top 10 plus ties
print(countDates[:10]['Stock'])

'''
5.
Date
2007-06-25    11
2012-04-23    11
2005-12-15    11
2013-01-30    10
2013-09-23    10
2011-03-08    10
2005-05-05    10
2005-07-14    10
2006-12-04    10
2005-02-28    10
Name: Stock, dtype: int64
'''

# 6. For each stock, impute (fill in) the missing records using linear interpolation. For instance, if d1 <
# d2 < d3 are dates, and P1 and P3 are opening prices on dates d1 and d3, respectively, then we estimate
# P2 (the opening price on date d2) with
# P2 =
# (d3 − d2)P1 + (d2 − d1)P3
# d3 − d1
# The same formula is used for the other missing values of High, Low, Close, and Volume.
# Use the imputed values to recalculate the Python Index (see Assignment 10 for the formula) for the
# open dates in 2007-2013. (Remember that weekends and holidays are not open dates, so don’t impute
# those.)
# (a) Find the Open, High, Low, and Close for the imputed Python Index for each day the market was
# open in October 2010. Give a table the includes the Date, Open, High, Low, and Close, with one
# date per row.

row_list = []

#Iterate through each stock
for s in stockList:

	#Get all entries for that stock and find start/end date for data
	stockDates =  stocks[stocks['Stock'] == s]
	minDate = stockDates['Date'].min()
	maxDate = stockDates['Date'].max()

	#Find number of open days during data period
	numDays = stocks[(stocks['Date'] >= minDate) & (stocks['Date'] <= maxDate)]['Date'].unique()
	stockDays = stockDates['Date'].unique()

	#Make dataframe of missing days for one stock
	missingDays = pd.to_datetime(np.setdiff1d(numDays, stockDays))

	#Iterate through each missing day
	for d2 in missingDays:

		#Get day before by finding  max of previous days 
		d1 = stockDates[stockDates['Date'] < d2]
		d1 = d1.ix[d1['Date'].idxmax()]

		#Get day after by finding min of following days
		d3 = stockDates[stockDates['Date'] > d2]
		d3 = d3.ix[d3['Date'].idxmin()]

		#Calculate date differences
		a = (d3['Date'] - d2).days
		b = (d2 - d1['Date']).days
		c = (d3['Date'] - d1['Date']).days

		#Interpolated data for each column
		day_open = (a * d1['Open'] + b * d3['Open']) / c
		day_close = (a * d1['Close'] + b * d3['Close']) / c
		day_high = (a * d1['High'] + b * d3['High']) / c
		day_low = (a * d1['Low'] + b * d3['Low']) / c
		day_vol = (a * d1['Volume'] + b * d3['Volume']) / c

		#Append new row to list
		row_list.append({'Date':d2, 'Open':day_open, 'High':day_high, 'Low':day_low, 'Close':day_close, 'Volume':day_vol,'Adj Close':None,'Stock':s})

#Concat new  dataframe from rows and add to original stock data
interpolated = pd.concat([stocks, pd.DataFrame(row_list)])
		

#Get all interpolated  data within timeframe
dayStocks = interpolated[(interpolated['Date'].dt.year >= 2008) & (interpolated['Date'].dt.year <= 2012)]

#Weight each column based on its proportion of total volume
dayStocks['weight']  = dayStocks['Volume'] / dayStocks.groupby('Date')['Volume'].transform('sum')
#Make columns for each index value, by multiplying each rows values by its corresponding weight
dayStocks['OpenIndex'] = dayStocks['Open'] * dayStocks['weight']
dayStocks['CloseIndex'] = dayStocks['Close'] * dayStocks['weight']
dayStocks['HighIndex'] = dayStocks['High'] * dayStocks['weight']
dayStocks['LowIndex'] = dayStocks['Low'] * dayStocks['weight']

#Filter just stocks from october and groupby day to get each value
octoberStocks = dayStocks[(dayStocks['Date'].dt.month == 10) & (dayStocks['Date'].dt.year == 2010)]
print(octoberStocks.groupby('Date')[['OpenIndex','CloseIndex','HighIndex','LowIndex']].sum())

'''
6a.
            OpenIndex  CloseIndex  HighIndex   LowIndex
Date                                                   
2010-10-01  39.169581   38.847595  39.434530  38.461729
2010-10-04  36.510926   36.470644  36.970777  36.037449
2010-10-05  36.821391   37.105123  37.397876  36.469230
2010-10-06  39.893535   39.300411  40.348672  38.636233
2010-10-07  38.711915   38.474292  38.958309  38.004147
2010-10-08  33.890921   34.078250  34.354389  33.540042
2010-10-11  36.729402   36.646461  37.154667  36.305414
2010-10-12  36.442557   36.841441  37.035612  36.078277
2010-10-13  36.963579   37.025214  37.470745  36.601837
2010-10-14  32.105693   31.928302  32.370234  31.580260
2010-10-15  31.384209   31.063536  31.578964  30.617056
2010-10-18  34.031321   34.226742  34.490335  33.683067
2010-10-19  33.253679   33.010323  33.645777  32.673050
2010-10-20  33.199450   33.527427  33.880878  32.823187
2010-10-21  40.940366   40.919451  41.605321  40.194412
2010-10-22  40.189095   40.410532  40.802296  39.830970
2010-10-25  35.343950   35.151389  35.672289  34.925287
2010-10-26  37.290510   37.953417  38.299406  37.040847
2010-10-27  39.112723   39.289454  39.718565  38.627671
2010-10-28  38.538390   38.267811  38.825426  37.787602
2010-10-29  39.347623   39.458878  39.811310  38.935350
'''


# (b) Determine the mean Open, High, Low, and Close imputed Python index for each month in 2008-
# 2012, and report that in a table that includes the month and year together with the corresponding
# Open, High, Low, and Close.

#Groupby date to find index for each day, then group by month and find mean
indexes = dayStocks.groupby('Date')[['OpenIndex','CloseIndex','HighIndex','LowIndex']].sum().reset_index()
print(indexes.groupby(indexes['Date'].dt.strftime("%Y-%m"))[['OpenIndex','CloseIndex','HighIndex','LowIndex']].mean())

'''
6b.
         OpenIndex  CloseIndex  HighIndex   LowIndex
Date                                                
2008-01  43.879383   43.879455  44.892409  42.818134
2008-02  44.312511   44.231277  45.094670  43.430333
2008-03  43.931635   43.933829  44.795459  43.048824
2008-04  44.443226   44.503364  45.155724  43.795947
2008-05  46.223506   46.240284  46.903393  45.527736
2008-06  43.551863   43.351498  44.206226  42.731014
2008-07  40.355927   40.294039  41.309069  39.296554
2008-08  41.288243   41.308876  42.040213  40.513061
2008-09  40.180907   39.998303  41.356652  38.654772
2008-10  31.236292   30.985339  32.628599  29.519426
2008-11  27.219452   27.058088  28.183572  25.990354
2008-12  26.335239   26.413611  27.183410  25.544060
2009-01  25.409133   25.308607  26.069218  24.567002
2009-02  21.604370   21.537163  22.229320  20.907962
2009-03  21.135608   21.201853  21.857057  20.461184
2009-04  23.071624   23.285297  23.851243  22.531289
2009-05  24.395802   24.428134  25.015676  23.782373
2009-06  26.374804   26.354770  26.816666  25.879218
2009-07  26.714240   26.811794  27.212668  26.268579
2009-08  28.961602   29.062931  29.516990  28.487846
2009-09  30.872073   30.899522  31.393763  30.383100
2009-10  32.438632   32.393257  32.937909  31.901634
2009-11  32.019869   32.113337  32.471559  31.640013
2009-12  32.763814   32.742729  33.119627  32.400190
2010-01  32.705986   32.608962  33.121490  32.155696
2010-02  33.132899   33.230161  33.590305  32.712490
2010-03  34.026824   34.099288  34.439033  33.705850
2010-04  36.493883   36.493005  36.989883  35.956138
2010-05  34.991162   34.919117  35.602147  34.217451
2010-06  34.969566   34.854441  35.442337  34.399057
2010-07  33.607538   33.652820  34.101586  33.069073
2010-08  35.069629   35.129022  35.561742  34.632379
2010-09  36.286588   36.384822  36.778156  35.907844
2010-10  36.660515   36.666509  37.134589  36.135863
2010-11  37.720691   37.807793  38.234390  37.284057
2010-12  39.662716   39.684723  40.081944  39.251770
2011-01  39.626213   39.667586  40.106999  39.128459
2011-02  42.111608   42.212864  42.680693  41.621860
2011-03  42.638494   42.651902  43.186795  42.078523
2011-04  42.867418   42.860279  43.353457  42.320513
2011-05  42.486394   42.498843  42.965594  41.996559
2011-06  39.442939   39.428882  39.915710  38.998463
2011-07  42.172371   42.201682  42.731904  41.674772
2011-08  34.352679   34.211051  35.003856  33.486768
2011-09  37.009378   36.725012  37.650239  36.107664
2011-10  34.838146   34.922552  35.551106  34.138827
2011-11  34.096725   34.019407  34.566951  33.503721
2011-12  33.602081   33.537572  34.031428  33.111160
2012-01  36.615057   36.824483  37.266753  36.128494
2012-02  37.729617   37.801535  38.218533  37.302312
2012-03  36.854072   36.917044  37.273991  36.465473
2012-04  38.646941   38.629491  39.105297  38.166190
2012-05  36.616235   36.460415  37.099327  36.010804
2012-06  35.507085   35.539954  35.974332  35.038382
2012-07  37.884296   37.910984  38.400811  37.362617
2012-08  37.160381   37.204773  37.574388  36.803358
2012-09  37.713443   37.760984  38.147519  37.328751
2012-10  38.252714   38.242168  38.763395  37.739419
2012-11  36.931831   36.988903  37.411101  36.523875
2012-12  37.350130   37.443758  37.825887  36.975137
'''