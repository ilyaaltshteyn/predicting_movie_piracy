#This script models total_gross from a number of predictors.

import pandas as pd, numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
predictors = ['total_gross', 'major_award_wins_or_noms',] 
    # 'minor_award_wins', 'minor_award_noms', 'metascore']
data = data.dropna(subset = predictors)

#Keep track of what you're doing by adding the outcomes to a list:
outcomes_list = []

#m1***---First do simplest model:
y = data.total_gross
X = data.major_award_wins_or_noms
X = sm.add_constant(X)
print '\n', X.head()

#Run model with 1 predictor, check residuals:
est = sm.OLS(y, X)
est = est.fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
X_prime = np.linspace(X.major_award_wins_or_noms.min(), X.major_award_wins_or_noms.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

y_hat = est.predict(X_prime)
plt.scatter(X.major_award_wins_or_noms, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Major award wins + nominations")
plt.ylabel("Total gross")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #Add regression line
plt.show()

#Plot histogram of residuals:
resids = est.resid
plt.hist(resids)
plt.title('Histogram of residuals for total_gross = B*major_award_wins_or_noms + k')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, resids)
plt.hlines(0, 0,2.5e8)
plt.show()

outcomes_list.append(['m1',est.rsquared, est.aic])

#This model is all bad. The omnibus value suggests that there's
#either skew or kurtosis. The residuals are no normally distributed,
#and also have a decreasing variance as you move across the values
#of the predictor.

#m2***---QUADRATIC MODEL----- TRY 1: sqrt(outcome)
data['sqrt_gross'] = np.sqrt(data.total_gross)
y = data.sqrt_gross
X = data.major_award_wins_or_noms
X = sm.add_constant(X)
print '\n', X.head()

#Run model with 1 predictor, check residuals:
est = sm.OLS(y, X)
est = est.fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
X_prime = np.linspace(X.major_award_wins_or_noms.min(), X.major_award_wins_or_noms.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

y_hat = est.predict(X_prime)
plt.scatter(X.major_award_wins_or_noms, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Major award wins + nominations")
plt.ylabel("Total gross")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #Add regression line
plt.show()

#Plot histogram of residuals:
resids = est.resid
plt.hist(resids)
plt.title('Histogram of residuals for total_gross = B*major_award_wins_or_noms + k')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, resids, facecolors = 'none',
    edgecolors = 'blue', alpha = .5)
# plt.hlines(0, 0,2.5e8)
plt.show()

outcomes_list.append(['m2',est.rsquared, est.aic])

#m3***EXPONENTIAL MODEL: log(outcome)
data['log_gross'] = np.log(data.total_gross)
y = data.log_gross
X = data.major_award_wins_or_noms
X = sm.add_constant(X)
print '\n', X.head()

#Run model with 1 predictor, check residuals:
est = sm.OLS(y, X)
est = est.fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
X_prime = np.linspace(X.major_award_wins_or_noms.min(), X.major_award_wins_or_noms.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

y_hat = est.predict(X_prime)
plt.scatter(X.major_award_wins_or_noms, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Major award wins + nominations")
plt.ylabel("Total gross")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #Add regression line
plt.show()

#Plot histogram of residuals:
resids = est.resid
plt.hist(resids)
plt.title('Histogram of residuals for total_gross = B*major_award_wins_or_noms + k')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, resids, facecolors = 'none',
    edgecolors = 'blue', alpha = .5)
# plt.hlines(0, 0,2.5e8)
plt.show()

outcomes_list.append(['m3',est.rsquared, est.aic])

#m4***---LOGARITHMIC MODEL: log(predictor)
data['log_major_award_wins_or_noms'] = np.log(data.major_award_wins_or_noms + .5)
y = data.total_gross
X = data.log_major_award_wins_or_noms
X = sm.add_constant(X)
print '\n', X.head()

#Run model with 1 predictor, check residuals:
est = sm.OLS(y, X)
est = est.fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
X_prime = np.linspace(X.log_major_award_wins_or_noms.min(), X.log_major_award_wins_or_noms.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

y_hat = est.predict(X_prime)
plt.scatter(X.log_major_award_wins_or_noms, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Major award wins + nominations")
plt.ylabel("Total gross")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #Add regression line
plt.show()

#Plot histogram of residuals:
resids = est.resid
plt.hist(resids)
plt.title('Histogram of residuals for total_gross = B*major_award_wins_or_noms + k')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, resids, facecolors = 'none',
    edgecolors = 'blue', alpha = .5)
# plt.hlines(0, 0,2.5e8)
plt.show()

outcomes_list.append(['m4',est.rsquared, est.aic])

#m5***---Something else MODEL: log(predictor) AND sqrt(outcome)
data['sqrt_gross'] = np.sqrt(data.total_gross)
data['log_major_award_wins_or_noms'] = np.log(data.major_award_wins_or_noms + .5)
y = data.sqrt_gross
X = data.log_major_award_wins_or_noms
X = sm.add_constant(X)
print '\n', X.head()

#Run model with 1 predictor, check residuals:
est = sm.OLS(y, X)
est = est.fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
X_prime = np.linspace(X.log_major_award_wins_or_noms.min(), X.log_major_award_wins_or_noms.max(), 100)[:, np.newaxis]
X_prime = sm.add_constant(X_prime)  # add constant as we did before

y_hat = est.predict(X_prime)
plt.scatter(X.log_major_award_wins_or_noms, y, alpha=0.3)  # Plot the raw data
plt.xlabel("Major award wins + nominations")
plt.ylabel("Total gross")
plt.plot(X_prime[:, 1], y_hat, 'r', alpha=0.9) #Add regression line
plt.show()

#Plot histogram of residuals:
resids = est.resid
plt.hist(resids)
plt.title('Histogram of residuals for total_gross = B*major_award_wins_or_noms + k')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, resids, facecolors = 'none',
    edgecolors = 'blue', alpha = .5)
# plt.hlines(0, 0,2.5e8)
plt.show()

outcomes_list.append(['m5',est.rsquared, est.aic])

#m6***2ND ORDER POLYNOMIAL AGAINST LOGGED PREDICTOR:
import statsmodels.formula.api as smf
data['log_gross'] = np.log(data.total_gross)
est = smf.ols(formula = 'log_gross ~ major_award_wins_or_noms +\
    I(major_award_wins_or_noms**2)', data = data).fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
sm.graphics.plot_fit(est, 1)
plt.show()

#Plot histogram of residuals:
resids2 = est.resid
plt.hist(resids2)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, 
    resids2, alpha = .2)
# plt.hlines(y = 0)
# plt.axis((1,6,-6,6))
plt.title('Residuals plotted against model prediction')
plt.show()

outcomes_list.append(['m6',est.rsquared, est.aic])

#Compute R**2: .014
print est.rsquared

#m7**--2ND ORDER POLYNOMIAL AGAINST SQRT PREDICTOR:
import statsmodels.formula.api as smf
data['sqrt_gross'] = np.sqrt(data.total_gross)
est = smf.ols(formula = 'sqrt_gross ~ major_award_wins_or_noms +\
    I(major_award_wins_or_noms**2)', data = data).fit()
print est.summary()

#Plot model:
#Pick 100 points evenly spaced from min to max:
sm.graphics.plot_fit(est, 1)
plt.show()

#Plot histogram of residuals:
resids2 = est.resid
plt.hist(resids2)
plt.title('Histogram of residuals')
plt.show()

#Plot residuals against predicted values:
plt.scatter(est.fittedvalues, 
    resids2, alpha = .2)
# plt.hlines(y = 0)
# plt.axis((1,6,-6,6))
plt.title('Residuals plotted against model prediction')
plt.show()

outcomes_list.append(['m7',est.rsquared, est.aic])

#Compute R**2: .014
print est.rsquared
