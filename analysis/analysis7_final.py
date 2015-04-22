import scipy.stats as sci
import pandas as pd, numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import random
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

#Separate data into training (75%) and test (25%) sets:
rows = random.sample(data.index, len(data)/4)
training_data = data.drop(rows)
test_data = data.ix[rows]

#***---EXPLORE DATA-----------------------
#Make scatterplot matrix of predictors to look for multicollinearity, and also
#to see how predictors are related to outcome var. 

#***---RUN MODEL AND EVALUATE-----------------------
#PREDICT LOG TOTAL GROSS FROM RELEASE WIDTH:
predictors = ['log_release_width', 'metascore', 'log_average_fame',
    'imdb_rating', 'major_award_wins_or_noms', 'votecount_clean']
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

#1. Plot the entire model against observed ys


#2a Predict test set ys from test set Xs:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)

#2b. Plot the model against test set ys

#3. Plot the unlogged residuals (from test set?)


