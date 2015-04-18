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

#Plot distribution of outcome variable:
data.version_count.hist(bins = 70, grid = False)
sns.despine(left = True, right = True, bottom = True)
plt.title('Distribution of version counts (the outcome variable; can also be\n\
    thought of as a piracy index), n = 3979')
plt.show()

