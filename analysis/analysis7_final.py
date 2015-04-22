import scipy.stats as sci
import pandas as pd, numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random
import seaborn as sns
sns.set(style = 'white')
data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']

#***---DATA PREP-----------------------

#Drop rows that are incomplete for any predictor columns:
predictor_columns = ['total_gross', 'major_award_wins_or_noms','release_width',
    'metascore', 'imdb_rating', 'votecount_clean', 'fame', 'fame_actor2'] 
data = data[data.release_width < 50000]
data = data.dropna(subset = predictor_columns)

#Transform predictors:
data = data[data.fame_actor2 > 0]
data = data[data.fame > 0]
data['log_average_fame'] = ((data.fame + data.fame_actor2)/2)
data['log_gross'] = np.log(data.total_gross)
data['log_release_width'] = np.log(data.release_width)
data['log_votecount'] = np.log(data.votecount_clean)

#Separate data into training (75%) and test (25%) sets:
rows = random.sample(data.index, len(data)/4)
training_data = data.drop(rows)
test_data = data.ix[rows]

#***---EXPLORE DATA-----------------------

#Histogram of outcome variable:
plt.hist(training_data.total_gross/1000000, bins = 30)
plt.title('Distribution of movie total grosses in millions of $.\nTraining\
 data only, n = 1227', fontsize = '20')
#The far-right outlier is the Dark Night (2008)
plt.xlabel('Millions of dollars made', fontsize = '20')
plt.ylabel('Number of movies in dataset', fontsize = '20')
sns.despine()
plt.show()

#Scatterplot matrix of predictors:
scatter_data = training_data[['log_gross', 'log_release_width', 'metascore', 
    'log_average_fame', 'major_award_wins_or_noms', 
    'log_votecount']]
sns.pairplot(scatter_data, size = 2.5, )
plt.xlabel('')
plt.ylabel('')
plt.show()

#***---RUN MODEL AND EVALUATE-----------------------
#PREDICT LOG TOTAL GROSS FROM RELEASE WIDTH:
predictors = ['log_release_width', 'metascore', 'log_average_fame',
    'major_award_wins_or_noms', 'log_votecount']
X = training_data[predictors]
X = sm.add_constant(X)
y = training_data.log_gross
model = sm.OLS(y, X)
results = model.fit()
print results.summary()

#Plot hist of residuals:
resids2 = results.resid
plt.hist(resids2)
plt.title('Histogram of residuals')
plt.show()

#1. Plot the model's predicted ys vs observed ys
td = training_data
b = results.params
predicted_x = b[0] + b[1]*td.log_release_width + b[2]*td.metascore +\
    b[3]*td.log_average_fame + b[4]*td.imdb_rating +\
    b[5]*td.major_award_wins_or_noms + b[6]*td.votecount_clean

plt.scatter(results.predict(X), y, facecolors = 'none', edgecolors = 'black')
plt.title('Model predicted log(total_gross) vs observed log(total_gross)')
plt.xlabel('Overall x')
plt.ylabel('Observed log(total_gross)')
plt.show()

#2a Predict test set ys from test set Xs:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)

#2b. Plot the model against test set ys

#3. Plot the unlogged residuals (from test set?)


