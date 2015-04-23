import pylab
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

#1. Histogram of outcome variable:
plt.hist(training_data.total_gross/1000000, bins = 30)
plt.title('Distribution of movie total domestic grosses in millions of $.\nTraining\
 data only, n = 1227', fontsize = '20')
#The far-right outlier is the Dark Night (2008)
plt.xlabel('Millions of dollars made', fontsize = '20')
plt.ylabel('Number of movies in dataset', fontsize = '20')
plt.xticks(fontsize = '16')
plt.yticks(fontsize = '16')
plt.annotate('Avatar', xy=(735, 5), xytext=(700, 40),
            arrowprops=dict(facecolor='black', shrink=0.05), fontsize = '16'
            )
sns.despine()
plt.show()

#2. Scatterplot matrix of predictors:
scatter_data = training_data[['log_gross', 'log_release_width', 'metascore', 
    'log_average_fame', 'major_award_wins_or_noms', 
    'log_votecount']]
scatter_data.columns = ['log(gross)', 'log(release_width)', 'metascore', 
    'log(fame)', 'major_awards', 
    'log(imdb_votecount)']
sns.pairplot(scatter_data, size = 2).set(xticks = [], yticks = [])
plt.title('Scatterplot matrix of variables in model')
plt.show()

#***---RUN MODEL AND EVALUATE-----------------------
#1. PREDICT LOG TOTAL GROSS FROM RELEASE WIDTH:
predictors = ['log_release_width', 'metascore', 'log_average_fame',
    'major_award_wins_or_noms', 'log_votecount']
X = training_data[predictors]
X = sm.add_constant(X)
y = training_data.log_gross
model = sm.OLS(y, X)
results = model.fit()
print results.summary()

#2. Plot hist of residuals:
resids1 = results.resid
plt.hist(resids1)
plt.title('Histogram of model residuals', fontsize = '20')
plt.xlabel('Residual size', fontsize = '20')
plt.ylabel('Frequency', fontsize = '20')
plt.xticks(fontsize = '16')
plt.yticks(fontsize = '16')
sns.despine()
plt.show()

#3. Q-Q plot of residuals:
sci.probplot(resids1, dist = "norm", plot = plt)
plt.show()

#4. Plot residuals against predicted values on training data:
plt.scatter(results.fittedvalues, 
    resids1, facecolor = 'none', edgecolor = 'maroon')
plt.axhline(y = 0, color = 'black', ls = 'dashed')
plt.title('Residual model error plotted against training fitted values\nResponse is log(total_gross)', fontsize = '15')
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.axis([6,22,-3,3])
plt.show()

#5. Calculate and plot unlogged residuals against predicted values:
#***THIS MAY NOT BE WORTH IT BECAUSE THERE'S A REASON THEY WERE LOGGED!
unlogged_resids_train = np.exp(training_data.log_gross) - np.exp(results.fittedvalues)
plt.scatter(np.exp(results.fittedvalues), 
    unlogged_resids_train, facecolor = 'none', edgecolor = 'maroon')
plt.axhline(y = 0, color = 'black', ls = 'dashed')
plt.title('Residual model error plotted against training fitted values\nResponse is log(total_gross)', fontsize = '15')
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.show()

#6. Plot the model's predicted ys vs observed ys in test set:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)
plt.scatter(y_predicted, test_data['log_gross'], facecolors = 'none', edgecolors = 'black')
xyline = np.arange(6,23,1)
plt.plot(xyline,xyline, ls = 'dashed')
plt.axis([6,22,6,22])
plt.title('Model predicted log(total_gross) vs observed log(total_gross)')
plt.xlabel('Observed log(total_gross)')
plt.ylabel('Predicted log(total_gross)')
plt.show()

#7a Predict test set ys from test set Xs:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)

#7b. Plot the model residuals against test set ys:
resids2 = test_data.log_gross - y_predicted
plt.scatter(test_data.log_gross, 
    resids2, facecolor = 'none', edgecolor = 'maroon')
plt.axhline(y = 0, color = 'black', ls = 'dashed')
plt.title('Residual model error plotted against test data observed response data.\nResponse is log(total_gross).', fontsize = '15')
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.show()

#8. Plot the model predicted values for the strongest predictor against the
#actual values for that predictor





