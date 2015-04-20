import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
# sns_palette = sns.color_palette(colors, desat = .7)
sns.set(style = 'white')
import numpy as np
import re

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']

#Get basic descriptives for all columns:
for col in data:
    # print data[col][data[col].notnull()].describe()
    print data[col].describe()

#Remove any 0s in version_count, because you don't know if these come from
#incorrect putlocker urls or from the movie actually not being up there.
data2 = data[data.version_count != 0]
print len(data2) #Was 3979 rows, now 3096 rows.

#Plot the distribution of the outcome variable:
data2.version_count.hist(bins = 65, grid = False)
sns.despine(left = True, right = True, bottom = True)
print len(data2.version_count)
plt.title('Distribution of version counts (the outcome variable; can also be\n\
    thought of as a piracy index), after removing version_count = 0, n = 3096')
plt.show()
#Cumulative distribution:
sorted_data = np.sort(data2.version_count)
plt.step(sorted_data, np.arange(sorted_data.size))
plt.title('Cumulative distribution plot of version counts (the outcome\
 variable; can also be thought \nof as a piracy index), after removing\
 version_count = 0, n = 3096')
plt.xlabel('Version count')
plt.ylabel('# of movies with fewer versions')
plt.show()

#Remove movies that have version_count = 1 and re-do histogram:
data3 = data2[data2.version_count != 1]
print len(data3) #Was 3096, now 2856.

#Re-plot histogram:
data3.version_count.hist(bins = 60, grid = False)
sns.despine(left = True, right = True, bottom = True)
print len(data3.version_count)
plt.title('Distribution of version counts (the outcome variable; can also be\n\
    thought of as a piracy index), after removing version_count = 0, n = 3096')
plt.show()

#Calculate summary stats for the outcome variable:
print np.mean(data3.version_count) #8.10
print np.var(data3.version_count) #32.32
print np.median(data3.version_count) #6



#***----The goal below is to look at version_count by studio, but only for
#studios that have at least 50 movies.

#Figure out how many rows each studio has:
studios = set(data2.studio_name)
studio_movie_counts = {}
for studio in studios:
    movie_count = len(data2[data2.studio_name == studio])
    studio_movie_counts[studio] = movie_count

#Remove studios that have under 50 movies:
for i, v in studio_movie_counts.items():
    if v < 50:
        del studio_movie_counts[i]


#Get basic descriptives about version_count by studio_name:
grouped = data2.groupby(by = ['studio_name']).mean()
version_count_by_studio = grouped['version_count']


version_count_by_studio.plot(kind = 'bar')
plt.show()

