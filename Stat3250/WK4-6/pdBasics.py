##
## File: week04a.py (STAT 3250)
## Topic: "Series" in pandas
##

#### The Series object in pandas

import pandas as pd # load pandas as pd
import  sys

print(pd.__version__)

enrolls = pd.Series([235, 119, 184, 44, 47, 71, 76])
enrolls

# In the output, the first column is the index
# and the second column are the values.  If no 
# index is provided, then 0, 1, 2, ... is the
# default.

# We can extract values from a Series with the 
# usual square bracket notation.

enrolls[2] # 3rd entry
enrolls[4:6] # 5th and 6th entries

# We can add our own index to the Series, which provides
# context to the enrollments.

enrolls = pd.Series([235, 119, 184, 44, 47, 71, 71],
            index=['STAT 2120','STAT 2220','STAT 2320',
            'STAT 3080','STAT 3180','ECON 3720','ECON 3730'])
enrolls

enrolls.values # Just the values of the Series
enrolls.index # And the index

# We can use the index to reference subsets of the Series 

enrolls['STAT 3080'] # Just STAT 3080
enrolls[['STAT 2120','ECON 3720']] # STAT 2120 and ECON 3720
#enrolls['STAT 3080':'ECON 3720'] # Slicing works

# We can extract the values from subsets of a Series
enrolls['STAT 2120'].values # Just the STAT 2120 enrollments
enrolls[['STAT 3080','ECON 3720']].values # STAT 3080, ECON 3720

# The function 'iloc' allows reference to the implicit index 
# (the default 0, 1, 2, ...) of a Series.
# This might be handy, depending on the situation.
enrolls.iloc[3:6] # Entries indexed by 3-5
enrolls.iloc[2] # Enrollment for 3rd STAT 2120 section
enrolls.iloc[2:3] # Subseries with just 3rd STAT 2120

# The function 'loc' is the counterpart to 'iloc' that
# references the explicit index.  
enrolls.loc['STAT 3080'] # Just STAT 3080
enrolls.loc[['STAT 2120','ECON 3720']] # STAT 2120 and ECON 3720
#enrolls.loc['STAT 3080':'ECON 3720'] # Slicing works

# Our practice will be to use 'loc' and 'iloc' to make
# it clear whether we are referencing the explicit or
# implicit index.  The next example better illustrates
# the advantage of this. 

## Changing the index, and 'loc'

# Define a Series of exam scores
scores = pd.Series([87,73,91,80,90,77,85,95,97,71])
scores  # Scores has the default index 0, 1, ....

scores.index = scores.index+1 # Add 1 to the indices
scores

# The 'loc' function will reference the exact values of
# the index, without the usual Python index adjustments for 
# lists and arrays
scores.loc[3] # The 3rd score
scores.loc[5:7] # Scores 5-7
scores.loc[:6] # The first 6 scores
scores.loc[8:] # Scores 8-10
scores.loc[::2] # Every other score

# When there is no specific index for a Series of data,
# it can simplify your code (and make it more readable) 
# if you do as above: reset the index to 1, 2, 3, ...
# and use 'loc' for the referencing.  (No more trying
# to remember "Do I subtract 1?  Or is it add 1?")

## Reading in data:
#   * Download 'fastfood1.csv' from Collab
#   * Place 'fastfood1.csv in same folder as this file
#   * Click "folder" icon in upper left, select the folder
#     containing this file.
#   * Run command below.
ff = pd.read_csv('fastfood1.csv',index_col=0)
type(ff)

# Pandas reads the data in as a DataFrame, but we're
# looking at Series today, so we this trick to convert. 
ff = ff.iloc[:,0] # Selects all rows, first column.
type(ff)

# Some examples of slicing
ff.loc[10]  # All records from store 10
ff.loc[[23,45,822]] # All records from stores 23,45,822
ff.loc[20:30]   # This won't work because store numbers are
                # mixed together.  Sorting by index will fix it.
           
ff = ff.sort_index() # This sorts by index
ff 
ff.loc[20:30] # Now this works.

# Masking also works
ff.loc[ff.index <= 10] # All records for store numbers 10 or lower
ff.loc[ff.index <= 10].values # Just the values, as an array
ff.loc[ff.values == 30] # All records with time = 30
# All records with times between 45 and 50.
ff.loc[(ff.values >= 45) & (ff.values <= 50)]   