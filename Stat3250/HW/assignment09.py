## File: Assignment09.py (STAT 3250)
## Topic: Assignment 09
## Name: Gabriel Groover
## Section time: 330-445
## Grading group: 2

import pandas as pd # load pandas as pd
import numpy as np
import datetime
import re

#Read in csv file, tab separated and label the columns
reviews = pd.read_csv('reviews.txt', 
                        sep='\t',
                        header=None,
                        names=['Reviewer','Movie','Rating','Date'])

movies = pd.read_csv('genres.txt',
						sep='|',
						header=None,
						names=['Id', 'Title', 'Release', 'Video Release', 'Url',
						'Unknown', 'Action', 'Adventure', 'Animation', 'Childrens', 
						'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'FilmNoir',
						'Horror', 'Musical', 'Mystery', 'Romance', 'ScFi', 'Thriller',
						'War', 'Western'])

reviewers = pd.read_csv('reviewers.txt',
						sep='|',
						header=None,
						names=['Id', 'Age', 'Gender', 'Occupation', 'Zipcode'])

zips = pd.read_csv('zipcodes.txt',    # Read in zip codes, eliminate dups
                  usecols = [1,4],
                  converters={'Zipcode':str}).drop_duplicates()

# 1. Find the 5 reviewers with the most reviews, and then use their reviews to find a 95% confidence
# interval for their average rating (taken as a group). Then find the average rating for the remainder
# of the reviewers. Is this average within the top-5 confidence interval? Here the sample sizes are quite
# large, so we can use the confidence interval formula
# x¯ ± 1.96
# s
# √
# n
# where s is the standard deviation with ddof = 1.

#Group reviews by reviewer column and count occurences of each reviewer
byReviewer = reviews.groupby('Reviewer').count()
#Sort to find top most frequest reviewers and take top 5
indexes = byReviewer.sort_values('Movie',ascending=False).index[:5]
print('Top Reviewer Indexes: ', indexes)
#Get all reviews by top reviewers
topReviewers = reviews[reviews['Reviewer'].isin(indexes)]

#N and S for matching reviews
n = len(topReviewers)
s = topReviewers.std(ddof=1)['Rating']
xBar = topReviewers.sum()['Rating'] / n
#Plug into formula and  print range as a tuple
upperLimit = xBar + 1.96 * ( s / np.sqrt(n))
lowerLimit = xBar - 1.96 * ( s / np.sqrt(n))
print((lowerLimit, upperLimit))

#Get all the reviews not by top 5
remainingReviews = reviews[~reviews['Reviewer'].isin(indexes)]
#Print the mean rating
print('Average remaining rating: ', remainingReviews.mean()['Rating'])
print("This is outside the confidence interval.")

'''
1.
Top Reviewer Indexes:  Int64Index([405, 655, 13, 450, 276], dtype='int64', name='Reviewer')
(2.9048586350882037, 2.9975803893020401)
Average remaining rating:  3.54847033566
This is outside the confidence interval.
'''

# 2. Which movies were the top-10 based on of number of times reviewed? (Provide the movie title and
# the number of times reviewed for each. If there is a tie for 10th place, include all that tied.)

#Group all reviews by movie and count occurences of each
#Sort descending and take top ten (I verified there were no ties)
topMovies = reviews.groupby('Movie').count().sort_values('Reviewer', ascending=False)[:10]
#Contruct new DF using movie id and count to merge with genres
topMovies = pd.DataFrame({"Id":topMovies.index, "Count":topMovies['Reviewer']})
#Get title column of all movies whos id is in top ten
movieNames = movies[movies['Id'].isin(topMovies.index)][['Title', 'Id']]
#Print merged dataset that has count col for number of reviews and title
print(pd.merge(movieNames,topMovies,on='Id'))

'''
2.
                           Title   Id  Count
0               Toy Story (1995)    1    452
1               Star Wars (1977)   50    583
2                   Fargo (1996)  100    508
3  Independence Day (ID4) (1996)  121    429
4      Return of the Jedi (1983)  181    507
5                 Contact (1997)  258    509
6    English Patient, The (1996)  286    481
7                  Scream (1996)  288    478
8               Liar Liar (1997)  294    485
9           Air Force One (1997)  300    431
'''


# 3. Which genre occurred most often, based on the number of reviews. Which was least often? (Don’t
# include “unknown” as a genre.)


#Reneame review and movie columns to movieId so they can be merged
moviesIds = movies.rename(columns={'Id':'MovieId'})
reviewIds = reviews.rename(columns={'Movie':'MovieId'})
#Merge on movieId
reviewGenre = pd.merge(moviesIds,reviewIds, on='MovieId')

#Get just the columns that contain movie genre bits
reviewGenreCounts = reviewGenre[['Action', 'Adventure', 'Animation', 'Childrens', 
						'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'FilmNoir',
						'Horror', 'Musical', 'Mystery', 'Romance', 'ScFi', 'Thriller',
						'War', 'Western']]

#Sum columns and print the genre (column) that had max and min
print("Most common:", reviewGenreCounts.sum().idxmax())
print("Least common:", reviewGenreCounts.sum().idxmin())

'''
3.
Most common: Drama
Least common: Documentary
'''

# 4. What percentage of reviews are for movies classified in at least two genres?

#Add a new column that is a rowwise sum of just genre columns
reviewGenreCounts['genreSum'] = reviewGenre.loc[:,'Action':'Western'].sum(axis=1)
#Divide number of elements in this column that have 2+ reviews by total reviews
print(len(reviewGenreCounts[reviewGenreCounts['genreSum'] >= 2]) / len(reviewGenreCounts) * 100, '%', sep="") 

'''
4.
69.938%
'''

# 5. Give a 95% confidence interval for the average rating for male reviewers, and do the same for female
# reviewers.

#Extract just move ids to index column so we can use them later
genders = reviewers.set_index('Id')
#Get all indexes (ids) of male and female reviewers
maleIds = genders[genders['Gender'] == 'M'].index
femaleIds = genders[genders['Gender'] == 'F'].index

#Get reviews in each of those id lists
maleReviews = reviews[reviews['Reviewer'].isin(maleIds)]
femaleReviews = reviews[reviews['Reviewer'].isin(femaleIds)]

#Get mean, n and std for male and female
n_male = len(maleReviews)
n_female = len(femaleReviews)
s_male = maleReviews.std(ddof=1)['Rating']
s_female = femaleReviews.std(ddof=1)['Rating']
maleMean = maleReviews.mean()['Rating']
femaleMean = femaleReviews.mean()['Rating']

#Plug in for each
mLower = maleMean - 1.96 * (s_male / np.sqrt(n_male))
mUpper = maleMean + 1.96 * (s_male / np.sqrt(n_male))
fLower = femaleMean - 1.96 * (s_female / np.sqrt(n_female))
fUpper = femaleMean + 1.96 * (s_female / np.sqrt(n_female))

#Print range as a tuple
print("Male:", (mLower, mUpper))
print("Female:", (fLower, fUpper))

'''
5.
Male: (3.5213085280777978, 3.5372694412192667)
Female: (3.5172022879993174, 3.5458124750154458)
''' 

# 6. Which locations (state, territory, or Canada) formed the top-10 for number of reviews? (Provide a
# table of location and number of reviews. The location ’unknown’ should not be included.)

#Convert read in zip codes to a series using the state as value and code as index
zipseries = pd.Series(data=zips['State'].values, index=zips['Zipcode'])

#Function that given row, extracts zipcode and returns the state, canada or unknown
def ziptostate(row):
	if re.search('[a-zA-Z]', row['Zipcode']):
		return 'Canada'
	elif row['Zipcode'] in zipseries:
		return zipseries[row['Zipcode']]
	else:
		return 'Unknown'

#Add new column based on applying func to each row
reviewers['State'] = reviewers.apply(ziptostate, axis=1)

#Rename the id column of each to match
reviewers = reviewers.rename(columns={'Id': 'ReviewerId'})
reviews = reviews.rename(columns={'Reviewer': 'ReviewerId'})

#Merge reviews with reviewers to have combined data
mergedData = pd.merge(reviews, reviewers, on='ReviewerId')

#Grouby merged data by state and count appearances of  each
#Sort descending  by random col to get top entries and slice top 10
#Finally rename col containing counts to something sensible
top10 = mergedData.groupby('State').count().sort_values('Movie',ascending=False)[:10].rename(columns={'ReviewerId':'NumReviews'})
print(top10[['NumReviews']])

'''
6.
       NumReviews
State            
CA          13842
MN           7635
NY           6882
IL           5740
TX           5042
OH           3475
PA           3339
MD           2739
VA           2590
MA           2584
'''

# 7. Find the occupations that gave the highest average reviews, and the lowest average reviews. (Here
# “other” and “none” are not occupations, but “student” is.)

#Grab only reviews that are  not none or other for occupations
excludeNone = mergedData[(mergedData['Occupation'] != 'none') & (mergedData['Occupation'] != 'other')]
#Group on occupation, find  mean of  each col, and sort by rating descending
#Extract just rating column and slice top and bottom 5
meanRatings = excludeNone.groupby('Occupation').mean().sort_values('Rating',ascending=False)['Rating']
print('Top rating occupation:\n' ,meanRatings.idxmax())
print('Bottom rating occupation:\n', meanRatings.idxmin())

'''
7.
Top rating occupation:
 lawyer
Bottom rating occupation:
 healthcare
'''

#8. What percentage of movies have exactly 1 review? 2 reviews? 3 reviews? Continue to 20 reviews.

#Group by movie to get review cocunts
reviewCounts = mergedData.groupby('Movie').count()
#Make new dataframe containing moviecounts and movieId
reviewCounts = pd.DataFrame({'Id':reviewCounts['ReviewerId'].index, 'Count':reviewCounts['ReviewerId']})
#Use new id column to merge with genres
genreCounts = pd.merge(reviewCounts, movies, on='Id')
#Get all elements that should be in our final dataset and group by count again to move all <20 together. 
#The count occurence of each number and take arbitrary column
genreCountsGrouped = genreCounts[genreCounts['Count'] <= 20].groupby('Count').count()['Id']

#Print out occurences of each divided by total movies element-wise and convert to percent
print(genreCountsGrouped / len(movies) * 100)

'''
8.
Count
1     8.382878
2     4.042806
3     3.567182
4     3.804994
5     3.032105
6     2.318668
7     2.615933
8     1.783591
9     1.961950
10    1.961950
11    1.189061
12    1.664685
13    1.486326
14    0.832342
15    1.307967
16    1.129608
17    0.594530
18    1.426873
19    1.070155
20    0.713436
Name: Id, dtype: float64
'''

#9. Which genre had the highest average review, and which had the lowest average review?

#Rename columns of each to merge later
movies = movies.rename(columns={'Id':'MovieId'})
mergedData = mergedData.rename(columns={'Movie':'MovieId'})

#Merge everything together
merged_with_movies = pd.merge(movies, mergedData, on='MovieId')

genreList = ['Action', 'Adventure', 'Animation', 'Childrens', 
						'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'FilmNoir',
						'Horror', 'Musical', 'Mystery', 'Romance', 'ScFi', 'Thriller',
						'War', 'Western']
#Loop through every genre, and add tuple containing genre name and average rating (from rows where that genre col is 1) to list
genreAvgs = []
for genre in genreList:
	genreAvgs.append((genre, merged_with_movies[merged_with_movies[genre] == 1].mean()['Rating']))

#Sort by second val of tuple
genreAvgs = sorted(genreAvgs, key=lambda x: x[1])
#Print out first value of first and last element (the genre)
print('Min:', genreAvgs[0][0])
print('Max:', genreAvgs[-1][0])

'''
9.
Min: Fantasy
Max: FilmNoir
'''

# 10. Suppose that a “positive review” is one with a rating of 4 or 5.
# (a) Find a 95% confidence interval for pf − pm, where pf is the proportion of positive reviews from
# females and pm is the proportion of positive reviews from males. Is there evidence that the
# proportions differ?

#Get all reviews by male and female reviewer separately
maleReviews = mergedData[mergedData['Gender'] == 'M']
femaleReviews = mergedData[mergedData['Gender'] == 'F']
#Get male/female reviews that are also positive separately
posMale = maleReviews[maleReviews['Rating'] >= 4]
posFemale = femaleReviews[femaleReviews['Rating'] >= 4]

#Get proportions and lengths from above datasets
n_male = len(maleReviews)
n_female = len(femaleReviews)
p_male = len(posMale) / n_male
p_female = len(posFemale) / n_female

#Proportion differencec
difference = p_female - p_male
#Plug into formula and add to difference
upperBound = difference + 1.96 * np.sqrt(p_female*(1-p_female)/n_female + p_male*(1-p_male)/n_male)
lowerBound = difference - 1.96 * np.sqrt(p_female*(1-p_female)/n_female + p_male*(1-p_male)/n_male)
#Print as tuple
print((lowerBound, upperBound))
print('There is not significant difference that the proportions differ.')

'''
10a.
(-0.0057658579712690323, 0.0083267378550685271)
There is not significant difference that the proportions differ.
'''

# (b) It is thought that Canadians are nicer than Americans. Find a 95% confidence interval for
# pC −pA, where pC is the proportion of positive reviews from Canadians, and pA is the proportion
# of positive reviews from Americans. (Exclude those whose location is unknown.) Is there evidence
# that Canadians give more positive reviews?

#Get all reviews by canadian and american reviewers separately (not unknowns)
canReviews = mergedData[mergedData['State'] == 'Canada']
amerReviews = mergedData[(mergedData['State'] != 'Canada') & (mergedData['State'] != 'Unknown')]
#Get Can/Amer reviews that are also positive separately
posCan = canReviews[canReviews['Rating'] >= 4]
posAmer = amerReviews[amerReviews['Rating'] >= 4]

#Get proportions and lengths from above datasets
n_can = len(canReviews)
n_amer = len(amerReviews)
p_can = len(posCan) / n_can
p_amer = len(posAmer) / n_amer

difference = p_can - p_amer
#Plug into formula and add to difference
upperBound = difference + 1.96 * np.sqrt(p_can*(1-p_can) / n_can + p_amer*(1-p_amer) / n_amer)
lowerBound = difference - 1.96 * np.sqrt(p_can*(1-p_can) / n_can + p_amer*(1-p_amer) / n_amer)
#Print as tuple
print((lowerBound, upperBound))
print('There is evidence that Canadians actually give less positive reviews.')

'''
10b.
(-0.069417374393881695, -0.026050239950439692)
There is significant difference that the proportions differ.
'''



