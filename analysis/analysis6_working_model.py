import scipy.stats as sci
import pandas as pd, numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
predictors = ['total_gross', 'major_award_wins_or_noms','release_width', 
    'fame', 'fame_actor2'] 
data = data[data.release_width < 50000]
data = data.dropna(subset = predictors)

#Make scatterplot matrix of predictors to 

#***---PREDICT LOG TOTAL GROSS FROM RELEASE WIDTH:
import statsmodels.formula.api as smf
data = data[data.fame_actor2 > 0]
data = data[data.fame > 0]
data['average_fame'] = (data.fame + data.fame_actor2)/2
data['any_versions'] = [1 if x > 0 else 0 for x in data.version_count]
data['minor_awards_total'] = data.minor_award_wins + data.minor_award_noms
data['log_gross'] = np.log(data.total_gross)
est = smf.ols(formula = 'np.log(total_gross) ~ np.log(release_width) +\
    metascore + np.sqrt(average_fame)  +\
    major_award_wins_or_noms + np.log(votecount_clean)', data = data).fit()
print est.summary()

#Plot histogram of residuals from original model:
resids2 = est.resid
plt.hist(resids2)
plt.title('Histogram of residuals')
plt.show()

sm.graphics.plot_fit(est, 1)
plt.show()

#1. Plot the entire model against observed ys

#2. Plot the model against test set ys

#3. Plot the unlogged residuals (from test set?)

#Find mean squared error after plugging in test set data. MSE is sum of squared differences between predicted y values and actual y values of the test set. Observed is what you really saw and predicted is what your model predicts.

