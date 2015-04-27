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
plt.hist(training_data.total_gross/1000000, bins = 30, color = 'maroon', alpha= .8)
plt.title('Distribution of movie total domestic grosses in millions of $.\nTraining\
 data only, n = 1227', fontsize = '18')
#The far-right outlier is the Dark Night (2008)
plt.xlabel('Millions of dollars made', fontsize = '17')
plt.ylabel('Number of movies', fontsize = '17')
plt.xticks(fontsize = '16')
plt.yticks(fontsize = '16')
plt.annotate('Avatar', xy=(735, 5), xytext=(700, 40),
            arrowprops=dict(facecolor='black', shrink=0.05), fontsize = '16'
            )
sns.despine()
plt.show()

#2. Scatterplot matrix of predictors:
# scatter_data = training_data[['log_gross', 'log_release_width', 'metascore', 
#     'log_average_fame', 'major_award_wins_or_noms', 
#     'log_votecount']]
# scatter_data.columns = ['log(gross)', 'log(release_width)', 'metascore', 
#     'log(fame)', 'major_awards', 
#     'log(imdb_votecount)']
# sns.pairplot(scatter_data, size = 2).set(xticks = [], yticks = [])
# plt.show()

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
plt.hist(resids1, color = 'maroon', alpha = .8)
plt.title('Histogram of model residuals for training set', fontsize = '18')
plt.xlabel('Residual', fontsize = '17')
plt.ylabel('Frequency', fontsize = '17')
plt.xticks(fontsize = '16')
plt.yticks(fontsize = '16')
sns.despine()
plt.show()

#3. Q-Q plot of residuals:
sci.probplot(resids1, dist = "norm", plot = plt)
plt.show()

#4. Plot residuals against predicted values on training data:
plt.scatter(results.fittedvalues, 
    resids1, facecolor = '#A92A2A', edgecolor = 'black', alpha = .75)
plt.axhline(y = 0, color = 'black', ls = 'dashed')
plt.title('Model residuals plotted against fitted values in training data\n', fontsize = '18')
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.xlabel('Fitted log(total_gross)', fontsize = '16')
plt.ylabel('Difference between fitted and\nobserved log(total_gross) in training data', fontsize = '16')
plt.axis([6,22,-3,3])
plt.show()

#5. Plot the model's predicted ys vs observed ys in test set:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)
plt.scatter(y_predicted, test_data['log_gross'], facecolors = '#C67C7C', edgecolors = 'black')
xyline = np.arange(6,23,1)
plt.plot(xyline,xyline, ls = 'dashed', color = 'black', alpha = .8)
plt.axis([8,21,8,21])
plt.title('Model predicted log(total_gross) vs observed log(total_gross) in the test dataset',
    fontsize = '18')
plt.xlabel('Observed log(total_gross)', fontsize = 16)
plt.ylabel('Predicted log(total_gross)', fontsize = 16)
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.show()

#6 Predict test set ys from test set Xs:
test_X = test_data[predictors]
test_X = sm.add_constant(test_X)
y_predicted = results.predict(test_X)

#7. Plot the model residuals against predicted in test data:
resids2 = test_data.log_gross - y_predicted
plt.scatter(y_predicted, 
    resids2, facecolor = '#A92A2A', edgecolor = 'black', alpha = .75)
plt.axhline(y = 0, color = 'black', ls = 'dashed')
plt.title('Residual model error plotted against model-predicted log(total_gross) for test data\n', fontsize = '18')
plt.xlabel('Fitted log(total_gross)', fontsize = '16')
plt.ylabel('Residual', fontsize = '16')
plt.xticks(fontsize = '15')
plt.yticks(fontsize = '15')
plt.show()

#8. Plot the model predicted values for the strongest predictor against the
#actual values for that predictor in the test and training sets:
#In training set:
sm.graphics.plot_fit(results, 1)
plt.show()

#In test set:
actual_y_vals = test_data.log_gross
x_vals = test_data.log_release_width
plt.scatter(x_vals, actual_y_vals, facecolor = 'orange', edgecolor = 'black', label = 'Actual values', alpha = .6)
plt.scatter(x_vals, y_predicted, facecolor = 'blue', edgecolor = 'black', alpha = .8, label = 'Model prediction')
plt.axis([-1,9,7,21])
plt.title('Predicted total_gross as a function of how widely the movie is released', fontsize = '18')
plt.xlabel('log(release_width)', fontsize = '16')
plt.ylabel('log(total_gross)', fontsize = '16')
plt.legend(loc = 4, fontsize = '16')
plt.annotate('"Shut Up and Sing" made $927,270', xy=(4.48,13.63), xytext=(3.5,17), arrowprops=dict(arrowstyle = "->"), fontsize = '15')
plt.annotate('My model would predict that it made $803,118', xy=(4.5,13.2), xytext=(5,12), arrowprops=dict(arrowstyle = "->"), fontsize = '15')
plt.show()

#9. How well did the model work on my test data?
#9a. Calculate mean squared error for the training and test data:
#training:
print "Mean Squared Error of training set is: %f" % results.mse_resid
test_mse = (y_predicted - test_data.log_gross)**2
print "Mean Squared Error on test set is: %f" % (np.mean(test_mse))
# Mean Squared Error of training set is: 0.375303
# Mean Squared Error on test set is: 0.391886

