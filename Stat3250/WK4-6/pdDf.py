##
## File: week04a.py (STAT 3250)
## Topic: "DataFrame" in pandas (mostly)
##

import numpy as np # load numpy as np
import pandas as pd # load pandas as pdls

## A quick Series item

enrolls = pd.Series([235, 119, 184, 44, 47, 71, 76]) # A sample series
len(enrolls)  # The length of the Series. (Handy at various times.)


## Creating a DataFrame for demonstration

data = {'Course':['STAT 3A','STAT 3A','STAT 3A','STAT 3B','STAT 3B'],
        'Time':['MW200','TR930','TR330','MW1000','MWF900'],
        'Sect':[1,2,4,1,2],
        'Enroll':[41,46,39,78,84]}
df = pd.DataFrame(data, columns=['Course','Sect','Time','Enroll'])
df

# The index is set by default to 0, 1, 2, ...
# We can change it to ['A','B','C','D','E'] for demonstration
df.index = ['A','B','C','D','E']
df

## Extracting subsets of a DataFrame
# Columns
df['Enroll']  # The column 'Enroll'
df.loc[:,'Enroll'] # Same as above, but with .loc
df[['Course','Time']] # The columns Course, Time
df.loc[:,'Sect':'Enroll'] # The slice Sect-Enroll, all rows

# Rows
df.loc['D',:] # Row D, but mildly annoying format
df.loc[['D'],:]  # Row D as dataframe
df.loc[['B','D'],:] # Rows B and D, all columns

# Columns and Rows
df.loc[['E','C'],'Time'] # Rows E, C, and column Time (type = Series)
df.loc[['B','A','E'],['Enroll','Sect']] # Rows B,A,E; Columns Enroll, Sect

#df.loc[0:3,'Time'] # Want rows 1-3, with Time; This doesn't work

# Alternatives
df.loc[df.index[0:3],'Time'] # This works by swapping row numbers for index
df.loc[:,'Time'].iloc[0:3] # An alternative that is perhaps less clear

# Examples of masking
df[df['Enroll'] < 50]  # Slightly surprising that this produces rows
df.loc[df['Enroll'] < 50]   # These give the same thing
df.loc[df['Enroll'] < 50,:] 

df.loc[df['Sect'] == 2, ['Time','Enroll']] # Time, Enroll for Sect=2

np.median(df.loc[(df['Sect']==1) & (df['Course']=='STAT 3A'), 'Enroll'])
np.mean(df) # Computes mean of all columns where it makes sense

# Sorting
sorteddf = df.sort_values(by = 'Enroll') # Sort by Enroll value
sorteddf = df.sort_values(by = 'Enroll', ascending=False) # Reverse direction

sorteddf.iloc[0:2,:]

## Reading in a .csv file

grades = pd.read_csv('samplegrades.csv',index_col=0)
grades  # Note some values are NaN (missing)





