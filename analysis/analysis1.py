#This script runs negative binomial models on the clean data. It uses
#version_count as the outcome variable and several combinations of predictors.

#This analysis follows instructions for doing negative binomial analyses from
#here: http://bit.ly/1H7QG4A

#Make function that calculates likelihood for a neg binom model for count data

import numpy as np
from scipy.stats import nbinom
def _ll_nb2(y, X, beta, alph):
     mu = np.exp(np.dot(X, beta))
     size = 1 / alph
     prob = size / (size + mu)
     ll = nbinom.logpmf(y, size, prob)
     return ll

#Create new model class that inherits from GenericLikelihoodModel:
from statsmodels.base.model import GenericLikelihoodModel
class NBin(GenericLikelihoodModel):
     def __init__(self, endog, exog, **kwds):
         super(NBin, self).__init__(endog, exog, **kwds)
     def nloglikeobs(self, params):
         alph = params[-1]
         beta = params[:-1]
         ll = _ll_nb2(self.endog, self.exog, beta, alph)
         return -ll
     def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
         if start_params == None:
             # Reasonable starting values
             start_params = np.append(np.zeros(self.exog.shape[1]), .5)
             start_params[0] = np.log(self.endog.mean())
         return super(NBin, self).fit(start_params=start_params,
                                      maxiter=maxiter, maxfun=maxfun,
                                      **kwds)

import pandas as pd
data = pd.read_csv('/Users/ilya/metis/week2/project2/clean_data.csv')
del data['Unnamed: 0']
data = data[data.version_count > 0]
data = data.dropna(subset = ['total_gross', 'imdb_rating', 'votecount_clean',
    'runtime_mins', 'version_count', 'major_award_wins_or_noms'])

import patsy
#Outcome var is version_count
#Input var is total_gross
y, X = patsy.dmatrices('version_count~major_award_wins_or_noms', data)
# print y[:5]
# print X[:5]

mod = NBin(y, X)
res = mod.fit()
print res.summary()

y, X = patsy.dmatrices('total_gross ~ major_award_wins_or_noms +\
    minor_award_wins + minor_award_noms', data)
mod2 = NBin(y, X)
res2 = mod2.fit()
print res2.summary()





