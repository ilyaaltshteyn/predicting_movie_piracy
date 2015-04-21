#Going to model the outcome variable version_count using an
#ols regression.

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci

data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
data['minor_award_wins_and_noms'] = data['minor_award_wins'] + \
    data['minor_award_noms']

predictors = ['total_gross', 'year', 'metascore', 'major_award_wins_or_noms', 
    'version_count', 'minor_award_wins_and_noms', 'votecount_clean']
data = data[predictors]
data = data.dropna(subset = predictors)

#Model version_count using major_award_wins.
sci.probplot(data.version_count, plot = plt)
plt.show()
fit1 = smf.ols("version_count ~ major_award_wins_or_noms", data).fit()
print fit1.summary()
sm.graphics.plot_fit(fit1, 1)
plt.show()
#Prob(Omnibus) is very low, so the 

#Plot histogram of residuals:
resids1 = fit1.resid
plt.hist(resids1)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(fit1.fittedvalues, 
    resids1, alpha = .2)
plt.hlines(y = 0, xmin = -2, xmax = 12)
plt.title('Residuals plotted against model prediction')
plt.show()

#Compute R**2: .013

#Residual variance decreases as you go across the x-axis. Also,
#residuals are non-normally distributed, with a right-skewed tail.

#***---BOXCOX TRANSFORM THE OUTCOME VARIABLE:
#Model a boxcox transformation of the outcome variable:
#According to the scipy documentation, you can add any value to the
#data before running the boxcox function on it to "shift" it over so
#that all values are positive. See http://bit.ly/1F9uoxM
#Also, sci.boxcox is returning all the transformed values but also
#returns the lambda that maximizes the log-likelihood function.
#I shifted it .5 because that's half of the smallest non-zero value.
data['version_count_positive'] = (data.version_count + .5)
data['version_count_boxcox'] = sci.boxcox(data.version_count_positive)[0]
sci.probplot(data.version_count_boxcox, plot = plt)
plt.show()
fit2 = smf.ols("version_count_boxcox ~ major_award_wins_or_noms", data).fit()
print fit2.summary()
sm.graphics.plot_fit(fit2, 1)
plt.show()

#Plot histogram of residuals:
resids2 = fit2.resid
plt.hist(resids2)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(fit2.fittedvalues, 
    resids2, alpha = .2)
# plt.hlines(y = 0)
# plt.axis((1,6,-6,6))
plt.title('Residuals plotted against model prediction')
plt.show()

#Compute R**2: .014
print fit2.rsquared

#***---Square-root transform the outcome variable:

data['version_count_positive'] = (data.version_count)
data['square_rooted'] = np.sqrt(data.version_count_positive)
sci.probplot(data.square_rooted, plot = plt)
plt.show()
fit3 = smf.ols("square_rooted ~ major_award_wins_or_noms", data).fit()
print fit3.summary()
sm.graphics.plot_fit(fit3, 1)
plt.show()

#Plot histogram of residuals:
resids3 = fit3.resid
plt.hist(resids3)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(fit3.fittedvalues, 
    resids3, alpha = .2)
# plt.hlines(y = 0)
# plt.axis((1,6,-6,6))
plt.title('Residuals plotted against model prediction')
plt.show()

#Compute R**2: .014

#***---PREDICT CATEGORICAL VERSION COUNT from total_gross:
data['version_count_cat'] = [1 if x > 0 else 0 for x in data.version_count]
data['log_gross'] = np.log(data.total_gross)

sci.probplot(data.version_count_cat, plot = plt)
plt.show()
fit3 = smf.ols("square_rooted ~ major_award_wins_or_noms", data).fit()
print fit3.summary()
sm.graphics.plot_fit(fit3, 1)
plt.show()

#Plot histogram of residuals:
resids3 = fit3.resid
plt.hist(resids3)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(fit3.fittedvalues, 
    resids3, alpha = .2)
# plt.hlines(y = 0)
# plt.axis((1,6,-6,6))
plt.title('Residuals plotted against model prediction')
plt.show()


